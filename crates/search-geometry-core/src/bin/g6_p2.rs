use search_geometry_core::g6::{
    rotate_action_c4, Cube, Face, Move, Phase1, Phase1Moves, Phase1Pdb, COSET_COUNT, HTM,
};
use std::collections::{HashMap, HashSet, VecDeque};

fn main() {
    let moves = Phase1Moves::build();
    let pdb = Phase1Pdb::build(&moves);
    let id = Cube::SOLVED;
    let q0 = id.phase1();
    assert_eq!(COSET_COUNT, 2_217_093_120);
    assert!(q0.is_g1());
    assert_eq!(moves.next(q0, 0), q0);
    assert_eq!(moves.next(q0, 9), q0);
    assert_eq!(pdb.lower_bound(q0), 0);

    // Full-solve policy witness: U and D are distinct states inside one phase-1 coset.
    let u = id.apply(Move {
        face: Face::U,
        power: 1,
    });
    let d = id.apply(Move {
        face: Face::D,
        power: 1,
    });
    assert_eq!(u.phase1(), d.phase1());
    assert_eq!(u.phase1(), q0);
    let pi_u = (0..18)
        .filter(|&a| u.apply(HTM[a]).is_solved())
        .collect::<Vec<_>>();
    let pi_d = (0..18)
        .filter(|&a| d.apply(HTM[a]).is_solved())
        .collect::<Vec<_>>();
    assert_eq!(pi_u, vec![2]);
    assert_eq!(pi_d, vec![11]);

    // C4 around the U-D axis preserves G1 generator membership and relabels HTM actions.
    let g1_actions = (0..18)
        .filter(|&a| {
            let mv = HTM[a];
            matches!(mv.face, Face::U | Face::D) || (mv.power == 2)
        })
        .collect::<Vec<_>>();
    for &a in &g1_actions {
        assert!(g1_actions.contains(&rotate_action_c4(a)));
    }

    // A local full-state BFS records exact distances only through depth 3.
    let mut dist = HashMap::new();
    let mut queue = VecDeque::new();
    dist.insert(id, 0u8);
    queue.push_back(id);
    while let Some(c) = queue.pop_front() {
        let depth = dist[&c];
        if depth == 3 {
            continue;
        }
        for &mv in &HTM {
            let n = c.apply(mv);
            if !dist.contains_key(&n) {
                dist.insert(n, depth + 1);
                queue.push_back(n);
            }
        }
    }
    for (&c, &exact_local) in &dist {
        assert!(c.validate());
        assert!(
            pdb.lower_bound(c.phase1()) <= exact_local,
            "projected phase-1 bound cannot exceed full-cube distance in the local ball"
        );
    }
    // Exhaustively test the coordinate transition oracle over the radius-3 full-state ball.
    for c in dist.keys() {
        for action in 0..18 {
            assert_eq!(
                moves.next(c.phase1(), action),
                c.apply(HTM[action]).phase1(),
                "coordinate transition mismatch at {c:?}, action {action}"
            );
        }
    }

    // Exact Schreier and full-state breadth-first balls, both through radius 5.
    let mut qdist = HashMap::new();
    let mut qqueue = VecDeque::new();
    qdist.insert(q0, 0u8);
    qqueue.push_back(q0);
    while let Some(q) = qqueue.pop_front() {
        let depth = qdist[&q];
        if depth == 5 {
            continue;
        }
        for action in 0..18 {
            let next = moves.next(q, action);
            if !qdist.contains_key(&next) {
                qdist.insert(next, depth + 1);
                qqueue.push_back(next);
            }
        }
    }

    let mut full = HashMap::new();
    let mut path_codes = HashMap::new();
    let mut order = Vec::new();
    let mut full_queue = VecDeque::new();
    full.insert(id, 0u8);
    path_codes.insert(id, 0u32);
    order.push(id);
    full_queue.push_back(id);
    while let Some(c) = full_queue.pop_front() {
        let depth = full[&c];
        if depth == 5 {
            continue;
        }
        for (action, &mv) in HTM.iter().enumerate() {
            let next = c.apply(mv);
            if !full.contains_key(&next) {
                let code = path_codes[&c] * 18 + action as u32;
                full.insert(next, depth + 1);
                path_codes.insert(next, code);
                order.push(next);
                full_queue.push_back(next);
            }
        }
    }
    let distortion_witness = order.iter().find_map(|c| {
        let dg = full[c];
        qdist
            .get(&c.phase1())
            .filter(|&&d1| d1 != dg)
            .map(|&d1| (*c, dg, d1))
    });
    let path_for = |c: &Cube| {
        let mut code = path_codes[c];
        let mut path = vec![0usize; full[c] as usize];
        for i in (0..path.len()).rev() {
            path[i] = (code % 18) as usize;
            code /= 18;
        }
        path
    };

    // At d1=1, enumerate every first-hit endpoint. Same q gives the same action labels,
    // while omitted permutations may make the full G1 entry endpoints differ.
    let mut entries_by_q: HashMap<Phase1, (Cube, HashSet<Cube>)> = HashMap::new();
    let mut entry_witness = None;
    for c in &order {
        let qx = c.phase1();
        if qdist.get(&qx) != Some(&1) {
            continue;
        }
        let endpoints = (0..18)
            .map(|a| c.apply(HTM[a]))
            .filter(|end| end.phase1().is_g1())
            .collect::<HashSet<_>>();
        if endpoints.is_empty() {
            continue;
        }
        if let Some((prior, prior_endpoints)) = entries_by_q.get(&qx) {
            if prior_endpoints != &endpoints {
                entry_witness = Some((*prior, *c, prior_endpoints.len(), endpoints.len()));
                break;
            }
        } else {
            entries_by_q.insert(qx, (*c, endpoints));
        }
    }

    // Apply a physical U-D-axis C4 rotation to deterministic move words.
    let symmetry_probe = [0usize, 4, 8, 9, 13, 16, 2, 6];
    let mut state = Cube::SOLVED;
    let mut rotated = Cube::SOLVED;
    for action in symmetry_probe {
        state = state.apply(HTM[action]);
        rotated = rotated.apply(HTM[rotate_action_c4(action)]);
        assert_eq!(state.phase1().is_g1(), rotated.phase1().is_g1());
        assert_eq!(
            pdb.lower_bound(state.phase1()),
            pdb.lower_bound(rotated.phase1())
        );
    }

    println!("G6_P2_LOCAL_COURT_PASS");
    println!("ACTION_GRAMMAR\t18 HTM");
    println!("PHASE1_COORDINATE_TRANSITIONS\t3 component tables × 18 actions");
    println!("SCHREIER_VERTICES\t{COSET_COUNT}");
    println!("SCHREIER_GRAPH\tDEFINITION_AND_ORACLE; NOT FULLY MATERIALIZED");
    println!(
        "PDB_TWIST_SLICE\t{} entries; exact projected distances",
        pdb.twist_slice.len()
    );
    println!(
        "PDB_FLIP_SLICE\t{} entries; exact projected distances",
        pdb.flip_slice.len()
    );
    println!("PDB_CONTRACT\tadmissible lower bound to G1; not exact full phase-1 distance");
    println!("FULL_POLICY_COLLISION\tq=G1: U state Pi={{U'}}, D state Pi={{D'}}");
    println!(
        "LOCAL_FULL_STATE_BALL\t{} states; exact HTM distance through depth 3",
        dist.len()
    );
    println!(
        "SCHREIER_LOCAL_BALL\t{} vertices; exact distance through radius 5",
        qdist.len()
    );
    println!(
        "FULL_LOCAL_BALL\t{} states; exact HTM distance through radius 5",
        full.len()
    );
    match distortion_witness {
        Some((c, dg, d1)) => println!(
            "PHASE_DISTORTION_WITNESS\tdG={dg}; d1={d1}; q={:?}; scramble={:?}",
            c.phase1(),
            path_for(&c)
        ),
        None => println!("PHASE_DISTORTION_WITNESS\tNONE_IN_INTERSECTION_OF_RADIUS_5_BALLS"),
    }
    match entry_witness {
        Some((a, b, na, nb)) => println!(
            "ENTRY_SURFACE_COLLISION\tq={:?}; endpoint-counts={na},{nb}; scrambles={:?}|{:?}",
            a.phase1(),
            path_for(&a),
            path_for(&b)
        ),
        None => println!("ENTRY_SURFACE_COLLISION\tNONE_FOUND_IN_RADIUS_5_LOCAL_BALL"),
    }
    println!("SYMMETRY\tC4 U-D-axis preserves G1 and projected PDB on deterministic word probe");
    println!("FULL_3X3_ENUMERATION\tNOT RUN");
}

