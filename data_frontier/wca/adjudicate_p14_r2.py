#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import duckdb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--database", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    c = duckdb.connect(args.database, read_only=True)
    queries = {
      "overall_adjacent": """
        SELECT count(*) n,corr(x.residual,y.residual) corr,regr_slope(y.residual,x.residual) slope
        FROM valid_residual x JOIN valid_residual y
          ON x.result_id=y.result_id AND y.attempt_number=x.attempt_number+1
      """,
      "status_transition": """
        WITH t AS (
          SELECT x.attempt_status predecessor,y.attempt_status successor
          FROM a0 x JOIN a0 y ON x.result_id=y.result_id AND y.attempt_number=x.attempt_number+1
        )
        SELECT predecessor,count(*) denominator,sum(successor='DNF') dnf_next,
               sum(successor='DNF')*1.0/count(*) dnf_next_rate
        FROM t WHERE predecessor IN ('VALID','DNF','DNS') GROUP BY predecessor ORDER BY predecessor
      """,
      "post_valid": """
        WITH q AS (
          SELECT x.attempt_status predecessor,y.residual,
                 CASE WHEN x.round_type_id='f' THEN 'final' ELSE 'nonfinal' END finality
          FROM a0 x JOIN valid_residual y
            ON x.result_id=y.result_id AND y.attempt_number=x.attempt_number+1
          WHERE x.attempt_status IN ('VALID','DNF','DNS')
        )
        SELECT predecessor,finality,count(*) n,avg(residual) mean_residual,
               exp(avg(residual))-1 proportional_difference
        FROM q GROUP BY predecessor,finality ORDER BY finality,predecessor
      """,
      "placebo": """
        WITH o AS (
          SELECT result_id,attempt_number,
                 lead(attempt_status) OVER(PARTITION BY result_id ORDER BY attempt_number) next_status,
                 lag(attempt_status) OVER(PARTITION BY result_id ORDER BY attempt_number) previous_status
          FROM a0
        ), q AS (
          SELECT v.residual,o.next_status,o.previous_status
          FROM valid_residual v JOIN o USING(result_id,attempt_number)
        )
        SELECT count(*) FILTER(next_status='DNF') pre_dnf_n,
               avg(residual) FILTER(next_status='DNF') pre_dnf_mean,
               count(*) FILTER(previous_status='DNF') post_dnf_n,
               avg(residual) FILTER(previous_status='DNF') post_dnf_mean,
               avg(residual) FILTER(next_status='VALID' AND previous_status='VALID') ordinary_mean
        FROM q
      """,
      "trajectory_index": """
        WITH cc AS (
          SELECT a.competitor_key,c.competition_index,median(ln(a.solve_seconds)) median_log_time
          FROM a0 a JOIN comp_order c USING(competitor_key,competition_id)
          WHERE a.attempt_status='VALID' GROUP BY ALL
        ), z AS (
          SELECT *,median_log_time-first_value(median_log_time)
            OVER(PARTITION BY competitor_key ORDER BY competition_index) delta
          FROM cc
        )
        SELECT competition_index,count(*) n,avg(delta) mean_log_change,
               exp(avg(delta))-1 proportional_change
        FROM z WHERE competition_index<=10 GROUP BY competition_index ORDER BY competition_index
      """,
      "position_person": """
        SELECT attempt_number,count(*) n,avg(person_resid) mean_person_residual,
               exp(avg(person_resid))-1 proportional_difference
        FROM valid_residual WHERE attempt_number<=5 GROUP BY attempt_number ORDER BY attempt_number
      """,
      "matched_post_dnf": """
        WITH q AS (
          SELECT x.attempt_status predecessor,x.attempt_number predecessor_position,
                 CASE WHEN x.round_type_id='f' THEN 'final' ELSE 'nonfinal' END finality,
                 CASE WHEN year(x.competition_date)<2010 THEN 'pre2010'
                      WHEN year(x.competition_date)<2020 THEN '2010-2019' ELSE '2020+' END era,
                 x.format_id,x.round_type_id,s.skill_quartile,d.depth_stratum,y.residual
          FROM a0 x JOIN valid_residual y
            ON x.result_id=y.result_id AND y.attempt_number=x.attempt_number+1
          LEFT JOIN initial_skill s ON s.competitor_key=x.competitor_key
          JOIN depth d ON d.competitor_key=x.competitor_key
          WHERE x.attempt_status IN ('VALID','DNF')
        ), cells AS (
          SELECT predecessor_position,finality,era,format_id,round_type_id,skill_quartile,depth_stratum,
                 count(*) FILTER(predecessor='DNF') dnf_n,
                 avg(residual) FILTER(predecessor='DNF') dnf_mean,
                 count(*) FILTER(predecessor='VALID') valid_n,
                 avg(residual) FILTER(predecessor='VALID') valid_mean
          FROM q GROUP BY ALL
        )
        SELECT finality,count(*) cells,sum(dnf_n) dnf_n,
               sum(dnf_n*(dnf_mean-valid_mean))/sum(dnf_n) matched_log_difference,
               exp(sum(dnf_n*(dnf_mean-valid_mean))/sum(dnf_n))-1 matched_proportional_difference
        FROM cells WHERE dnf_n>=20 AND valid_n>=100 GROUP BY finality ORDER BY finality
      """,
      "attempt_availability": """
        WITH r AS (
          SELECT result_id,format_id,round_type_id,count(*) observed_rows,max(attempt_number) max_attempt_number
          FROM a0 GROUP BY ALL
        )
        SELECT format_id,round_type_id,observed_rows,max_attempt_number,count(*) results
        FROM r GROUP BY ALL ORDER BY format_id,round_type_id,observed_rows,max_attempt_number
      """
    }
    result = {}
    for name, query in queries.items():
        df = c.execute(query).fetchdf()
        result[name] = json.loads(df.to_json(orient="records"))
    c.close()
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
