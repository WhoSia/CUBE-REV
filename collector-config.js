// CUBE-REV 0.7.12 verified receipt-v2 collector configuration.
// Enabled after health, synthetic storage, checksum, receipt, and deduplication checks.
window.CUBE_REV_COLLECTOR_CONFIG = {
  enabled: true,
  endpoint: 'https://script.google.com/macros/s/AKfycbwJEB0khZSmbbvUkjlzdWE9y33ALHml9D8NUnDhPi9_Z5Z6ZmhoRfjwaRo6vjjaDVVyPw/exec',
  manualUploadUrl: 'https://script.google.com/macros/s/AKfycbwJEB0khZSmbbvUkjlzdWE9y33ALHml9D8NUnDhPi9_Z5Z6ZmhoRfjwaRo6vjjaDVVyPw/exec',
  studyId: 'CUBE-REV-0.7.12',
  collectorId: 'CUBE-REV-0712-MAIN',
  protocolVersion: 'receipt-v2',
  autoSubmitOnComplete: true,
  gzipWhenAvailable: true,
  timeoutMs: 90000,
  receiptPollIntervalMs: 1500,
  healthCheckTimeoutMs: 12000
};
