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
      this.clockApi = options.clockApi || root.CubeRevEligibilityClock;
      this.exportApi = options.exportApi || root.CubeRevExportDecoration;
      this.randomizationApi = options.randomizationApi || root.CubeRevDecisionRandomization;
      this.historyApi = options.historyApi || root.CubeRevHistoryPresentation;
      this.neutralProbeApi = options.neutralProbeApi || root.CubeRevNeutralProbe;
      const installation_id = this.linkageApi.getInstallationId(options.storage || root.localStorage);
      this.linkage = this.linkageApi.createRunInToken(installation_id);
      this.linkage = Object.freeze({ installation_id, ...this.linkage });
      this.probeState = this.randomizationApi.initialState();
      this.causalRunInEligible = true;
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
        document.title = "CUBE-REV 0.7.12 · source-bound browser run-in";
      }
    }

    factorialCell(key) {
      const hash = this.fnv1a32(`memory:${key}`);
      const historyType = (hash & 1) ? "redundant_equivalent" : "geodesic";
      const viewContext = (hash & 2) ? "reoriented" : "stable";
      const modality = this.historyApi.MODALITIES[Math.floor(hash / 4) % this.historyApi.MODALITIES.length];
      return Object.freeze({
        cell_id: `H${this.historyApi.MODALITIES.indexOf(modality) + 1}-${historyType === "geodesic" ? "G" : "R"}-${viewContext === "stable" ? "S" : "V"}`,
        history_modality: modality,
        history_type: historyType,
        view_context: viewContext,
        assignment_method: "fixed_hash_3x2x2_v1"
      });
    }

    fnv1a32(text) {
      let hash = 0x811c9dc5;
      for (const ch of String(text)) {
        hash ^= ch.charCodeAt(0);
        hash = Math.imul(hash, 0x01000193) >>> 0;
      }
      return hash >>> 0;
    }

    decorateSession(session) {
      session.calibration_runtime = {
        protocol_version: this.config.protocol_version,
        calibration_build_id: this.config.build_id,
        mode: this.config.mode,
        linkage: this.linkage,
        collection_locked: true,
        eligibility_clock_state: this.eligibility.state,
        probe_randomization_policy: this.randomizationApi.POLICY_ID,
        browser_timing_status: "BROWSER_TIMING_PENDING"
      };
      return session;
    }

    resolveTrial(trial, participant) {
      const cell = this.factorialCell(`${participant}:${trial.trial_id}`);
      trial.calibration_assignment = { memory: cell };
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
      trial.probe_after = false;
      trial.presentation_mode = cell.history_modality;
      return trial;
    }

    decorateTrial(record, trial) {
      record.calibration_assignment = structuredClone(trial.calibration_assignment);
      record.assigned_history_label = trial.assigned_history_label ?? null;
      const modality = trial.calibration_assignment?.memory?.history_modality || "TERMINAL_ONLY";
      record.presentation_mode = modality;
      record.generating_path_hidden = modality === "TERMINAL_ONLY";
      record.scramble_text_shown = modality === "TEXT_HISTORY";
      record.scramble_animation_shown = modality === "ANIMATED_HISTORY";
      record.visibility_supports_replay_inference = modality !== "TERMINAL_ONLY";
      record.replay_inference_allowed = modality !== "TERMINAL_ONLY";
      return record;
    }

    async presentAssignedHistory(record, trial, helpers) {
      const memory = record?.calibration_assignment?.memory || {};
      helpers.setView?.(memory.view_context || "stable");
      helpers.log("calibration_view_context_applied", { view_context: memory.view_context || "stable" });
      const presentation = this.historyApi.plan(
        memory.history_modality || "TERMINAL_ONLY",
        trial.scramble_tokens,
        {
          exposure_ms: this.config.history_presentation.nominal_exposure_ms,
          minimum_move_ms: this.config.history_presentation.minimum_animated_move_ms
        }
      );
      helpers.log("history_presentation_started", presentation);
      const result = await this.historyApi.present(presentation, helpers);
      record.history_presentation = result;
      helpers.log("history_presentation_completed", result);
      return result;
    }

    decideProbe(record, completedTrials, cryptoSource) {
      const result = this.randomizationApi.decide({
        trial_ordinal: record.ordinal,
        completed_trials: completedTrials,
        state: this.probeState
      }, cryptoSource);
      this.probeState = result.state;
      if (result.causal_run_in_eligible === false) this.causalRunInEligible = false;
      record.probe_policy = structuredClone(result.assignment);
      record.probe_after = ["TIME_MATCHED_NEUTRAL", "STRATEGY_DIAGNOSTIC"].includes(result.assignment.arm);
      return result.assignment;
    }

    prepareProbe(record) {
      const arm = record?.probe_policy?.arm;
      const title = document.querySelector("#probeScreen h2");
      const description = document.querySelector("#probeScreen p");
      const labels = Array.from(document.querySelectorAll("#probeChoices label"));
      this.neutralProbeApi.restoreDom(document);
      if (arm === "TIME_MATCHED_NEUTRAL") {
        record.neutral_probe = this.neutralProbeApi.configureDom(document);
        return arm;
      }
      const diagnostic = [
        ["replay", "방금 본 생성 경로를 역순으로 재생했다 (REPLAY)"],
        ["geodesic_planning", "현재 상태에서 최단 또는 단계 경로를 계획했다"],
        ["algorithmic_chunk", "익숙한 알고리즘·주기·청크를 사용했다"],
        ["local_repair_or_search", "국소 탐색, 프레임 수정, 입력 복구를 했다"],
        ["unsure_or_mixed", "잘 모르겠거나 여러 방법이 섞였다"]
      ];
      labels.forEach((label, index) => {
        const input = label.querySelector("input");
        const text = label.querySelector("span");
        if (input && diagnostic[index]) input.value = diagnostic[index][0];
        if (text && diagnostic[index]) text.textContent = diagnostic[index][1];
        label.classList.remove("hidden");
      });
      if (title) title.textContent = "방금 어떤 방식으로 풀었나요?";
      if (description) description.textContent = "가장 가까운 방식을 하나 선택하세요.";
      return arm;
    }

    decorateExport(session) {
      return this.exportApi.decorate(session, this);
    }

    collectionAllowed() { return false; }
  }

  return { CubeRevCalibrationRuntime };
});
