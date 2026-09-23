/* G3-P35-R1 fail-closed divergence-surface compiler entrypoint.
 * It cannot classify a certified P34 row until the presealed representation
 * instrument binds r1/r2, g/gamma, Phi/E/C/J/Q, and row -> (s,b,H).
 */
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const P34 = join(HERE, '..', 'p34-runtime');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const bankBytes = readFileSync(join(P34, 'p34-bank.json'));
const bank = JSON.parse(bankBytes);
const p34r2 = JSON.parse(readFileSync(join(P34, 'p34-r2-replay-receipt.json'), 'utf8'));
const authorityPath = join(HERE, 'p35-r1-representation-authority.json');
const requiredBindings = [
  'representation_r1', 'representation_r2', 'state_bijection_g', 'action_bijection_gamma',
  'observation_maps_phi', 'action_encodings_e', 'selector_rules_c', 'history_rules_j',
  'target_sets_q', 'row_to_start_budget_history', 'prospective_witness_order',
];
const expectedBankHash = 'cef57e7943510d15d2bfbb59f18761217599f9d5c7b749511a02d1c371e9ae00';
const authorityPresent = existsSync(authorityPath);
const authority = authorityPresent ? JSON.parse(readFileSync(authorityPath, 'utf8')) : null;
const missingBindings = authority
  ? requiredBindings.filter((binding) => authority[binding] === undefined || authority[binding] === null)
  : requiredBindings;
const preconditions = {
  inherited_p34_r2_pass: p34r2.verdict === 'EXACT_CROSS_LANE_SEMANTIC_EQUIVALENCE_PASS',
  bank_sha256_matches_p34: sha(bankBytes) === expectedBankHash,
  bank_schema: bank.schema === 'CUBE-REV-G3-P34-LANE-A-v1',
  representation_authority_materialized: authorityPresent,
  representation_authority_complete: authorityPresent && missingBindings.length === 0,
};
const ready = Object.values(preconditions).every(Boolean);
// Deliberately do not map missing representation authority to I− or OOA.
const receipt = {
  schema: 'CUBE-REV-G3-P35-R1-DIVERGENCE-SURFACE-PREFLIGHT-v1',
  authority: 'G3-P35-R1-PRESEAL',
  inherited_authority: 'G3-P34-R2',
  inputs: {
    p34_bank_sha256: sha(bankBytes),
    p34_r2_receipt_sha256: sha(readFileSync(join(P34, 'p34-r2-replay-receipt.json'))),
    compiler_sha256: sha(readFileSync(fileURLToPath(import.meta.url))),
  },
  preconditions,
  missing_representation_bindings: missingBindings,
  certified_bank_rows: bank.rows.length,
  divergence_surface_census: ready ? 'NOT_IMPLEMENTED_BY_THIS_PREFLIGHT' : {
    I_positive: 'NOT_COMPUTED', I_negative: 'NOT_COMPUTED', R1_only: 'NOT_COMPUTED',
    R2_only: 'NOT_COMPUTED', OOA: 'NOT_COMPUTED',
    reason: 'CERTIFIED_BANK_ROWS_CANNOT_BE_CLASSIFIED_WITHOUT_PRESEALED_REPRESENTATION_INSTRUMENT',
  },
  assumption_level_diagnostics: ready ? 'NOT_IMPLEMENTED_BY_THIS_PREFLIGHT' : 'NOT_COMPUTED_MISSING_G_GAMMA_PHI_E_C_J_Q_AND_ROW_MAPPING',
  first_non_commuting_component_census: ready ? 'NOT_IMPLEMENTED_BY_THIS_PREFLIGHT' : 'NOT_COMPUTED_NO_LOAD_BEARING_REPRESENTATION_CONTEXT_DEFINED',
  minimal_witness: 'NOT_SEARCHED_NO_PROSPECTIVELY_BOUND_REPRESENTATION_ORDERING_INPUT',
  no_witness_region: 'NOT_CERTIFIABLE',
  bank_mutation: false,
  p36_gate: 'CLOSED',
  verdict: ready ? 'P35_R1_PREFLIGHT_READY_NOT_EXECUTED' : 'P35_R1_INSTRUMENT_AUTHORITY_HOLD',
};
mkdirSync(HERE, { recursive: true });
writeFileSync(join(HERE, 'p35-r1-preflight-receipt.json'), `${JSON.stringify(receipt, null, 2)}\n`);
console.log(JSON.stringify(receipt, null, 2));
