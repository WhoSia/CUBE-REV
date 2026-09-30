const NAMED = {
  amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ",
};

export function decodeHtml(s) {
  return String(s ?? "")
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
    .replace(/&([a-z]+);/gi, (m, n) => NAMED[n.toLowerCase()] ?? m);
}

function stripTags(s) {
  return decodeHtml(
    String(s ?? "")
      .replace(/<br\s*\/?\s*>/gi, "\n")
      .replace(/<[^>]+>/g, "")
  )
    .replace(/\u00a0/g, " ")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n[ \t]+/g, "\n")
    .trim();
}

function firstMatch(html, re) {
  const m = String(html).match(re);
  return m ? m[1] : null;
}

function parseCells(rowHtml) {
  return [...String(rowHtml).matchAll(/<(?:th|td)[^>]*>([\s\S]*?)<\/(?:th|td)>/gi)]
    .map(m => stripTags(m[1]));
}

export function parseRecoIndexHtml(html) {
  const ids = [...String(html).matchAll(/href=["'](?:https?:\/\/reco\.nz)?\/?solve\/(\d+)["']/gi)]
    .map(m => Number(m[1]));
  const uniqueIds = [...new Set(ids)].sort((a, b) => a - b);

  const pages = [...String(html).matchAll(/[?&]page=(\d+)/g)]
    .map(m => Number(m[1]))
    .filter(Number.isFinite);

  return {
    solve_ids: uniqueIds,
    min_id: uniqueIds.length ? uniqueIds[0] : null,
    max_id: uniqueIds.length ? uniqueIds.at(-1) : null,
    referenced_pages: [...new Set(pages)].sort((a, b) => a - b),
  };
}

export function parseRecoSolveHtml(html, sourceUrl = null) {
  const h1 = stripTags(firstMatch(html, /<h1[^>]*>([\s\S]*?)<\/h1>/i) ?? "");
  const titleMatch = h1.match(/^(.*?)\s+-\s+([0-9.]+)\s+(.+?)\s+solve$/i);
  if (!titleMatch) throw new Error("RECO_SOLVE_TITLE_PARSE");

  const solver = titleMatch[1].trim();
  const resultText = titleMatch[2];
  const puzzle = titleMatch[3].trim();

  const h3 = stripTags(firstMatch(html, /<h3[^>]*>([\s\S]*?)<\/h3>/i) ?? "");
  const metaMatch = h3.match(/^(?:\[[^\]]+\]\s*)?(\d{4}-\d{2}-\d{2})\s+-\s+(.*?)\s+-\s+reconstruction by\s+(.*)$/i);

  const reconBlock = firstMatch(html, /<div[^>]+id=["']reconstruction["'][^>]*>([\s\S]*?)<\/div>/i);
  if (reconBlock == null) throw new Error("RECO_RECONSTRUCTION_BLOCK_MISSING");
  const reconText = stripTags(reconBlock);
  const lines = reconText.split(/\n+/).map(x => x.trim()).filter(Boolean);
  if (lines.length < 2) throw new Error("RECO_RECONSTRUCTION_TOO_SHORT");
  const scramble = lines[0];
  const reconstruction = lines.slice(1).join("\n");

  const solveIdFromUrl = sourceUrl?.match(/\/solve\/(\d+)/)?.[1] ?? null;
  const solveIdFromCanonical = firstMatch(html, /href=["'][^"']*\/solve\/(\d+)["']/i);
  const solveId = solveIdFromUrl ?? solveIdFromCanonical;

  const algUrl = firstMatch(html, /href=["'](https:\/\/alg\.cubing\.net\/\?[^"']+)["']/i);
  const videoUrl = firstMatch(html, /<iframe[^>]+src=["']([^"']+)["']/i);

  const statsHtml = firstMatch(html, /<table[^>]+id=["']solvestats["'][^>]*>([\s\S]*?)<\/table>/i);
  const stats = {};
  if (statsHtml) {
    const rows = [...statsHtml.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)].map(m => parseCells(m[1]));
    if (rows.length >= 2) {
      const headers = rows[0];
      for (const row of rows.slice(1)) {
        if (row.length < 2) continue;
        const label = row[0];
        stats[label] = {};
        for (let i = 1; i < Math.min(headers.length, row.length); i++) {
          stats[label][headers[i] || "Total"] = row[i];
        }
      }
    }
  }

  const averageNeighborIds = [...String(html).matchAll(/href=["'](?:\.\.\/)?(?:solve\/)?(\d+)["']/gi)]
    .map(m => Number(m[1]))
    .filter(Number.isFinite)
    .filter(id => String(id) !== String(solveId));
  const uniqueNeighbors = [...new Set(averageNeighborIds)];

  return {
    source_id: "reco_nz",
    source_record_id: solveId ? String(solveId) : null,
    source_url: sourceUrl,
    solver,
    result_text: resultText,
    puzzle,
    solve_date: metaMatch?.[1] ?? null,
    competition: metaMatch?.[2]?.trim() ?? null,
    reconstructor: metaMatch?.[3]?.trim() ?? null,
    scramble_raw: scramble,
    reconstruction_raw: reconstruction,
    alg_cubing_url: algUrl ? decodeHtml(algUrl) : null,
    video_url: videoUrl ? decodeHtml(videoUrl) : null,
    stats,
    average_neighbor_ids: uniqueNeighbors,
  };
}
