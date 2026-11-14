#!/usr/bin/env python3
"""Replay the 19-frame edge policy when parity is disclosed at the last frame."""
from collections import Counter
import json

from audit_r14_p840_constructive_19_frame import COLORS, EdgeGame, transports


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


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
