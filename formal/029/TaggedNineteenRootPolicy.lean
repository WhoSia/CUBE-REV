import FiftyTwoRootReceipt
import ElevenPrefix

namespace CubeRev029.Nineteen

open Eighteen

/-- A tagged edge address prevents the first-eleven sticker addresses
from being confused with the thirteen possible continuation addresses.
The Bool flag is TRUE for an original first sticker, and FALSE for
the sector continuation observation. These are different sensor channels
over one original complete oriented edge word. -/
abbrev TaggedEdgeAddress := Bool × Nat

def taggedEdgeObserve (word : Word) (query : TaggedEdgeAddress) : Nat :=
  if query.1 then sticker word[query.2]! false
  else observation word query.2

def firstElevenTagged : List TaggedEdgeAddress :=
  (List.range 11).map (fun i => (true, i))

theorem first_eleven_tagged_count :
    firstElevenTagged.length = 11 := by
  decide

theorem first_eleven_tagged_values (word : Word) :
    firstElevenTagged.map (taggedEdgeObserve word) =
      (List.range 11).map (fun i => sticker word[i]! false) := by
  simp [firstElevenTagged, taggedEdgeObserve]

/-- Lift a signed continuation to the tagged original edge channel.
The response is unchanged; only the address vocabulary is transformed.
In particular no future color or corner parity is passed to this map. -/
def taggedContinuation (tree : Policy Nat Nat (Bool → Option Word)) :
    Policy TaggedEdgeAddress Nat (Bool → Option Word) :=
  tree.adapt (fun address => (false, address))
    (fun _ reply => reply) id

theorem taggedContinuation_fits {tree : Policy Nat Nat (Bool → Option Word)}
    (bounded : Fits 8 tree) :
    Fits 8 (taggedContinuation tree) := by
  exact Policy.adapt_fits
    (fun address : Nat => (false, address))
    (fun (_ : Nat) (reply : Nat) => reply)
    id bounded

theorem taggedContinuation_run (tree : Policy Nat Nat (Bool → Option Word))
    (word : Word) :
    (taggedContinuation tree).run taggedEdgeObserve word =
      tree.run observation word := by
  simpa [taggedContinuation, taggedEdgeObserve] using
    (Policy.adapt_run (fun address : Nat => (false, address))
      (fun (_ : Nat) (reply : Nat) => reply)
      id taggedEdgeObserve word tree)

/-- Only a root whose recorded eleven-color prefix is EXACTLY the
observed one may be selected. A missing root remains a fail-closed
terminal; source acceptance will ensure all genuine representative
prefixes are present. This selector does not normalize arbitrary
original prefixes under the 48 color maps. -/
def rootFirstColors (entry : Lean.Json) : Option (List Nat) := do
  let prefix ← (entry.getObjVal? "prefix").toOption
  let literal ← prefix.getStr?.toOption
  some (literal.toList.map colorCode)

def matchingFrozenRoot (roots : Array Lean.Json) (answers : List Nat) :
    Option Lean.Json :=
  roots.toList.find? (fun entry => rootFirstColors entry == some answers)

/-- Exact 8-frame continuation when a matching 52-root representative
exists and is parseable; otherwise fail closed with no fabricated word. -/
def continuationFromFrozenRoots (roots : Array Lean.Json)
    (answers : List Nat) : Policy Nat Nat (Bool → Option Word) :=
  match matchingFrozenRoot roots answers with
  | none => .stop (fun _ => none)
  | some entry =>
      match parseRepresentativeRoot entry with
      | .error _ => .stop (fun _ => none)
      | .ok (graph, belief) =>
          exactEightSectorPolicy 0 graph observation edgeWordSign 0 belief

theorem continuation_from_frozen_roots_fits
    (roots : Array Lean.Json) (answers : List Nat) :
    Fits 8 (continuationFromFrozenRoots roots answers) := by
  unfold continuationFromFrozenRoots
  cases matchingFrozenRoot roots answers with
  | none => exact Fits.stop 8 _
  | some entry =>
      cases parseRepresentativeRoot entry with
      | error _ => exact Fits.stop 8 _
      | ok payload =>
          rcases payload with ⟨graph, belief⟩
          exact exact_eight_sector_fits 0 graph observation edgeWordSign
            0 belief

/-- An eleven-first-read, response-adaptive eight-read continuation.
All policy choices in the continuation are functions of the ACTUAL
ordered first-eleven answers; the terminal sign is not supplied here. -/
def elevenThenFrozen (roots : Array Lean.Json) :
    Policy TaggedEdgeAddress Nat (Bool → Option Word) :=
  Policy.withPrefix firstElevenTagged [] (fun answers =>
    taggedContinuation (continuationFromFrozenRoots roots answers))

