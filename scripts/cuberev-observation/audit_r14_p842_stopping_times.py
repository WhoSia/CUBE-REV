#!/usr/bin/env python3
"""Count P8.40 and prefix-minimax stopping times under uniform legal states."""
from collections import Counter
from math import factorial, prod
from fractions import Fraction
from itertools import product
import json
from audit_r14_p840_constructive_19_frame import EdgeGame, COLORS, E, transports, physical_replay

class PrefixMinimaxGame:
    """Use the smallest feasible root budget for the existing suffix solver."""

    def __init__(self, game):
        self.game = game
        self.full = game.full
        self.signs = game.signs
        self.words = game.words
        self.step = game.step
        self.budget = next(depth for depth in range(3, 9)
                           if game.action(game.full, depth, 3) is not None)

    def action(self, belief, depth, delay):
        return self.game.action(belief, depth - (8 - self.budget), delay)

    def replay(self, word, sign):
        belief = self.full
        for frame in range(12, 12 + self.budget):
            query = self.action(belief, 20 - frame, max(0, 15 - frame))
            assert query is not None
            if query >= 0:
                belief = self.step(belief, query, word[query])
            if frame == 14:
                belief &= self.signs[sign]
            if frame >= 14 and belief.bit_count() == 1:
                assert self.words[belief.bit_length() - 1] == (word, sign)
                return frame
        raise AssertionError("Exceeded the prefix minimax budget")


def orientation_prefix_counts():
    # Independently count legal orientations and choices of unread label.
    # For a fixed ordered prefix, permute the labeled edges within each
    # equal-color class to obtain every legal completion exactly once.
    counts = Counter()
    for flips in product((0, 1), repeat=12):
        if sum(flips) % 2:
            continue
        colors = tuple(word[flip] for word, flip in zip(E, flips))
        for unread in range(12):
            observed = colors[:unread] + colors[unread + 1:]
            counts[tuple(observed.count(c) for c in COLORS)] += 1
    assert sum(counts.values()) == 12 * 2**11
    return counts


def summarize(hist, corner_completions):
    total = sum(hist.values())
    mean = Fraction(sum(frame * count for frame, count in hist.items()), total)
    return {
        "edge_states_by_frame": dict(sorted(hist.items())),
        "cube_states_by_frame": {frame: count * corner_completions
                                 for frame, count in sorted(hist.items())},
        "mean_frames": str(mean),
    }


def main():
    table, maps = transports()
    orientations = orientation_prefix_counts()
    assert set(orientations) == set(table)
    members = {}
    for counts, (rep, _) in table.items():
        members.setdefault(rep, []).append(counts)
    baseline, optimized = Counter(), Counter()
    physical_games = {}
    roots_by_frame = Counter()
    states_by_root_frame = Counter()
    details = []
    for rep, count_vectors in sorted(members.items()):
        game = EdgeGame(''.join(c * n for c, n in zip(COLORS, rep)))
        weight = 0
        for counts in count_vectors:
            repeated_color_permutations = prod(factorial(n) for n in counts)
            assert len(game.words) == orientations[counts] * repeated_color_permutations
            weight += factorial(11) // repeated_color_permutations
        base = Counter(game.replay(word, sign) for word, sign in game.words)
        minimax = PrefixMinimaxGame(game)
        opt = Counter(minimax.replay(word, sign) for word, sign in game.words)
        root_frame = 11 + minimax.budget
        assert max(opt) == root_frame
        roots_by_frame[root_frame] += 1
        states_by_root_frame[root_frame] += weight * len(game.words)
        baseline.update({frame: count * weight for frame, count in base.items()})
        optimized.update({frame: count * weight for frame, count in opt.items()})
        details.append({
            "representative": rep, "ordered_prefixes": weight,
            "root_minimax_frame": root_frame,
            "baseline": dict(sorted(base.items())), "prefix_minimax": dict(sorted(opt.items())),
        })
        physical_games[rep] = minimax
        game.action.cache_clear()
    assert sum(baseline.values()) == sum(optimized.values()) == factorial(12) * 2**11
    assert max(baseline) == max(optimized) == 19
    physical, routes = physical_replay(physical_games, table, maps)
    corners = factorial(8) // 2 * 3**7
    print(json.dumps({
        "edge_states": sum(optimized.values()),
        "corner_completions_per_edge_state": corners,
        "cube_states": sum(optimized.values()) * corners,
        "baseline": summarize(baseline, corners),
        "prefix_minimax": summarize(optimized, corners),
        "representatives_by_root_minimax_frame": dict(sorted(roots_by_frame.items())),
        "edge_states_by_root_minimax_frame": dict(sorted(states_by_root_frame.items())),
        "prefix_minimax_physical_replay_by_frame": dict(sorted(physical.items())),
        "paired_routes": routes,
        "representatives": details,
    }, indent=2))


if __name__ == '__main__':
    main()
