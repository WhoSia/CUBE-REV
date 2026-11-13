#!/usr/bin/env python3
"""Certify a 19-frame policy after an 11-position edge scan.

The remaining edge game uses only observed colors until the seventh
corner's second color at frame 14 reveals the common permutation sign.
"""
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from functools import lru_cache
from io import StringIO
import json

from audit_r14_p86_constructive_full_20_frame import (
    COLORS, E, C, all_count_vectors, color_symmetries, enumerate_sector,
    parity, transform_counts,
)


def prefix_count(colors):
    return tuple(colors.count(color) for color in COLORS)


def transports():
    prefixes = {
        tuple(n - (i == j) for i, n in enumerate(counts))
        for counts in all_count_vectors()
        for j, n in enumerate(counts) if n
    }
    maps = color_symmetries()
    return {
        count: min(
            ((transform_counts(count, colors), index) for index, (colors, *_) in enumerate(maps))
        )
        for count in sorted(prefixes)
    }, maps


class EdgeGame:
    def __init__(self, prefix):
        # Slots 0..10 are the mates of the eleven scanned edges.
        # Slots 11 and 12 are the two sides of the wholly unread edge.
        self.words = tuple(
            (other[:11] + color + other[11], sign)
            for color in COLORS
            for other, sign in enumerate_sector(prefix + color)
        )
        assert len({word for word, _ in self.words}) == len(self.words)
        self.cells = [defaultdict(int) for _ in range(13)]
        self.signs = [0, 0]
        for i, (word, sign) in enumerate(self.words):
            bit = 1 << i
            self.signs[sign] |= bit
            for query, color in enumerate(word):
                self.cells[query][color] |= bit
        self.full = self.signs[0] | self.signs[1]

    @lru_cache(None)
    def action(self, belief, depth, delay):
        count = belief.bit_count()
        if count <= 1:
            return -1
        if depth == 0:
            return None
        options = []
        for query, row in enumerate(self.cells):
            children = sorted(
                (belief & cell for cell in row.values() if belief & cell),
                key=int.bit_count, reverse=True,
            )
            if len(children) > 1:
                options.append((children[0].bit_count(), len(children), query, children))
        if delay:
            # Repeat a known observation to advance to the next corner frame.
            options.append((count, 1, -2, [belief]))
        for _, _, query, children in sorted(options):
            if delay == 1:
                successors = ((child & sign, 0) for child in children for sign in self.signs)
            else:
                successors = ((child, max(0, delay - 1)) for child in children)
            if all(self.action(child, depth - 1, next_delay) is not None
                   for child, next_delay in successors if child):
                return query
        return None

    def step(self, belief, query, color):
        return belief if query == -2 else belief & self.cells[query][color]

    def replay(self, word, sign):
        belief = self.full
        for frame in range(12, 20):
            query = self.action(belief, 20 - frame, max(0, 15 - frame))
            assert query is not None
            if query != -1:
                belief = self.step(belief, query, word[query])
            if frame == 14:
                belief &= self.signs[sign]
            if frame >= 14 and belief.bit_count() == 1:
                assert self.words[belief.bit_length() - 1] == (word, sign)
                return frame
        raise AssertionError("The edge policy exceeded 19 frames")


