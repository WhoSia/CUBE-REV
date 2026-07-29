(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api;
  root.CubeRevCalibrationRuntime = api.CubeRevCalibrationRuntime;
})(typeof globalThis !== "undefined" ? globalThis : this, function (root) {
  "use strict";

  class CubeRevCalibrationRuntime {
    constructor(options = {}) {
      this.config = options.config || root.CUBE_REV_CALIBRATION_CONFIG;
      this.linkageApi = options.linkageApi || root.CubeRevCalibrationLinkage;
      this.probeApi = options.probeApi || root.CubeRevProbePolicy;
      this.clockApi = options.clockApi || root.CubeRevEligibilityClock;
      this.exportApi = options.exportApi || root.CubeRevExportDecoration;
      const installation_id = this.linkageApi.getInstallationId(options.storage || root.localStorage);
      this.linkage = this.linkageApi.createRunInToken(installation_id);
      this.linkage = Object.freeze({ installation_id, ...this.linkage });
      this.eligibility = this.clockApi.evaluate({
        ...this.config,
        linkage: this.linkage,
        source_bound_verified: true,
        build_frozen: true,
        protocol_frozen: true,
        collector_receipt_verified: false,
        two_pass_annotation_ready: true
      });
      root.addEventListener?.("cube-rev-language-change", () => this.applyUiIdentity());
      if (typeof setTimeout === "function") setTimeout(() => this.applyUiIdentity(), 0);
    }
    applyUiIdentity() {
      if (typeof document !== "undefined") {
        document.title = "CUBE-REV 0.7.11 Calibration · verified 0.6.11 host";
      }
    }
    factorialCell(key) {
      const n = this.probeApi.fnv1a32(`memory:${key}`) % 8;
      return Object.freeze({
        cell_id: `M${n + 1}`,
        history_visibility: (n & 1) ? "shown" : "hidden",
        history_type: (n & 2) ? "redundant_equivalent" : "geodesic",
        view_context: (n & 4) ? "reoriented" : "stable",
        assignment_method: "fixed_hash_mod_8_v1"
      });
    }
    decorateSession(session) {
      session.calibration_runtime = {
        protocol_version: this.config.protocol_version,
        calibration_build_id: this.config.build_id,
        mode: this.config.mode,
        linkage: this.linkage,
        collection_locked: true,
        eligibility_clock_state: this.eligibility.state
      };
      return session;
    }
    resolveTrial(trial, participant) {
      const cell = this.factorialCell(`${participant}:${trial.trial_id}`);
      trial.calibration_assignment = {
        memory: cell,
        probe: this.probeApi.assign(`${participant}:${trial.trial_id}:probe`)
      };
      if (trial.hidden_generation_candidates?.length) {
        const target = cell.history_type === "geodesic" ? "geodesic" : "uniform_reduced_bridge";
        const option = trial.hidden_generation_candidates.find((x) => x.label === target);
        if (option) {
          trial.scramble = option.scramble;
          trial.scramble_tokens = String(option.scramble).split(/\s+/).filter(Boolean);
          trial.history_length = option.length;
          trial.history_redundancy = option.redundancy;
          trial.assigned_history_label = option.label;
        }
      }
      trial.probe_after = trial.calibration_assignment.probe.arm !== "no_probe";
      trial.presentation_mode = cell.history_visibility === "shown"
        ? "fixed_text_history_then_terminal_state"
        : "terminal_state_only";
      return trial;
    }
    decorateTrial(record, trial) {
      record.calibration_assignment = structuredClone(trial.calibration_assignment);
      record.assigned_history_label = trial.assigned_history_label ?? null;
      const shown = trial.calibration_assignment?.memory?.history_visibility === "shown";
      record.presentation_mode = trial.presentation_mode;
      record.generating_path_hidden = !shown;
      record.scramble_text_shown = shown;
      record.visibility_supports_replay_inference = shown;
      record.replay_inference_allowed = shown;
      return record;
    }
    async presentAssignedHistory(record, trial, helpers) {
      const viewContext = record?.calibration_assignment?.memory?.view_context || "stable";
      helpers.setView?.(viewContext);
      helpers.log("calibration_view_context_applied", { view_context: viewContext });
      if (!record?.scramble_text_shown) return false;
      helpers.setText(trial.scramble);
      helpers.log("calibration_history_presented", {
        assigned_history_label: record.assigned_history_label,
        exposure_ms: 1600,
        memory_cell: record.calibration_assignment.memory
      });
      await helpers.sleep(1600);
      helpers.setText(helpers.privateLabel());
      return true;
    }
    prepareProbe(record) {
      const arm = record?.calibration_assignment?.probe?.arm || "no_probe";
      const title = document.querySelector("#probeScreen h2");
      const description = document.querySelector("#probeScreen p");
      const labels = Array.from(document.querySelectorAll("#probeChoices label"));
      const diagnostic = [
        ["replay", "방금 본 생성 경로를 역순으로 재생했다 (REPLAY)"],
        ["geodesic_planning", "현재 상태에서 최단 또는 단계 경로를 계획했다"],
        ["algorithmic_chunk", "익숙한 알고리즘·주기·청크를 사용했다"],
        ["local_repair_or_search", "국소 탐색, 프레임 수정, 입력 복구를 했다"],
        ["unsure_or_mixed", "잘 모르겠거나 여러 방법이 섞였다"]
      ];
      const sham = [
        ["sham_comfort_1", "매우 불편했다"],
        ["sham_comfort_2", "조금 불편했다"],
        ["sham_comfort_3", "보통이었다"],
        ["sham_comfort_4", "조금 편안했다"],
        ["sham_comfort_5", "매우 편안했다"]
      ];
      const content = arm === "sham_probe" ? sham : diagnostic;
      labels.forEach((label, index) => {
        const input = label.querySelector("input");
        const text = label.querySelector("span");
        if (input && content[index]) input.value = content[index][0];
        if (text && content[index]) text.textContent = content[index][1];
        label.classList.remove("hidden");
      });
      if (arm === "sham_probe") {
        if (title) title.textContent = "방금 화면 조작은 얼마나 편안했나요?";
        if (description) description.textContent = "이 문항은 전략 판별과 무관한 고정 sham probe입니다.";
      } else {
        if (title) title.textContent = "방금 어떤 방식으로 풀었나요?";
        if (description) description.textContent = "가장 가까운 방식을 하나 선택하세요.";
      }
      record.probe_policy = structuredClone(record.calibration_assignment.probe);
      return arm;
    }
    decorateExport(session) {
      return this.exportApi.decorate(session, this);
    }
    collectionAllowed() { return false; }
  }
  return { CubeRevCalibrationRuntime };
});
