import fs from "node:fs";

const path = process.argv[2] ?? "g7/p2/source-registry.json";
const data = JSON.parse(fs.readFileSync(path, "utf8"));

if (data.schema_version !== "g7-p2-source-registry-1") {
  throw new Error("SOURCE_REGISTRY_SCHEMA_VERSION");
}
if (!Array.isArray(data.sources) || data.sources.length < 4) {
  throw new Error("SOURCE_REGISTRY_TOO_SMALL");
}

const ids = new Set();
for (const source of data.sources) {
  for (const key of [
    "source_id","title","source_class","provides","move_by_move",
    "access_status","bulk_acquisition","data_rights_status",
    "redistribution_status","priority","notes"
  ]) {
    if (!(key in source)) throw new Error(`SOURCE_MISSING_FIELD:${source.source_id ?? "?"}:${key}`);
  }
  if (ids.has(source.source_id)) throw new Error(`SOURCE_DUPLICATE_ID:${source.source_id}`);
  ids.add(source.source_id);

  const rightsUnknown = /UNSPECIFIED|UNKNOWN/.test(source.data_rights_status);
  if (rightsUnknown && /AUTOMATIC_ALLOWED/.test(source.bulk_acquisition)) {
    throw new Error(`RIGHTS_ACQUISITION_CONFLICT:${source.source_id}`);
  }
  if (source.redistribution_status === "ALLOWED_WITH_REQUIRED_NOTICE" &&
      source.data_rights_status !== "EXPLICIT_EXPORT_TERMS") {
    throw new Error(`REDISTRIBUTION_WITHOUT_EXPLICIT_TERMS:${source.source_id}`);
  }
}

for (const required of [
  "wca_results_v2",
  "cubesolves_2014_dump",
  "speedcubing_reconstructions",
  "cubedb",
  "manual_reconstruction_intake"
]) {
  if (!ids.has(required)) throw new Error(`REQUIRED_SOURCE_MISSING:${required}`);
}

console.log("G7_P2_SOURCE_REGISTRY_PASS");
console.log("SOURCES\t" + data.sources.length);
console.log("MOVE_BY_MOVE_SOURCES\t" + data.sources.filter(x => x.move_by_move).length);
console.log("AUTO_BULK_ALLOWED\t" + data.sources.filter(x => x.bulk_acquisition === "AUTOMATIC_ALLOWED").length);
console.log("RIGHTS_HOLD_SOURCES\t" + data.sources.filter(x => /HOLD/.test(x.redistribution_status)).length);