theorem eleven_then_frozen_fits_nineteen (roots : Array Lean.Json) :
    Fits 19 (elevenThenFrozen roots) := by
  have within : ∀ replies,
      Fits 8 (taggedContinuation
        (continuationFromFrozenRoots roots replies)) := by
    intro replies
    exact taggedContinuation_fits
      (continuation_from_frozen_roots_fits roots replies)
  have bound := Policy.withPrefix_fits
    firstElevenTagged []
    (fun answers => taggedContinuation (continuationFromFrozenRoots roots answers))
    within
  simpa [first_eleven_tagged_count, elevenThenFrozen] using bound

/-- Global EXACT nineteen physical edge-side frames, even if the
observed prefix is absent or malformed. The fallback reads count
as real observations and never invent a successful reconstruction. -/
def exactNineteenTagged (roots : Array Lean.Json) :
    Policy TaggedEdgeAddress Nat (Bool → Option Word) :=
  (elevenThenFrozen roots).padToExact (true, 0) 19

theorem exact_nineteen_tagged_fits (roots : Array Lean.Json) :
    Fits 19 (exactNineteenTagged roots) := by
  exact Policy.padToExact_fits (true, 0)
    (eleven_then_frozen_fits_nineteen roots)

theorem exact_nineteen_tagged_transcript_length
    (roots : Array Lean.Json) (word : Word) :
    (Policy.transcript taggedEdgeObserve word
      (exactNineteenTagged roots)).length = 19 := by
  exact Policy.padToExact_transcript_length (true, 0)
    taggedEdgeObserve word (eleven_then_frozen_fits_nineteen roots)

/-- The canonicalized candidate's result after the *ordered first
eleven replies* is exactly the same eight-frame signed sector run.
This is the central nonanticipating composition equation. -/
theorem eleven_then_frozen_run (roots : Array Lean.Json)
    (word : Word) :
    (elevenThenFrozen roots).run taggedEdgeObserve word =
      (continuationFromFrozenRoots roots
        (firstElevenTagged.map (taggedEdgeObserve word))).run
          observation word := by
  unfold elevenThenFrozen
  rw [Policy.withPrefix_run]
  simpa using
    (taggedContinuation_run
      (continuationFromFrozenRoots roots
        (firstElevenTagged.map (taggedEdgeObserve word))) word)

/-- Exactly nineteen real tagged observations, with no leaked sign bit:
a parsed and selected actual root which contains the original candidate
returns that candidate after the final sign is provided. The promise
is restricted to a matching frozen REPRESENTATIVE prefix; the 1362
original count vectors still require signed symmetry normalization. -/
theorem exact_nineteen_tagged_recovers_matching_actual_root
    (roots : Array Lean.Json)
    (parsed : parsedRepresentativeArray
      (include_str "upper-policy-certificate.json") = .ok roots)
    (entry : Lean.Json) (member : entry ∈ roots.toList)
    (word : Word)
    (selected : matchingFrozenRoot roots
      (firstElevenTagged.map (taggedEdgeObserve word)) = some entry)
    (graph : Array (FrozenInstruction Nat Nat Unit))
    (belief : List Word)
    (entryParsed : parseRepresentativeRoot entry = .ok (graph, belief))
    (candidate : word ∈ belief) :
    ((exactNineteenTagged roots).run taggedEdgeObserve word)
      (edgeWordSign word) = some word := by
  have rootsCorrect := every_actual_frozen_root_recovers
    roots parsed entry member
  obtain ⟨g, b, matchEntry, allCorrect⟩ := rootsCorrect
  have same : (graph, belief) = (g, b) := by
    have e : Except.ok (graph, belief) = Except.ok (g, b) :=
      entryParsed.symm.trans matchEntry
    injection e with equal
    exact equal
  rcases Prod.mk.inj same with ⟨sameGraph, sameBelief⟩
  subst g
  subst b
  have exactCorrect := allCorrect word candidate
  rw [show (exactNineteenTagged roots).run taggedEdgeObserve word =
    (elevenThenFrozen roots).run taggedEdgeObserve word from
    Policy.padToExact_run (true, 0) taggedEdgeObserve word
      (eleven_then_frozen_fits_nineteen roots)]
  rw [eleven_then_frozen_run]
  simp only [continuationFromFrozenRoots, selected, matchEntry]
  exact exactCorrect

#print axioms first_eleven_tagged_count
#print axioms first_eleven_tagged_values
#print axioms taggedContinuation_fits
#print axioms taggedContinuation_run
#print axioms continuation_from_frozen_roots_fits
#print axioms eleven_then_frozen_fits_nineteen
#print axioms exact_nineteen_tagged_fits
#print axioms exact_nineteen_tagged_transcript_length
#print axioms eleven_then_frozen_run
#print axioms exact_nineteen_tagged_recovers_matching_actual_root

end CubeRev029.Nineteen
