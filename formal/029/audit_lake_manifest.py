#!/usr/bin/env python3
"""Fail-closed static package/CI preflight. Not a Lean kernel proof."""
from __future__ import annotations
import json
from pathlib import Path
import tomllib

ROOT=Path(__file__).resolve().parent
EXTERNAL={'Lean','Std'}
REQUIRED={
 'PhysicalEighteen','EighteenCertified','EighteenDataReceipt',
 'NineteenDataReceipt','NineteenReadData','NineteenSector',
 'PhysicalPolicyCompilerFast','CornerPairDecoder','NineteenSchedule',
 'CornerTurnGenerators','ReachableCornerCoordinates','CornerConservation',
 'ReachableCornerIdentification','CornerPermutation','NineteenCornerTranscript','ObservationTransport','ElevenPrefix','NineteenSymmetry','SymmetryWordTransport','LegalEdgeSymmetry','PairedPolicyTransport','SymmetryInverse','RepresentativeRoundTrip','ColorGraphCharacter','GraphPosteriorCovariance',
 'SignedRepresentativePolicy','SignedPairedPosterior','SignedTerminalIdentification','SignedPolicyTranscript','FrozenPolicyInterpreter','SignedSectorLeaf','SectorSemanticCompiler','FrozenJsonSectorParser','SectorStatewiseValidity','ExactBudgetPadding','ExactEightSector','ReflectedSectorChecker','DistinctReplyChecker','FrozenRootReflection','FiftyTwoRootReceipt','TaggedNineteenRootPolicy','PairedCornerClock'
}


