// CUBE-REV 0.7.12 governance-locked collector configuration.
// A receipt-v2 endpoint will be bound only during the separate 0.7.13 dry run.
window.CUBE_REV_COLLECTOR_CONFIG = {
  enabled: false,
  endpoint: '',
  manualUploadUrl: '',
  studyId: 'CUBE-REV-0.7.12',
  collectorId: 'CUBE-REV-0712-RUN-IN-LOCKED',
  protocolVersion: 'receipt-v2',
  autoSubmitOnComplete: false,
  gzipWhenAvailable: true,
  timeoutMs: 30000
};
