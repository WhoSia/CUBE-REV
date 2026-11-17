#!/usr/bin/env python3
"""Replay the 19-frame edge policy when parity is disclosed at the last frame."""
import argparse
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import json

from audit_r14_p840_constructive_19_frame import (
    C, COLORS, E, EdgeGame, parity, prefix_count, transports,
)


def audit():
    prefix_transports, _ = transports()
    representatives = sorted({rep for rep, _ in prefix_transports.values()})
    without_sign_failures = {}
    final_color_group_sizes = Counter()
    stopping_frames = Counter()

    for counts in representatives:
        prefix = ''.join(color * count for color, count in zip(COLORS, counts))
        game = EdgeGame(prefix)
        # Delay 9 lies outside the eight remaining frames.
        if game.action(game.full, 8, 9) is None:
            without_sign_failures[prefix] = len(game.words)
        assert game.action(game.full, 8, 8) is not None, prefix

        for word, sign in game.words:
            belief = game.full
            for frame in range(12, 20):
                remaining = 20 - frame
                query = game.action(belief, remaining, remaining)
                assert query is not None and query != -1
                belief = game.step(belief, query, word[query])
                if frame == 19:
                    final_color_group_sizes[belief.bit_count()] += 1
                    belief &= game.signs[sign]
                if belief.bit_count() == 1:
                    assert game.words[belief.bit_length() - 1] == (word, sign)
                    stopping_frames[frame] += 1
                    break
            else:
                raise AssertionError((prefix, word, sign))
        game.action.cache_clear()

    assert len(representatives) == 52
    assert sum(stopping_frames.values()) == 144736
    assert set(final_color_group_sizes) <= {1, 2}
    assert "RFFDDLLLBBB" in without_sign_failures
    return {
        "representatives": len(representatives),
        "edge_assignments": sum(stopping_frames.values()),
        "edge_identification_frames": dict(sorted(stopping_frames.items())),
        "final_color_group_sizes": dict(sorted(final_color_group_sizes.items())),
        "eight_queries_without_sign_failures": without_sign_failures,
    }


def physical_witness():
    """Return a two-candidate physical replay with a nonzero sign offset."""
    with redirect_stdout(StringIO()):
        import audit_r14_p51_p48_group_lift as physical

    edges = tuple(physical.PIECES[p] for p in physical.EDGES)
    corners = tuple(physical.PIECES[p] for p in physical.CORNERS)
    assert tuple(''.join(physical.COLORS[s] for s in piece) for piece in edges) == E
    assert tuple(''.join(physical.COLORS[s] for s in piece) for piece in corners) == C
    addresses = {
        slot: f"{label}[{side + 1}]"
        for labels, pieces in ((E, edges), (C, corners))
        for label, piece in zip(labels, pieces)
        for side, slot in enumerate(piece)
    }
    corner_schedule = [s for piece in corners[:7] for s in piece[:2]]
    corner_schedule = corner_schedule[:13] + [corner_schedule[0]] * 5 + corner_schedule[13:]
    corner_code = {
        word[rot] + word[(rot + 1) % 3]: (src, rot)
        for src, word in enumerate(C) for rot in range(3)
    }
    prefix_transports, maps = transports()
    games = {}

    for sample, state in enumerate(physical.states):
        def read(edge, frame):
            corner = corner_schedule[frame - 1]
            pair = (edge, corner)
            moves = physical.seen[pair]
            forward = physical.EYE
            for move in moves:
                forward = physical.compose(physical.MOVES[move], forward)
            backward = physical.inverse(forward)
            assert tuple(backward[s] for s in pair) == physical.q0
            replies = physical.obs(physical.compose(backward, state), physical.q0)
            return replies, moves

        early = [read(piece[0], frame)[0] for frame, piece in enumerate(edges[:11], 1)]
        prefix = ''.join(edge_color for edge_color, _ in early)
        rep, map_index = prefix_transports[prefix_count(prefix)]
        relabel, _, source_sign, _ = maps[map_index]
        order = sorted(range(11), key=lambda i: COLORS.index(relabel[prefix[i]])) + [11]
        sign_offset = parity(order) ^ source_sign
        if (not sign_offset or all(a == b for a, b in relabel.items())
                or order == list(range(12))):
            continue
        canonical_prefix = ''.join(relabel[prefix[i]] for i in order[:11])
        if rep not in games:
            games[rep] = EdgeGame(canonical_prefix)
        game = games[rep]
        slots = [edges[i][1] for i in order[:11]] + list(edges[11])
        belief = game.full
        trace = []
        corner_replies = [reply for _, reply in early]

        for frame in range(12, 20):
            remaining = 20 - frame
            query = game.action(belief, remaining, remaining)
            assert query is not None
            if query == -1:
                break
            edge = slots[query] if query >= 0 else edges[0][0]
            (edge_color, corner_color), route = read(edge, frame)
            canonical_color = relabel[edge_color]
            corner_replies.append(corner_color)
            belief = game.step(belief, query, canonical_color)
            trace.append({
                "frame": frame, "representative_slot_zero_based": query,
                "edge": addresses[edge], "corner": addresses[corner_schedule[frame - 1]],
                "edge_color": edge_color, "corner_color": corner_color,
                "representative_color": canonical_color,
                "candidates_before_sign": belief.bit_count(),
                "forward_route_from_probes_to_addresses": route,
            })
        else:
            if belief.bit_count() != 2:
                continue
            decoded = [corner_code[''.join(corner_replies[i:i + 2])]
                       for i in range(0, 12, 2)] + [
                           corner_code[corner_replies[12] + corner_replies[18]]
                       ]
            perm = [src for src, _ in decoded]
            twists = [rotation for _, rotation in decoded]
            assert len(set(perm)) == 7
            perm.append(next(src for src in range(8) if src not in perm))
            twists.append(-sum(twists) % 3)
            corner_sign = parity(perm)
            sign = corner_sign ^ sign_offset
            terminal = [entry for i, entry in enumerate(game.words) if belief & (1 << i)]
            assert sorted(s for _, s in terminal) == [0, 1]
            belief &= game.signs[sign]
            assert belief.bit_count() == 1
            word, _ = game.words[belief.bit_length() - 1]
            inverse_color = {b: a for a, b in relabel.items()}
            recovered = {edge[0]: color for edge, color in zip(edges, prefix)}
            recovered.update((slot, inverse_color[color]) for slot, color in zip(slots, word))
            recovered.update({
                slot: C[src][(shift + i) % 3]
                for piece, src, shift in zip(corners, perm, twists)
                for i, slot in enumerate(piece)
            })
            inv = physical.inverse(state)
            assert len(recovered) == 48
            assert all(color == physical.COLORS[inv[slot]] for slot, color in recovered.items())
            return {
                "sample_index": sample, "prefix": prefix,
                "representative_prefix": canonical_prefix, "colors": relabel,
                "representative_edge_order": [E[i] for i in order],
                "fixed_probes": [addresses[s] for s in physical.q0],
                "trace": trace, "terminal_words_and_signs": terminal,
                "corner_permutation": [C[i] for i in perm],
                "physical_corner_sign": corner_sign, "position_sign": parity(order),
                "label_sign": source_sign, "representative_sign": sign,
                "recovered_moving_stickers": len(recovered),
            }
    raise AssertionError("No two-candidate physical witness found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--physical-witness", action="store_true",
                        help="replay a named physical witness through the final sign")
    args = parser.parse_args()
    print(json.dumps(physical_witness() if args.physical_witness else audit(), indent=2))
