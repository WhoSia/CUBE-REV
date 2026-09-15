#!/usr/bin/env python3
"""Build the release-safe G3-P14-R2 WCA atlas and adversarial checks."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SEED = 314159
N_PERM = 199


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False, lineterminator="\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--attempt-parquet", required=True)
    ap.add_argument("--longitudinal-parquet", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    attempt = Path(args.attempt_parquet).resolve()
    longitudinal = Path(args.longitudinal_parquet).resolve()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    figdir = out / "figures"
    figdir.mkdir(exist_ok=True)

    work_db = out / "p14_r2_work.duckdb"
    if work_db.exists():
        work_db.unlink()
    con = duckdb.connect(str(work_db))
    con.execute("PRAGMA threads=4")
    con.execute("PRAGMA preserve_insertion_order=false")
    aq = str(attempt).replace("'", "''")
    lq = str(longitudinal).replace("'", "''")
    con.execute(f"CREATE VIEW a0 AS SELECT * FROM read_parquet('{aq}')")
    con.execute(f"CREATE VIEW longitudinal AS SELECT * FROM read_parquet('{lq}')")

    invariants = con.execute("""
      SELECT count(*) AS row_count,
             count(DISTINCT (result_id, attempt_number)) unique_keys,
             count(DISTINCT competitor_key) competitors,
             count(DISTINCT competition_id) competitions,
             min(competition_date) date_min, max(competition_date) date_max,
             sum(attempt_status='VALID') valid_n,
             sum(attempt_status='DNF') dnf_n,
             sum(attempt_status='DNS') dns_n,
             sum(attempt_status='NO_RESULT') no_result_n,
             sum(attempt_status NOT IN ('VALID','DNF','DNS','NO_RESULT')) unexpected_n,
             sum((attempt_status='VALID') != (solve_seconds IS NOT NULL)) status_time_mismatch_n
      FROM a0
    """).fetchdf().iloc[0].to_dict()
    for k, v in list(invariants.items()):
        if hasattr(v, "item"):
            invariants[k] = v.item()
        elif hasattr(v, "isoformat"):
            invariants[k] = v.isoformat()
    if invariants["row_count"] != invariants["unique_keys"]:
        raise RuntimeError("primary-key collision")
    if invariants["unexpected_n"] or invariants["status_time_mismatch_n"]:
        raise RuntimeError(f"source semantic invariant failed: {invariants}")

    con.execute("""
      CREATE TABLE comp_order AS
      SELECT competitor_key, competition_id, min(competition_date) competition_date,
             dense_rank() OVER (PARTITION BY competitor_key ORDER BY min(competition_date), competition_id) competition_index
      FROM a0 GROUP BY competitor_key, competition_id
    """)
    con.execute("""
      CREATE TABLE depth AS
      SELECT competitor_key, count(DISTINCT competition_id) competition_depth,
             CASE WHEN count(DISTINCT competition_id)=1 THEN '1'
                  WHEN count(DISTINCT competition_id) BETWEEN 2 AND 4 THEN '2-4'
                  WHEN count(DISTINCT competition_id) BETWEEN 5 AND 19 THEN '5-19'
                  ELSE '20+' END depth_stratum
      FROM a0 GROUP BY competitor_key
    """)
    con.execute("""
      CREATE TABLE initial_skill AS
      WITH first2 AS (
        SELECT a.competitor_key, median(ln(a.solve_seconds)) initial_log_time, count(*) early_valid_n
        FROM a0 a JOIN comp_order c USING (competitor_key, competition_id)
        WHERE a.attempt_status='VALID' AND c.competition_index<=2
        GROUP BY a.competitor_key HAVING count(*)>=3
      )
      SELECT *, ntile(4) OVER (ORDER BY initial_log_time) skill_quartile FROM first2
    """)
    con.execute("""
      CREATE TABLE person_stats AS
      SELECT competitor_key, sum(ln(solve_seconds)) log_sum, count(*) log_n
      FROM a0 WHERE attempt_status='VALID' GROUP BY competitor_key
    """)
    con.execute("""
      CREATE TABLE result_stats AS
      SELECT result_id, sum(ln(solve_seconds)) result_log_sum, count(*) result_log_n
      FROM a0 WHERE attempt_status='VALID' GROUP BY result_id
    """)
    con.execute("""
      CREATE TABLE valid_residual AS
      WITH x AS (
        SELECT a.*, year(a.competition_date) AS competition_year,
          CASE WHEN year(a.competition_date)<2004 THEN '1982-2003'
               WHEN year(a.competition_date)<2010 THEN '2004-2009'
               WHEN year(a.competition_date)<2016 THEN '2010-2015'
               WHEN year(a.competition_date)<2020 THEN '2016-2019'
               WHEN year(a.competition_date)<2023 THEN '2020-2022'
               ELSE '2023-2026' END era,
          ln(a.solve_seconds) log_time,
          CASE WHEN p.log_n-r.result_log_n>0
               THEN (p.log_sum-r.result_log_sum)/(p.log_n-r.result_log_n) END loo_person_mean
        FROM a0 a JOIN person_stats p USING (competitor_key)
        JOIN result_stats r USING (result_id)
        WHERE a.attempt_status='VALID'
      ), y AS (
        SELECT *, log_time-loo_person_mean person_resid
        FROM x WHERE loo_person_mean IS NOT NULL
      ), ctx AS (
        SELECT competition_year, round_type_id, format_id, attempt_number, avg(person_resid) context_position_mean
        FROM y GROUP BY ALL
      )
      SELECT y.*, y.person_resid-c.context_position_mean residual
      FROM y JOIN ctx c USING (competition_year, round_type_id, format_id, attempt_number)
    """)

    annual = con.execute("""
      WITH y AS (
        SELECT year(competition_date) AS competition_year, competitor_key, competition_id, result_id,
               attempt_status, solve_seconds
        FROM a0
      ), firsts AS (SELECT competitor_key, min(competition_year) first_year FROM y GROUP BY competitor_key),
      pa AS (SELECT competition_year, competitor_key, count(*) n FROM y GROUP BY competition_year, competitor_key),
      conc AS (
        SELECT competition_year, sum(n*n)*1.0/sum(n)/sum(n) hhi,
          sum(CASE WHEN rn<=ceil(np*.01) THEN n ELSE 0 END)*1.0/sum(n) top_1pct_share,
          sum(CASE WHEN rn<=ceil(np*.05) THEN n ELSE 0 END)*1.0/sum(n) top_5pct_share,
          sum(CASE WHEN rn<=ceil(np*.10) THEN n ELSE 0 END)*1.0/sum(n) top_10pct_share
        FROM (SELECT *, row_number() OVER(PARTITION BY competition_year ORDER BY n DESC) rn,
                     count(*) OVER(PARTITION BY competition_year) np FROM pa) q GROUP BY competition_year
      )
      SELECT y.competition_year, count(DISTINCT competition_id) competitions,
        count(DISTINCT result_id) results, count(*) attempts, count(DISTINCT y.competitor_key) active_competitors,
        count(DISTINCT CASE WHEN f.first_year=y.competition_year THEN y.competitor_key END) entrants,
        count(DISTINCT CASE WHEN f.first_year<y.competition_year THEN y.competitor_key END) returning_competitors,
        sum(attempt_status='VALID') valid_n, sum(attempt_status='DNF') dnf_n,
        sum(attempt_status='DNS') dns_n, sum(attempt_status='NO_RESULT') no_result_n,
        avg(CAST(attempt_status='DNF' AS INTEGER)) dnf_rate,
        avg(CAST(attempt_status='DNS' AS INTEGER)) dns_rate,
        quantile_cont(solve_seconds,.10) FILTER(attempt_status='VALID') p10_seconds,
        quantile_cont(solve_seconds,.25) FILTER(attempt_status='VALID') p25_seconds,
        quantile_cont(solve_seconds,.50) FILTER(attempt_status='VALID') p50_seconds,
        quantile_cont(solve_seconds,.75) FILTER(attempt_status='VALID') p75_seconds,
        quantile_cont(solve_seconds,.90) FILTER(attempt_status='VALID') p90_seconds,
        c.hhi, c.top_1pct_share, c.top_5pct_share, c.top_10pct_share
      FROM y JOIN firsts f USING(competitor_key) JOIN conc c USING(competition_year)
      GROUP BY y.competition_year, c.hhi, c.top_1pct_share, c.top_5pct_share, c.top_10pct_share ORDER BY y.competition_year
    """).fetchdf()
    write_csv(annual, out / "atlas_annual.csv")

    composition = con.execute("""
      SELECT year(competition_date) AS competition_year, round_type_id, format_id,
             count(DISTINCT result_id) results, count(*) attempts,
             avg(CAST(attempt_status='DNF' AS INTEGER)) dnf_rate,
             avg(CAST(attempt_status='DNS' AS INTEGER)) dns_rate
      FROM a0 GROUP BY ALL ORDER BY competition_year, round_type_id, format_id
    """).fetchdf()
    write_csv(composition, out / "atlas_round_format.csv")

    depth_summary = con.execute("""
      SELECT quantile_cont(competitions,[.1,.25,.5,.75,.9,.99]) competitions_quantiles,
             avg(competitions) competitions_mean,
             quantile_cont(date_diff('day',first_competition_date,last_competition_date)/365.2425,[.1,.25,.5,.75,.9,.99]) span_year_quantiles,
             quantile_cont(attempt_rows,[.1,.25,.5,.75,.9,.99]) attempt_depth_quantiles
      FROM longitudinal
    """).fetchdf()
    depth_summary.to_json(out / "atlas_depth.json", orient="records", indent=2)

    position = con.execute("""
      SELECT attempt_number, count(*) n, avg(log_time) mean_log_time,
             avg(person_resid) mean_person_resid, avg(residual) mean_adjusted_residual,
             stddev_samp(residual) sd_adjusted_residual
      FROM valid_residual GROUP BY attempt_number ORDER BY attempt_number
    """).fetchdf()
    write_csv(position, out / "sequential_position.csv")

    pairs = con.execute("""
      WITH p AS (
        SELECT x.result_id, x.competitor_key, x.competition_id, x.competition_year, x.era,
               x.round_type_id, x.format_id, x.attempt_number k,
               x.residual residual_k, y.residual residual_next,
               s.skill_quartile, d.depth_stratum
        FROM valid_residual x JOIN valid_residual y
          ON x.result_id=y.result_id AND y.attempt_number=x.attempt_number+1
        LEFT JOIN initial_skill s ON s.competitor_key=x.competitor_key
        JOIN depth d ON d.competitor_key=x.competitor_key
      )
      SELECT coalesce(era,'ALL') era, coalesce(CAST(skill_quartile AS VARCHAR),'ALL') skill_quartile,
             coalesce(round_type_id,'ALL') round_type_id, coalesce(format_id,'ALL') format_id,
             coalesce(depth_stratum,'ALL') depth_stratum, count(*) n,
             corr(residual_k,residual_next) lag_corr,
             regr_slope(residual_next,residual_k) lag_slope,
             avg(residual_next-residual_k) mean_next_minus_current
      FROM p GROUP BY GROUPING SETS ((),(era),(skill_quartile),(round_type_id),(format_id),(depth_stratum))
      ORDER BY era,skill_quartile,round_type_id,format_id,depth_stratum
    """).fetchdf()
    write_csv(pairs, out / "sequential_adjacent.csv")

    transitions = con.execute("""
      WITH t AS (
        SELECT x.attempt_status previous_status, y.attempt_status next_status,
               x.attempt_number previous_position, x.round_type_id, x.format_id,
               CASE WHEN x.round_type_id='f' THEN 'final' ELSE 'nonfinal' END finality,
               CASE WHEN year(x.competition_date)<2010 THEN 'pre2010'
                    WHEN year(x.competition_date)<2020 THEN '2010-2019' ELSE '2020+' END era,
               x.competitor_key
        FROM a0 x JOIN a0 y ON x.result_id=y.result_id AND y.attempt_number=x.attempt_number+1
      ), counts AS (
        SELECT previous_status,next_status,previous_position,finality,era,count(*) n
        FROM t GROUP BY ALL
      )
      SELECT *, n*1.0/sum(n) OVER(PARTITION BY previous_status,previous_position,finality,era) probability
      FROM counts ORDER BY previous_status,next_status,previous_position,finality,era
    """).fetchdf()
    write_csv(transitions, out / "dnf_transition_matrix.csv")

    post_dnf = con.execute("""
      WITH q AS (
        SELECT x.attempt_status predecessor_status, x.attempt_number predecessor_position,
               CASE WHEN x.round_type_id='f' THEN 'final' ELSE 'nonfinal' END finality,
               CASE WHEN year(x.competition_date)<2010 THEN 'pre2010'
                    WHEN year(x.competition_date)<2020 THEN '2010-2019' ELSE '2020+' END era,
               x.format_id, x.round_type_id, s.skill_quartile, d.depth_stratum,
               y.residual next_valid_residual
        FROM a0 x JOIN valid_residual y ON x.result_id=y.result_id AND y.attempt_number=x.attempt_number+1
        LEFT JOIN initial_skill s ON s.competitor_key=x.competitor_key
        JOIN depth d ON d.competitor_key=x.competitor_key
        WHERE x.attempt_status IN ('DNF','VALID','DNS')
      )
      SELECT predecessor_status, predecessor_position, finality, era, format_id, round_type_id,
             skill_quartile, depth_stratum, count(*) n,
             avg(next_valid_residual) mean_next_valid_residual,
             median(next_valid_residual) median_next_valid_residual
      FROM q GROUP BY ALL ORDER BY predecessor_status,predecessor_position,finality,era
    """).fetchdf()
    write_csv(post_dnf, out / "dnf_next_valid_residual.csv")

    placebo = con.execute("""
      WITH ordered AS (
        SELECT result_id,attempt_number,
               lead(attempt_status) OVER(PARTITION BY result_id ORDER BY attempt_number) next_status,
               lag(attempt_status) OVER(PARTITION BY result_id ORDER BY attempt_number) prev_status
        FROM a0
      ), flags AS (
        SELECT v.*,o.next_status,o.prev_status
        FROM valid_residual v JOIN ordered o USING(result_id,attempt_number)
      )
      SELECT
        count(*) FILTER(next_status='DNF') pre_dnf_n,
        avg(residual) FILTER(next_status='DNF') pre_dnf_mean_residual,
        count(*) FILTER(prev_status='DNF') post_dnf_n,
        avg(residual) FILTER(prev_status='DNF') post_dnf_mean_residual,
        avg(residual) FILTER(next_status='VALID' AND prev_status='VALID') ordinary_valid_mean_residual
      FROM flags
    """).fetchdf()
    write_csv(placebo, out / "dnf_reverse_time_placebo.csv")

    trajectory = con.execute("""
      WITH cc AS (
        SELECT a.competitor_key,a.competition_id,min(a.competition_date) competition_date,
               c.competition_index,s.skill_quartile,d.depth_stratum,
               median(ln(a.solve_seconds)) median_log_time,count(*) valid_attempts,
               avg(CAST(a.attempt_status='DNF' AS INTEGER)) dnf_rate
        FROM a0 a JOIN comp_order c USING(competitor_key,competition_id)
        LEFT JOIN initial_skill s ON s.competitor_key=a.competitor_key
        JOIN depth d ON d.competitor_key=a.competitor_key
        GROUP BY ALL
      ), z AS (
        SELECT *, date_diff('day',min(competition_date) OVER(PARTITION BY competitor_key),competition_date)/365.2425 years_since_first,
               date_diff('day',lag(competition_date) OVER(PARTITION BY competitor_key ORDER BY competition_index),competition_date) gap_days,
               median_log_time-lag(median_log_time) OVER(PARTITION BY competitor_key ORDER BY competition_index) change_from_previous
        FROM cc
      )
      SELECT skill_quartile,depth_stratum,
             CASE WHEN competition_index<=10 THEN CAST(competition_index AS VARCHAR)
                  WHEN competition_index<=20 THEN '11-20' WHEN competition_index<=50 THEN '21-50' ELSE '51+' END competition_index_bin,
             count(*) person_competitions,count(DISTINCT competitor_key) competitors,
             median(median_log_time) median_log_time,avg(median_log_time) mean_log_time,
             avg(dnf_rate) mean_dnf_rate,avg(years_since_first) mean_years_since_first,
             avg(change_from_previous) mean_change_from_previous,
             avg(change_from_previous) FILTER(gap_days>=180) mean_change_after_180d_gap
      FROM z GROUP BY ALL ORDER BY skill_quartile,depth_stratum,competition_index_bin
    """).fetchdf()
    write_csv(trajectory, out / "skill_trajectory.csv")

    # Deterministic structure-preserving null on a bounded, hash-selected set of complete result blocks.
    perm = con.execute("""
      SELECT result_id, list(residual ORDER BY attempt_number) residuals,
             list(attempt_status ORDER BY attempt_number) statuses
      FROM (
        SELECT a.result_id,a.attempt_number,a.attempt_status,v.residual
        FROM a0 a LEFT JOIN valid_residual v USING(result_id,attempt_number)
        WHERE abs(hash(a.result_id,314159))%100 < 1
      ) q GROUP BY result_id HAVING count(*) BETWEEN 3 AND 5
    """).fetchall()
    rng = np.random.default_rng(SEED)
    observed_xy = []
    observed_dnf = 0
    observed_dnf_den = 0
    blocks = []
    for _, residuals, statuses in perm:
        r = np.array([np.nan if x is None else float(x) for x in residuals])
        s = np.array(statuses, dtype=object)
        blocks.append((r, s))
        ok = np.isfinite(r[:-1]) & np.isfinite(r[1:])
        observed_xy.extend(zip(r[:-1][ok], r[1:][ok]))
        observed_dnf += int(np.sum((s[:-1] == 'DNF') & (s[1:] == 'DNF')))
        observed_dnf_den += int(np.sum(s[:-1] == 'DNF'))
    obs_corr = float(np.corrcoef(np.asarray(observed_xy).T)[0, 1])
    obs_repeat = observed_dnf / observed_dnf_den if observed_dnf_den else np.nan
    null_corr, null_repeat = [], []
    for _ in range(N_PERM):
        xy, rep, den = [], 0, 0
        for r, s in blocks:
            idx = rng.permutation(len(s))
            rp, sp = r[idx], s[idx]
            ok = np.isfinite(rp[:-1]) & np.isfinite(rp[1:])
            xy.extend(zip(rp[:-1][ok], rp[1:][ok]))
            rep += int(np.sum((sp[:-1] == 'DNF') & (sp[1:] == 'DNF')))
            den += int(np.sum(sp[:-1] == 'DNF'))
        null_corr.append(float(np.corrcoef(np.asarray(xy).T)[0, 1]))
        null_repeat.append(rep / den if den else np.nan)
    null = {
        "seed": SEED, "permutations": N_PERM, "selected_blocks": len(blocks),
        "selection_rule": "abs(hash(result_id,314159)) % 100 < 1; block size 3-5",
        "lag_residual_correlation": {"observed": obs_corr, "null_mean": float(np.nanmean(null_corr)),
          "null_sd": float(np.nanstd(null_corr, ddof=1)),
          "two_sided_monte_carlo_p": (1 + sum(abs(x) >= abs(obs_corr) for x in null_corr)) / (N_PERM + 1)},
        "dnf_to_dnf_probability": {"observed": obs_repeat, "null_mean": float(np.nanmean(null_repeat)),
          "null_sd": float(np.nanstd(null_repeat, ddof=1)),
          "upper_monte_carlo_p": (1 + sum(x >= obs_repeat for x in null_repeat)) / (N_PERM + 1)}
    }
    (out / "structure_preserving_null.json").write_text(json.dumps(null, indent=2), encoding="utf-8")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    ax[0].plot(annual.competition_year, annual.active_competitors, color="#2b6cb0")
    ax[0].set_ylabel("Active competitors")
    ax[1].plot(annual.competition_year, annual.p50_seconds, color="#c05621", label="median")
    ax[1].fill_between(annual.competition_year, annual.p25_seconds, annual.p75_seconds, alpha=.2, color="#c05621", label="IQR")
    ax[1].set_ylabel("Valid solve time (s)"); ax[1].set_xlabel("Year"); ax[1].legend()
    fig.tight_layout(); fig.savefig(figdir / "atlas_population_performance.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(position.attempt_number, 100 * (np.exp(position.mean_adjusted_residual) - 1), marker="o")
    ax.axhline(0, color="black", lw=.8); ax.set_xlabel("Attempt number"); ax.set_ylabel("Adjusted difference (%)")
    fig.tight_layout(); fig.savefig(figdir / "within_round_position.png", dpi=180); plt.close(fig)

    summary = {
        "stage": "CUBE-REV Generation III G3-P14-R2",
        "source_invariants": invariants,
        "input_sha256": {attempt.name: sha256(attempt), longitudinal.name: sha256(longitudinal)},
        "zip_sha256": "694fca87aacc9a0dd71331d478af3b574b20cd560c3ee36399ff84f275ca8e75",
        "null": null,
        "authority_ceiling": "attempt-level behavioral telemetry; no cognitive mechanism identification"
    }
    (out / "p14_r2_machine_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    con.close()

    checksum_lines = []
    for p in sorted(x for x in out.rglob("*") if x.is_file() and x.name != "p14_r2_work.duckdb"):
        checksum_lines.append(f"{sha256(p)}  {p.relative_to(out).as_posix()}")
    (out / "checksums.sha256").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