#[cfg(test)]
mod tests {
    use super::*;
    use search_geometry_core::g6::Phase1;

    #[test]
    fn htm_generators_are_legal_and_inverse_consistent() {
        use search_geometry_core::g6::inverse_action;
        for (a, &mv) in HTM.iter().enumerate() {
            let once = Cube::SOLVED.apply(mv);
            assert!(once.validate());
            let inverse = HTM[inverse_action(a)];
            assert_eq!(once.apply(inverse), Cube::SOLVED);
            if mv.power == 2 {
                assert_eq!(once.apply(mv), Cube::SOLVED);
            }
            let mut x = Cube::SOLVED;
            for _ in 0..4 {
                x = x.apply(Move {
                    face: mv.face,
                    power: 1,
                });
            }
            assert_eq!(x, Cube::SOLVED);
        }
    }

    #[test]
    fn phase1_oracle_matches_full_cubie_transitions() {
        let tables = Phase1Moves::build();
        let mut c = Cube::SOLVED;
        let sequence = [0, 4, 8, 9, 13, 16, 2, 6, 11, 14];
        for a in sequence {
            let q = c.phase1();
            assert_eq!(tables.next(q, a), c.apply(HTM[a]).phase1());
            c = c.apply(HTM[a]);
        }
    }

    #[test]
    fn g1_generators_and_phase_target_are_exact() {
        let tables = Phase1Moves::build();
        for a in 0..18 {
            let mv = HTM[a];
            let should_be_g1 = matches!(mv.face, Face::U | Face::D) || mv.power == 2;
            assert_eq!(Cube::SOLVED.apply(mv).phase1().is_g1(), should_be_g1);
            if should_be_g1 {
                assert!(tables
                    .next(
                        Phase1 {
                            twist: 0,
                            flip: 0,
                            slice: 0
                        },
                        a
                    )
                    .is_g1());
            }
        }
    }

    #[test]
    fn static_phase_coordinate_does_not_determine_full_optimal_policy() {
        let u = Cube::SOLVED.apply(Move {
            face: Face::U,
            power: 1,
        });
        let d = Cube::SOLVED.apply(Move {
            face: Face::D,
            power: 1,
        });
        assert_eq!(u.phase1(), d.phase1());
        let pi_u = (0..18)
            .filter(|&a| u.apply(HTM[a]).is_solved())
            .collect::<Vec<_>>();
        let pi_d = (0..18)
            .filter(|&a| d.apply(HTM[a]).is_solved())
            .collect::<Vec<_>>();
        assert_ne!(pi_u, pi_d);
    }
}
