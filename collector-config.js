// CUBE-REV 0.6.10 collector configuration.
// Keep enabled=false until the Google Apps Script collector is deployed.
window.CUBE_REV_COLLECTOR_CONFIG = {
  enabled: false,
  endpoint: '', // Example: https://script.google.com/macros/s/DEPLOYMENT_ID/exec
  studyId: 'CUBE-REV-0.6.10',
  studyToken: '', // Paste the token printed by setupCollector(). This is an intake key, not a secret.
  autoSubmitOnComplete: true,
  gzipWhenAvailable: true,
  timeoutMs: 30000
};
