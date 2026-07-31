import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const indexPath = resolve(root, "index.html");
const i18nPath = resolve(root, "js/i18n-controller.js");
const archivePath = resolve(root, "CUBE-REV_0.7.12_GitHub_Pages_Pilot.html");

let index = await readFile(indexPath, "utf8");
index = index
  .replaceAll("0.6.11", "0.7.12")
  .replaceAll("0611", "0712")
  .replaceAll(
    "unbounded_yaw_pitch_full_vertical_orbit_v1",
    "screen_relative_matrix_360_orbit_v1"
  )
  .replaceAll(
    "background_drag_camera; sticker_drag_single_quarter_face_turn; endpoint_direction_resolver_v1",
    "background_drag_screen_relative_matrix_camera; sticker_drag_single_quarter_face_turn; endpoint_direction_resolver_v1"
  )
  .replaceAll(
    "fixed_front_yaw0_pitch0_zoom1",
    "aligned_screen_relative_identity_v1"
  );
await writeFile(indexPath, index, "utf8");
await writeFile(archivePath, index, "utf8");

let i18n = await readFile(i18nPath, "utf8");
i18n = i18n
  .replace(
    "'keymap.speed.title':'양손 virtual-cube 배열'",
    "'keymap.speed.title':'csTimer virtual-cube 배열'"
  )
  .replace(
    "'keymap.speed.desc':'양손 조작에 맞춘 빠른 입력 중심 배열입니다.'",
    "'keymap.speed.desc':'csTimer 양손 배열과 x·y·z 회전을 함께 지원합니다.'"
  )
  .replace(
    "W/O=B/B′. 180° 회전은 같은 키를 두 번 누릅니다.",
    "W/O=B/B′, T·Y/B·N=x/x′, ;/A=y/y′, P/Q=z/z′. 180° 회전은 같은 키를 두 번 누릅니다."
  )
  .replace(
    "'keymap.speed.title':'Two-hand virtual-cube layout'",
    "'keymap.speed.title':'csTimer virtual-cube layout'"
  )
  .replace(
    "'keymap.speed.desc':'A fast two-hand layout for frequent keyboard input.'",
    "'keymap.speed.desc':'The csTimer two-hand layout, including x, y, and z rotations.'"
  )
  .replace(
    "W/O=B/B′. Press the same key twice for 180°.",
    "W/O=B/B′, T·Y/B·N=x/x′, ;/A=y/y′, P/Q=z/z′. Press the same key twice for 180°."
  );
await writeFile(i18nPath, i18n, "utf8");

console.log("CUBE-REV 0.7.12 release identity synchronized.");