def check():
    config=tomllib.loads((ROOT/'lakefile.toml').read_text())
    names=[obj['name'] for obj in config['lean_lib']]
    default=config['defaultTargets']
    assert len(default)==len(set(default)), 'Duplicate defaultTargets'
    assert len(names)==len(set(names)), 'Duplicate Lean lib declarations'
    assert set(default)==set(names), 'Lean libs must all be default build targets'
    assert REQUIRED <= set(names), 'Missing a primary formal theorem or bridge module'
    for x in names:
        assert (ROOT/f'{x}.lean').is_file(), f'Missing Lean module {x}'
    imports={}
    for name in names:
        path=ROOT/f'{name}.lean'
        imports[name]=[imp for line in path.read_text().splitlines()
                       if line.startswith('import ')
                       for imp in line[7:].split() if imp not in EXTERNAL]
        assert all(dep in names for dep in imports[name]),f'Missing import for {name}'
        if name in ('CornerTurnGenerators','ReachableCornerCoordinates','CornerConservation',
                 'ReachableCornerIdentification','CornerPermutation','NineteenCornerTranscript','ObservationTransport','ElevenPrefix','NineteenSymmetry','SymmetryWordTransport','LegalEdgeSymmetry','PairedPolicyTransport','SymmetryInverse','RepresentativeRoundTrip','ColorGraphCharacter','GraphPosteriorCovariance','SignedRepresentativePolicy','SignedPairedPosterior','SignedTerminalIdentification','SignedPolicyTranscript','FrozenPolicyInterpreter','SignedSectorLeaf','SectorSemanticCompiler','FrozenJsonSectorParser','SectorStatewiseValidity','ExactBudgetPadding','ExactEightSector','ReflectedSectorChecker','DistinctReplyChecker','FrozenRootReflection','FiftyTwoRootReceipt','TaggedNineteenRootPolicy','PairedCornerClock'):
            text=path.read_text()
            assert not any(token in text for token in ('sorry','admit','axiom ')),f'Unjustified placeholder in {name}'
    trace = (ROOT/'NineteenCornerTranscript.lean').read_text()
    for theorem in ('nineteen_schedule_contains_required_corner_pairs',
                    'same_scheduled_colors_implies_fourteen',
                    'same_nineteen_corner_answers_force_all_corner_colors'):
        assert f'theorem {theorem}' in trace, f'Missing nineteen-frame bridge theorem: {theorem}'
        assert f'#print axioms {theorem}' in trace, f'Missing axiom audit: {theorem}'
    transport = (ROOT/'ObservationTransport.lean').read_text()
    for theorem in ('Policy.run_fixed_reply_equiv', 'transport_certified_policy'):
        assert f'theorem {theorem}' in transport, f'Missing transport theorem: {theorem}'
        assert f'#print axioms {theorem}' in transport, f'Missing transport axiom audit: {theorem}'
    assert 'Policy.adapt_fits' in transport and 'Policy.adapt_run' in transport, (
        'Transport must explicitly preserve budget and observation semantics')
    prefix = (ROOT/'ElevenPrefix.lean').read_text()
    for theorem in ('Policy.withPrefix_fits','Policy.withPrefix_run',
                    'first_eleven_address_count',
                    'first_eleven_matches_frozen_corner_schedule',
                    'first_eleven_edge_addresses',
                    'nineteen_budget_of_eight_read_continuations'):
        assert f'theorem {theorem}' in prefix, f'Missing prefix theorem: {theorem}'
        assert f'#print axioms {theorem}' in prefix or (
            f'#print axioms CubeRev029.{theorem}' in prefix), (
            f'Missing kernel-axiom inspection: {theorem}')
    symmetry = (ROOT/'NineteenSymmetry.lean').read_text()
    for theorem in ('symmetry_preserves_edge_type_bijection',
                    'symmetry_even_flip_offset',
                    'symmetry_preserves_oriented_edge_colors'):
        assert f'theorem {theorem}' in symmetry, f'Missing color symmetry result: {theorem}'
        assert f'#print axioms {theorem}' in symmetry, f'Missing axiom audit: {theorem}'
    assert symmetry.count('decide +kernel') >= 3, (
        'All finite symmetry proofs must be kernel-computed, not native_decide')
    word_transport = (ROOT/'SymmetryWordTransport.lean').read_text()
    for theorem in ('relabelEdgeValue_label',
                    'relabelEdgeValue_flip',
                    'relabelEdgeWord_labels',
                    'relabelEdgeWord_flip_formula',
                    'symmetry_preserves_flipBit_for_all_complete_words',
                    'symmetry_relabelEdgeValue_responses'):
        assert f'theorem {theorem}' in word_transport, f'Missing word-transport theorem: {theorem}'
        assert f'#print axioms {theorem}' in word_transport, f'Missing axiom audit: {theorem}'
    for necessary in ('complete.map', 'symmetry_even_flip_offset', 'symmetry_preserves_oriented_edge_colors'):
        assert necessary in word_transport, f'Missing cubie legality or observation bridge: {necessary}'
    legal_transport = (ROOT/'LegalEdgeSymmetry.lean').read_text()
    for theorem in ('every_symmetry_is_an_edge_type_permutation',
                    'symmetry_relabels_any_complete_edge_permutation',
                    'complete_word_oriented_addresses_in_range',
                    'symmetry_relabels_word_observation_vector',
                    'symmetry_preserves_both_edge_legality_conditions',
                    'symmetry_relabels_both_edge_sticker_vectors'):
        assert f'theorem {theorem}' in legal_transport, (
            f'Missing whole-cube transport lemma: {theorem}')
        assert f'#print axioms {theorem}' in legal_transport, (
            f'Missing whole-cube transport axiom report: {theorem}')
    assert 'symmetry_preserves_flipBit_for_all_complete_words' in legal_transport
    assert 'every_symmetry_is_an_edge_type_permutation' in legal_transport
    paired = (ROOT/'PairedPolicyTransport.lean').read_text()
    for theorem in ('paired_response_equivariant',
                    'transportPairedPolicy_fits',
                    'transportPairedPolicy_run'):
        assert f'theorem {theorem}' in paired, f'Missing paired policy theorem: {theorem}'
        assert f'#print axioms {theorem}' in paired, f'Missing paired policy axiom audit: {theorem}'
    for need in ('Policy.run_fixed_reply_equiv',
                 'Policy.adapt_run', 'Policy.adapt_fits',
                 'symmetry_relabelEdgeValue_responses'):
        assert need in paired, f'Missing policy transport semantics or color bridge: {need}'
    inverse = (ROOT/'SymmetryInverse.lean').read_text()
    for theorem in ('inverse_color_table_is_symmetry',
                    'inverse_color_table_restores_center_code',
                    'inverse_color_table_restores_oriented_edge',
                    'oriented_edge_inverse_table_restores_forward'):
        assert f'theorem {theorem}' in inverse, f'Missing color inverse theorem: {theorem}'
        assert f'#print axioms {theorem}' in inverse, f'Missing color inverse axiom audit: {theorem}'
    assert inverse.count('decide +kernel') >= 4, 'Inverse table cannot rely on native_decide'
    roundtrip = (ROOT/'RepresentativeRoundTrip.lean').read_text()
    for theorem in ('representative_pair_state_round_trip',
                    'correct_original_policy_of_certified_representative'):
        assert f'theorem {theorem}' in roundtrip, f'Missing exact inverse-policy theorem: {theorem}'
        assert f'#print axioms {theorem}' in roundtrip, f'Missing inverse-policy axiom inspection: {theorem}'
    for need in ('inverse_color_table_restores_oriented_edge',
                 'transportPairedPolicy_run', 'transportPairedPolicy_fits'):
        assert need in roundtrip, f'Incomplete exact inverse policy proof: {need}'
    character = (ROOT/'ColorGraphCharacter.lean').read_text()
    for theorem in ('every_symmetry_permutes_opposite_pairs',
                    'induced_edge_sign_is_three_pair_sign',
                    'color_generators_are_valid_symmetries',
                    'cayley_six_steps_cover_all_color_symmetries'):
        assert f'theorem {theorem}' in character, f'Missing group character theorem: {theorem}'
        assert f'#print axioms {theorem}' in character, f'Missing group character axiom report: {theorem}'
    assert character.count('decide +kernel') >= 4, (
        'Graph character and Cayley certificates must use kernel computation')
    assert 'native_decide' not in character, 'Graph character cannot rely on native_decide'
    graph_posterior = (ROOT/'GraphPosteriorCovariance.lean').read_text()
    for theorem in ('transported_posterior_covariance',
                    'transported_belief_preserves_ambiguity',
                    'adversary_transport_across_equivariant_game'):
        assert f'theorem {theorem}' in graph_posterior, f'Missing graph posterior theorem: {theorem}'
        assert f'#print axioms {theorem}' in graph_posterior, f'Missing graph axiom report: {theorem}'
    for necessary in ('replyInjective', 'everyTargetQuery', 'posterior sourceObserve'):
        assert necessary in graph_posterior, f'Missing causal game symmetry condition: {necessary}'
    signed_policy = (ROOT/'SignedRepresentativePolicy.lean').read_text()
    for theorem in ('signed_representative_round_trip',
                    'signed_paired_reply_equivariant',
                    'signed_original_policy_of_certified_representative'):
        assert f'theorem {theorem}' in signed_policy, (
            f'Missing signed gauge theorem: {theorem}')
        assert f'#print axioms {theorem}' in signed_policy, (
            f'Missing signed gauge axiom report: {theorem}')
    for checkpoint in ('Bool.xor','transport_certified_policy',
                       'signedRealPairRead','signedRepresentativePairRead'):
        assert checkpoint in signed_policy, (
            f'Missing signed policy semantic guard: {checkpoint}')
    signed_posterior = (ROOT/'SignedPairedPosterior.lean').read_text()
    for theorem in ('signed_representative_encode_injective',
                    'signed_paired_posterior_one_step',
                    'signed_paired_posterior_all_histories',
                    'signed_ambiguity_survives_normalization'):
        assert f'theorem {theorem}' in signed_posterior, (
            f'Missing signed posterior theorem: {theorem}')
        assert f'#print axioms {theorem}' in signed_posterior, (
            f'Missing signed posterior axiom report: {theorem}')
    for checkpoint in ('List (PairedAddress12 × PairedReply12)',
                       'posterior signedRepresentativePairRead',
                       'transported_posterior_covariance',
                       'signed_representative_encode_injective'):
        assert checkpoint in signed_posterior, (
            f'Missing ordered signed posterior semantic gate: {checkpoint}')
    terminal = (ROOT/'SignedTerminalIdentification.lean').read_text()
    for theorem in ('exactly_one_iff_transported_belief',
                    'signed_terminal_singleton_iff_after_any_history',
                    'unconstrained_parity_tag_is_unobservable',
                    'cannot_recover_an_independent_parity_oracle'):
        assert f'theorem {theorem}' in terminal, (
            f'Missing signed terminal theorem: {theorem}')
        assert f'#print axioms {theorem}' in terminal, (
            f'Missing terminal axiom print: {theorem}')
    for item in ('beliefExactlyOne', 'Bool',
                 'signed_paired_posterior_all_histories',
                 'Policy.run_fixed_reply_equiv'):
        assert item in terminal, f'No-free-parity model gate omitted: {item}'
    signed_trace=(ROOT/'SignedPolicyTranscript.lean').read_text()
    for theorem in ('transported_signed_transcript_preserves_budget',
                    'transported_signed_policy_transcript_exact'):
        assert f'theorem {theorem}' in signed_trace, (
            f'Missing adaptive signed transcript theorem: {theorem}')
        assert f'#print axioms {theorem}' in signed_trace, (
            f'Missing signed transcript axiom inspection: {theorem}')
    for checkpoint in ('Policy.adapt_fits', 'Policy.logged_fits',
                       'Policy.run_fixed_reply_equiv',
                       'signed_paired_reply_equivariant', 'Policy.logged_run'):
        assert checkpoint in signed_trace, (
            f'Missing causal policy trace premise: {checkpoint}')
    interpreter=(ROOT/'FrozenPolicyInterpreter.lean').read_text()
    for theorem in ('frozen_policy_has_total_budget',
                    'exact_leaf_at_zero_budget',
                    'empty_graph_rejects'):
        assert f'theorem {theorem}' in interpreter, (
            f'Missing typed frozen-policy proof: {theorem}')
        assert f'#print axioms {theorem}' in interpreter, (
            f'Missing frozen-policy axiom report: {theorem}')
    for checkpoint in ('inductive FrozenInstruction',
                       'compileFrozenPolicy', 'Fits.read', 'Fits.stop',
                       'Option O', 'Policy.stop none'):
        assert checkpoint in interpreter, (
            f'Missing fail-closed certificate interpreter guard: {checkpoint}')
    sector_leaf=(ROOT/'SignedSectorLeaf.lean').read_text()
    for theorem in ('first_candidate_is_correct_of_sign_unique',
                    'first_candidate_witness_belongs'):
        assert f'theorem {theorem}' in sector_leaf, f'Missing exact sign-sector theorem {theorem}'
        assert f'#print axioms {theorem}' in sector_leaf, f'Missing sign-sector axiom report {theorem}'
    for checkpoint in ('AtMostOnePerSign', 'firstCandidateWithSign'):
        assert checkpoint in sector_leaf, f'Missing sign-sector semantics {checkpoint}'
    sector_compiler=(ROOT/'SectorSemanticCompiler.lean').read_text()
    for theorem in ('finite_reply_fiber_mem',
                    'compiled_sector_fits_all_replies',
                    'valid_sector_compilation_recovers_each_candidate'):
        assert f'theorem {theorem}' in sector_compiler, (
            f'Missing finite sector semantics theorem: {theorem}')
        assert f'#print axioms {theorem}' in sector_compiler, (
            f'Missing finite sector axiom report: {theorem}')
    for checkpoint in ('SemanticallyValidSector', 'AtMostOnePerSign',
                       'finiteReplyFiber', 'firstCandidateWithSign',
                       'compileSectorDecoder', 'Fits.read'):
        assert checkpoint in sector_compiler, (
            f'Missing sign-deferred certificate semantic guard: {checkpoint}')
    frozen_json=(ROOT/'FrozenJsonSectorParser.lean').read_text()
    for theorem in ('exact_frozen_leaf_parse',
                    'malformed_singleton_is_rejected',
                    'parsed_sector_has_bounded_policy'):
        assert f'theorem {theorem}' in frozen_json, (
            f'Missing exact frozen parser theorem {theorem}')
        assert f'#print axioms {theorem}' in frozen_json, (
            f'Missing frozen parser axiom report {theorem}')
    for checkpoint in ('parseFrozenSectorNode', 'parseFrozenSectorNodes',
                       'Invalid singleton node tag.', 'Unexpected color response label.',
                       'Out-of-range sector address.', 'compileSectorDecoder',
                       'invalidIndex'):
        assert checkpoint in frozen_json, (
            f'Missing fail-closed frozen schema gate: {checkpoint}')
    statewise=(ROOT/'SectorStatewiseValidity.lean').read_text()
    for theorem in ('statewise_sector_valid_iff_semantic',
                    'statewise_checked_sector_recovers_each_candidate'):
        assert f'theorem {theorem}' in statewise, (
            f'Missing finite-statewise sector equivalence: {theorem}')
        assert f'#print axioms {theorem}' in statewise, (
            f'Missing statewise certificate axiom inspection: {theorem}')
    for evidence in ('StatewiseSectorValid','SemanticallyValidSector',
                     'finiteReplyFiber','observe state q'):
        assert evidence in statewise, f'Missing exact belief audit: {evidence}'
    exact_pad=(ROOT/'ExactBudgetPadding.lean').read_text()
    for theorem in ('Policy.padToExact_fits',
                    'Policy.padToExact_run',
                    'Policy.padToExact_transcript_length'):
        assert f'theorem {theorem}' in exact_pad, (
            f'Missing exact nineteen-frame padding theorem {theorem}')
        assert f'#print axioms {theorem}' in exact_pad, (
            f'Missing exact padding axiom report {theorem}')
    for checkpoint in ('Policy.padToExact','Policy.transcript',
                       'Fits.read', 'Policy.run'):
        assert checkpoint in exact_pad, (
            f'Padding cannot be a free observation: {checkpoint}')
    eight=(ROOT/'ExactEightSector.lean').read_text()
    for theorem in ('exact_eight_sector_fits',
                    'exact_eight_sector_trace_length',
                    'exact_eight_sector_recovers_given_terminal_sign'):
        assert f'theorem {theorem}' in eight, (
            f'Missing exact-eight sector theorem {theorem}')
        assert f'#print axioms {theorem}' in eight, (
            f'Missing exact-eight sector axiom report {theorem}')
    for premise in ('StatewiseSectorValid', 'Policy.padToExact_run',
                    'statewise_checked_sector_recovers_each_candidate',
                    'compileSectorDecoder'):
        assert premise in eight, f'Missing causal exact-eight sector premise {premise}'
    reflected=(ROOT/'ReflectedSectorChecker.lean').read_text()
    for theorem in ('allFinite_true_implies_every_member',
                    'checkSignUnique_sound',
                    'checkFiniteSector_sound',
                    'checked_eight_sector_recovers',
                    'opposite_sign_leaf_accepted',
                    'same_sign_leaf_rejected'):
        assert f'theorem {theorem}' in reflected, (
            f'Missing reflected finite checker theorem {theorem}')
        assert f'#print axioms {theorem}' in reflected, (
            f'Missing reflected checker axiom report {theorem}')
    for premise in ('allFinite', 'checkSignUnique',
                    'StatewiseSectorValid', 'checkFiniteSector',
                    'finiteReplyFiber', 'exactEightSectorPolicy',
                    'decide +kernel'):
        assert premise in reflected, f'Reflected checker proof gate missing: {premise}'
    distinct=(ROOT/'DistinctReplyChecker.lean').read_text()
    for theorem in ('own_reply_is_attainable',
                    'checkDistinctSector_sound',
                    'checked_distinct_eight_sector_recovers',
                    'distinct_reply_split_accepts_two_same_sign_states',
                    'unresolved_same_sign_leaf_is_rejected'):
        assert f'theorem {theorem}' in distinct, (
            f'Missing fast distinct-reply reflection: {theorem}')
        assert f'#print axioms {theorem}' in distinct, (
            f'Missing fast checker axiom inspection: {theorem}')
    for feature in ('eraseDups','LawfulBEq', 'StatewiseSectorValid',
                    'checkSignUnique', 'finiteReplyFiber', 'allFinite',
                    'decide +kernel'):
        assert feature in distinct, f'Missing exact finite reply semantics {feature}'
    frozen_roots=(ROOT/'FrozenRootReflection.lean').read_text()
    for theorem in ('certified_source_each_root_has_exact_semantics',
                    'certified_source_each_root_recovers'):
        assert f'theorem {theorem}' in frozen_roots, (
            f'Missing original JSON root/semantic soundness: {theorem}')
        assert f'#print axioms {theorem}' in frozen_roots, (
            f'Missing frozen-root axiom inspection: {theorem}')
    for gate in ('parsedRepresentativeArray', 'parseRepresentativeRoot',
                 'sector (List.range 12) 0 firstCodes', 'checkDistinctSector_sound',
                 'allFinite checkedRepresentativeRoot',
                 'certifiedFrozenRoots', '144736', '141097', '70774'):
        assert gate in frozen_roots, f'Missing frozen 52-root exactness gate {gate}'
    frozen_52=(ROOT/'FiftyTwoRootReceipt.lean').read_text()
    for theorem in ('fifty_two_frozen_roots_semantically_accepted',
                    'every_actual_frozen_root_recovers'):
        assert f'theorem {theorem}' in frozen_52, (
            f'Missing semantic 52-root receipt: {theorem}')
        assert f'#print axioms {theorem}' in frozen_52, (
            f'Missing 52-root axiom trust report: {theorem}')
    for anchor in ('include_str "upper-policy-certificate.json"',
                   'certifiedFrozenRoots immutableUpperSource',
                   'native_decide', 'certified_source_each_root_recovers'):
        assert anchor in frozen_52, f'Missing immutable exact 52-root link: {anchor}'
    tagged=(ROOT/'TaggedNineteenRootPolicy.lean').read_text()
    for theorem in ('first_eleven_tagged_count', 'first_eleven_tagged_values',
                    'taggedContinuation_fits', 'taggedContinuation_run',
                    'continuation_from_frozen_roots_fits',
                    'eleven_then_frozen_fits_nineteen',
                    'exact_nineteen_tagged_fits',
                    'exact_nineteen_tagged_transcript_length',
                    'eleven_then_frozen_run',
                    'exact_nineteen_tagged_recovers_matching_actual_root'):
        assert f'theorem {theorem}' in tagged, f'Missing nineteen-frame tagged theorem {theorem}'
        assert f'#print axioms {theorem}' in tagged, f'Missing tagged nineteen-frame axiom check {theorem}'
    for premise in ('FiftyTwoRootReceipt','matchingFrozenRoot',
                    'exactEightSectorPolicy','Policy.withPrefix_run',
                    'Policy.padToExact_transcript_length',
                    'every_actual_frozen_root_recovers'):
        assert premise in tagged, f'Missing frozen-root tagged proof premise: {premise}'
    clock=(ROOT/'PairedCornerClock.lean').read_text()
    for theorem in ('withCornerClock_fits','withCornerClock_run',
                    'observed_corner_addresses_eq_schedule',
                    'exact_nineteen_paired_roots_fits',
                    'exact_nineteen_paired_roots_corner_addresses',
                    'exact_nineteen_paired_roots_run',
                    'final_corner_sticker_is_nineteenth_paired_read',
                    'exact_nineteen_paired_recovers_matching_actual_root',
                    'observed_corner_colors_eq_schedule',
                    'exact_nineteen_paired_roots_corner_colors',
                    'exact_nineteen_paired_corner_colors_match_colorings',
                    'same_paired_corner_colors_force_all_legal_corners'):
        assert f'theorem {theorem}' in clock, f'Missing charged-corner clock theorem {theorem}'
        assert f'#print axioms {theorem}' in clock, f'Missing paired-clock axiom audit {theorem}'
    for anchor in ('cornerFrameAddresses', 'taggedPairedObserve',
                   'response.1', 'exactNineteenTagged',
                   'final_corner_color_not_early', 'Policy.transcript'):
        assert anchor in clock, f'Missing paired corner-clock causal guard: {anchor}'
    visiting=set();visited=set()
    def visit(x):
        if x in visiting:raise ValueError(f'Import cycle at {x}')
        if x in visited:return
        visiting.add(x)
        for y in imports[x]:visit(y)
        visiting.remove(x);visited.add(x)
    for name in names:visit(name)
    workflow=(ROOT.parents[1]/'.github/workflows/cuberev029-lean.yml').read_text()
    assert 'contents: read' in workflow
    assert 'persist-credentials: false' in workflow
    steps=['restore_pinned_data.py','validate_19_corner_schedule.py',
           'audit_corner_turn_generators.py','audit_reachable_corner_bridge.py',
           'lake-package-directory: formal/029']
    assert all(s in workflow for s in steps)
    hall_script=(ROOT.parents[1]/'scripts/cuberev-observation/audit_r029_hall_burnside_graph_quotient.py').read_text()
    for claim in ('four_hall_families','independent_family_failures',
                  'hall_fast','independent_dp','burnside_fix_sum',
                  'odd_character_stabilizer_orbits','signed_histogram_orbits',
                  'signed_character_burnside','even_fix==2256',
                  'unsafe_orbits,unsafe_vectors',
                  'stable_sort_cocycle_checks','full_gauge_unsafe_orbits',
                  'full_gauge_unsafe_vectors',
                  'full_correction_signed_histogram_orbits',
                  'full_correction_burnside','corrected_fixed_even',
                  'signed_normalized_orbits'):
        assert claim in hall_script, f'Missing graph-Hall independent gate: {claim}'
    assert 'audit_r029_hall_burnside_graph_quotient.py' in workflow, (
        'Actual read-only CI must run the graph quotient and Hall mutations')
    gauge_script=(ROOT.parents[1]/'scripts/cuberev-observation/audit_r029_gauge_counterexample.py').read_text()
    for checkpoint in ('build_legal_edge_word','is_edge_flip_even',
                       'normalized_sign_with_alternate_gauge',
                       'incorrectly_recovered!=original_sign',
                       'correctly_recovered==original_sign'):
        assert checkpoint in gauge_script, (
            f'Missing physical-edge gauge-loss negative control: {checkpoint}')
    assert 'audit_r029_gauge_counterexample.py' in workflow, (
        'Read-only CI must replay a legal-edge gauge-forgetting counterexample')
    return {'status':'PASS','lean_modules':len(names),
            'import_edges':sum(map(len,imports.values())),
            'primary_theorems_in_default_build':True,
            'read_only_ci':True,
            'scope':'Static dependency and workflow audit, not Lean compilation'}

if __name__=='__main__':print(json.dumps(check(),indent=2))
