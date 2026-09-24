import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:([A-Za-z]:))/, '$1'));
const read = name => fs.readFileSync(path.join(here, name));
const json = name => JSON.parse(read(name));
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const fail = message => { throw new Error(message); };

const theorem = json('theorem-ledger.json');
const atlas = json('minimal-counterexample-atlas.json');
const novelty = json('novelty-kill-matrix.json');
const tournament = json('transport-tournament.json');
const preseals = ['external-falsification-preseal-a.json','external-falsification-preseal-b.json'].map(json);

if (theorem.theorems?.length !== 10) fail('T1-T10 census mismatch');
if (new Set(theorem.theorems.map(t => t.id)).size !== 10) fail('duplicate theorem id');
if (atlas.cases?.length < 10) fail('counterexample census below contract');
if (novelty.adjudications?.length !== 10) fail('novelty census mismatch');
if (tournament.candidates?.length < 8) fail('candidate census below contract');
if (new Set(tournament.traditions_represented).size < 4) fail('tradition census below contract');
if (tournament.candidates.filter(c => c.status?.startsWith('ELIGIBLE_SURVIVOR')).length !== 2) fail('survivor census mismatch');
if (preseals.some(p => p.status !== 'PRESEALED_NOT_EXECUTED' || p.world_contact !== 'NOT_EXECUTED')) fail('world-contact boundary mismatch');

// The atlas schema retains project-lineage metadata; cube erasure applies to
// theorem premises, claims, candidate definitions, and falsification packets.
const textCorpus = ['qast-axioms.md','theorem-ledger.json','novelty-kill-matrix.json','transport-tournament.json','external-falsification-preseal-a.json','external-falsification-preseal-b.json'].map(n => read(n).toString('utf8')).join('\n');
const forbidden = [/Rubik/i,/CFOP/i,/F2L/i,/큐브/i,/CUBE-REV/i];
const hits = forbidden.filter(re => re.test(textCorpus)).map(String);
if (hits.length) fail(`cube erasure failed: ${hits.join(',')}`);

const files = fs.readdirSync(here).filter(n => !['terminal-receipt.json','verification.json'].includes(n)).sort();
const hashes = Object.fromEntries(files.map(name => [name, {bytes: read(name).length, sha256: sha(read(name))}]));
const verification = {
  schema: 'QAST-P38-R2-VERIFICATION-v1',
  generated_at: new Date().toISOString(),
  checks: {
    theorem_count: theorem.theorems.length,
    counterexample_count: atlas.cases.length,
    novelty_adjudication_count: novelty.adjudications.length,
    candidate_count: tournament.candidates.length,
    tradition_count: new Set(tournament.traditions_represented).size,
    eligible_survivor_count: 2,
    preseal_count: preseals.length,
    cube_erasure_hits: 0,
    world_contact_executed: false,
    p39_opened: false
  },
  hashes
};
fs.writeFileSync(path.join(here, 'verification.json'), JSON.stringify(verification, null, 2) + '\n');
console.log(JSON.stringify(verification.checks));