def physical_replay(games, prefix_transports, maps):
    with redirect_stdout(StringIO()):
        import audit_r14_p51_p48_group_lift as physical

    edges = tuple(physical.PIECES[p] for p in physical.EDGES)
    corners = tuple(physical.PIECES[p] for p in physical.CORNERS)
    assert tuple(''.join(physical.COLORS[s] for s in slots) for slots in edges) == E
    assert tuple(''.join(physical.COLORS[s] for s in slots) for slots in corners) == C
    corner_code = {
        word[rot] + word[(rot + 1) % 3]: (src, rot)
        for src, word in enumerate(C) for rot in range(3)
    }
    assert len(corner_code) == 24
    # Reverse the forward slot route, keeping its turns legal, to bring
    # the requested initial-frame slots under the stationary probes.
    routes = {}
    for pair, moves in physical.seen.items():
        forward = physical.EYE
        for move in moves:
            forward = physical.compose(physical.MOVES[move], forward)
        backward = physical.inverse(forward)
        assert tuple(backward[s] for s in pair) == physical.q0
        routes[pair] = backward

    hist = Counter()
    for state in physical.states:
        def read(edge, frame):
            corner = corners[(frame - 1) // 2][(frame - 1) % 2] if frame <= 14 else corners[0][0]
            return physical.obs(physical.compose(routes[edge, corner], state), physical.q0)

        prefix, corner_colors = zip(*(read(edges[i][0], i + 1) for i in range(11)))
        corner_colors = list(corner_colors)
        rep, map_index = prefix_transports[prefix_count(prefix)]
        relabel, _, source_sign, _ = maps[map_index]
        inverse_color = {b: a for a, b in relabel.items()}
        order = sorted(range(11), key=lambda i: COLORS.index(relabel[prefix[i]])) + [11]
        game = games[rep]
        assert tuple(relabel[prefix[i]] for i in order[:11]) == tuple(
            color for color, n in zip(COLORS, rep) for _ in range(n)
        )
        slots = [edges[i][1] for i in order[:11]] + list(edges[11])
        belief = game.full
        for frame in range(12, 20):
            query = game.action(belief, 20 - frame, max(0, 15 - frame))
            assert query is not None
            edge_color, corner_color = read(slots[query] if query >= 0 else edges[0][0], frame)
            corner_colors.append(corner_color)
            if query >= 0:
                belief = game.step(belief, query, relabel[edge_color])
            if frame == 14:
                decoded = [corner_code[''.join(corner_colors[i:i+2])] for i in range(0, 14, 2)]
                perm = [src for src, _ in decoded]
                twists = [rot for _, rot in decoded]
                assert len(set(perm)) == 7
                perm.append(next(src for src in range(8) if src not in perm))
                twists.append(-sum(twists) % 3)
                full_corner = ''.join(C[src][(rot + k) % 3] for src, rot in zip(perm, twists) for k in range(3))
                belief &= game.signs[parity(perm) ^ parity(order) ^ source_sign]
            if frame >= 14 and belief.bit_count() == 1:
                canonical, _ = game.words[belief.bit_length() - 1]
                recovered = {slot: color for slot, color in zip((edge[0] for edge in edges), prefix)}
                recovered.update((slot, inverse_color[color]) for slot, color in zip(slots, canonical))
                inv = physical.inverse(state)
                assert all(recovered[s] == physical.COLORS[inv[s]] for edge in edges for s in edge)
                assert full_corner == ''.join(physical.COLORS[inv[s]] for corner in corners for s in corner)
                hist[frame] += 1
                break
        else:
            raise AssertionError("Physical replay exceeded 19 frames")
    assert sum(hist.values()) == len(physical.states)
    return hist, len(routes)


def verify_eighteen_frame_obstruction():
    # Literal assignment enumeration and set-partition recursion, independent
    # of the policy's bitsets and delayed parity recurrence.
    prefix = "RFFDDLLLBBB"
    words = [set(), set()]

    def visit(remaining, labels, sides, flips):
        pos = len(labels)
        if pos == 12:
            if flips == 0:
                word = ''.join(side[1] for side in sides[:11]) + sides[11]
                words[parity(labels)].add(word)
            return
        for label in sorted(remaining):
            for flip, side in enumerate((E[label], E[label][::-1])):
                if pos == 11 or side[0] == prefix[pos]:
                    visit(remaining - {label}, labels + [label], sides + [side], flips ^ flip)

    visit(set(range(12)), [], [], 0)
    game = EdgeGame(prefix)
    assert [len(group) for group in words] == [1656, 1656]
    assert all(group == {word for word, sign in game.words if sign == i}
               for i, group in enumerate(words))
    witnesses = []
    for group in words:
        @lru_cache(None)
        def wins(belief, depth):
            if len(belief) <= 1:
                return True
            if depth == 0:
                return False
            options = []
            for q in range(13):
                cells = defaultdict(set)
                for word in belief:
                    cells[word[q]].add(word)
                if len(cells) > 1:
                    children = sorted(map(frozenset, cells.values()), key=len, reverse=True)
                    options.append((len(children[0]), q, children))
            return any(all(wins(child, depth - 1) for child in children)
                       for _, _, children in sorted(options))

        for q in range(13):
            for color in COLORS:
                child = frozenset(word for word in group if word[q] == color)
                if child and not wins(child, 6):
                    witnesses.append([q, color, len(child)])
                    break
            else:
                raise AssertionError("Missing root obstruction")
        wins.cache_clear()
    return {"prefix": prefix, "states_per_sign": [len(group) for group in words],
            "root_obstructions_per_sign": [witnesses[:13], witnesses[13:]]}


def main():
    prefix_transports, maps = transports()
    assert len(prefix_transports) == 1362
    representatives = sorted({rep for rep, _ in prefix_transports.values()})
    assert len(representatives) == 52
    games = {}
    hist = Counter()
    for rep in representatives:
        prefix = ''.join(color * n for color, n in zip(COLORS, rep))
        game = EdgeGame(prefix)
        games[rep] = game
        assert game.action(game.full, 8, 3) is not None, prefix
        hist.update(game.replay(word, sign) for word, sign in game.words)
    physical_hist, routes = physical_replay(games, prefix_transports, maps)
    print(json.dumps({
        "status": "PASS",
        "upper_bound_frames": 19,
        "prefix_color_count_vectors": len(prefix_transports),
        "representatives": len(games),
        "canonical_edge_assignments": sum(hist.values()),
        "canonical_replay_by_frame": hist,
        "physical_replay_by_frame": physical_hist,
        "paired_routes": routes,
        "eighteen_frame_obstruction_after_fixed_eleven_scan": verify_eighteen_frame_obstruction(),
    }, sort_keys=True))


if __name__ == '__main__':
    main()
