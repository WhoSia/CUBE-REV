export function classifyToken(rawToken) {
  const raw = rawToken.replace(/[’′]/g, "'").trim();
  if (/^[URFDLB](?:w)?(?:2'?|'|)?$/.test(raw)) {
    return raw.includes("w") ? "WIDE_TURN" : "FACE_TURN";
  }
  if (/^[urfdlb](?:2'?|'|)?$/.test(raw)) return "WIDE_TURN";
  if (/^[MES](?:2'?|'|)?$/.test(raw)) return "SLICE_TURN";
  if (/^[xyz](?:2'?|'|)?$/.test(raw)) return "ROTATION";
  return "UNKNOWN";
}

export function parseReconstruction(text) {
  const events = [];
  let ordinal = 0;
  let sawRotation = false;
  let sawExtended = false;
  let sawUnknown = false;

  const lines = String(text ?? "").replace(/\r\n?/g, "\n").split("\n");
  lines.forEach((line, index) => {
    const lineNo = index + 1;
    const marker = line.indexOf("//");
    const movePart = marker >= 0 ? line.slice(0, marker) : line;
    const annotation = marker >= 0 ? line.slice(marker + 2).trim() : "";

    const tokens = movePart
      .trim()
      .split(/\s+/)
      .filter(Boolean);

    for (const token of tokens) {
      const normalizedToken = token.replace(/^[([{]+/, "").replace(/[)\]}]+$/, "");
      if (!normalizedToken) continue;
      const kind = classifyToken(normalizedToken);
      if (kind === "ROTATION") sawRotation = true;
      if (kind === "WIDE_TURN" || kind === "SLICE_TURN") sawExtended = true;
      if (kind === "UNKNOWN") sawUnknown = true;
      events.push({
        ordinal: ordinal++,
        raw: normalizedToken.replace(/[’′]/g, "'"),
        kind,
        annotation: null,
        line: lineNo,
      });
    }

    if (annotation) {
      events.push({
        ordinal: ordinal++,
        raw: "// " + annotation,
        kind: "ANNOTATION",
        annotation,
        line: lineNo,
      });
    }
  });

  let geometry_status = "HTM_READY";
  if (sawUnknown) geometry_status = "UNRESOLVED";
  else if (sawExtended) geometry_status = "EXTENDED_MOVE_KERNEL_REQUIRED";
  else if (sawRotation) geometry_status = "FRAME_CANONICALIZATION_REQUIRED";

  return {
    status: sawUnknown ? "PARTIAL" : "PARSED",
    geometry_status,
    events,
  };
}
