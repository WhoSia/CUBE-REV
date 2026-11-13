// CUBE-REV R14-P8.41: exact 18-frame edge minimax with the full corner oracle.
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <string_view>
#include <vector>
using namespace std;

constexpr int label_count = 12, codes = 15625, full_mask = (1 << label_count) - 1;
constexpr array<int, 6> powers{1,5,25,125,625,3125};
constexpr string_view colors = "URFDLB";
constexpr array<string_view, label_count> edges{
    "DL","BL","FL","UL","DB","DF","UB","UF","DR","BR","FR","UR"
};
array<array<int,2>,label_count> stickers;
struct Pending {
    array<int,6> count{}, before{}, after{};
    int size = 0;
};
array<Pending,codes> patterns;

// Each position is either single-read or untouched. The remaining labels and
// parity requirements describe a bijection in the order of these positions.
struct State {
    int mask, code, sign, flip;
    size_t key() const {
        return ((size_t(mask) * codes + code) * 2 + sign) * 2 + flip;
    }
    State remove(int label, int position, int color, int orientation) const {
        const int bit = 1 << label;
        return {mask ^ bit, color < 0 ? code : code - powers[color],
                sign ^ ((position + popcount(unsigned(mask & (bit - 1)))) & 1),
                flip ^ orientation};
    }
};

vector<uint8_t> counts(size_t(full_mask + 1) * codes * 4);
vector<uint8_t> outcomes(counts.size());
uint64_t games = 0;

int count_at_most_two(State state) {
    auto &cached = counts[state.key()];
    if (cached) return cached - 1;
    const auto &pending = patterns[state.code];
    const int remaining = popcount(unsigned(state.mask));
    if (pending.size > remaining) {
        cached = 1;
        return 0;
    }
    if (!remaining) {
        cached = 1 + (state.sign == 0 && state.flip == 0);
        return cached - 1;
    }
    int first_color = -1;
    if (pending.size)
        for (int color = 0; color < 6; ++color)
            if (pending.count[color]) {
                first_color = color;
                break;
            }
    int count = 0;
    for (int bits = state.mask; bits && count < 2; bits &= bits - 1) {
        const int label = countr_zero(unsigned(bits));
        for (int orientation = 0; orientation < 2 && count < 2; ++orientation)
            if (first_color < 0 || stickers[label][orientation] == first_color)
                count += count_at_most_two(state.remove(label, 0, first_color, orientation));
    }
    cached = 1 + (count >= 2 ? 2 : count);
    return cached - 1;
}

bool wins(State state, int depth) {
    if (count_at_most_two(state) <= 1) return true;
    if (!depth) return false;
    // Each recursive step reads a previously unread sticker. The mask
    // and pending length determine the number of such readings, so the
    // remaining budget is implicit for this fixed-horizon executable.
    auto &cached = outcomes[state.key()];
    if (cached) return cached == 2;
    ++games;
    const auto &pending = patterns[state.code];
    const int unseen = popcount(unsigned(state.mask)) - pending.size;
    if (unseen) {
        for (int position = 0; position < (unseen >= 2 ? 2 : 1); ++position) {
            for (int side = 0; side < 2; ++side) {
                bool valid = true;
                for (int color = 0; color < 6 && valid; ++color) {
                    if (pending.count[color] == 4) continue;
                    State child{state.mask, state.code + powers[color],
                                state.sign ^ ((pending.after[color] + position) & 1),
                                state.flip ^ side};
                    valid = wins(child, depth - 1);
                }
                if (valid) {
                    cached = 2;
                    return true;
                }
            }
        }
    }
    for (int color = 0; color < 6; ++color) {
        // Interchanging two equal-color pending positions preserves all
        // observed colors. The two index parities cover the available queries.
        for (int offset = 0; offset < (pending.count[color] >= 2 ? 2 : pending.count[color]); ++offset) {
            bool valid = true;
            for (int bits = state.mask; bits && valid; bits &= bits - 1) {
                const int label = countr_zero(unsigned(bits));
                for (int orientation = 0; orientation < 2 && valid; ++orientation)
                    if (stickers[label][orientation] == color)
                        valid = wins(state.remove(label, pending.before[color] + offset,
                                                  color, orientation), depth - 1);
            }
            if (valid) {
                cached = 2;
                return true;
            }
        }
    }
    cached = 1;
    return false;
}

int main() {
    for (int label = 0; label < label_count; ++label)
        for (int side = 0; side < 2; ++side)
            stickers[label][side] = int(colors.find(edges[label][side]));
    for (int code = 0; code < codes; ++code) {
        auto &pending = patterns[code];
        for (int c = 0; c < 6; ++c) {
            pending.count[c] = (code / powers[c]) % 5;
            pending.before[c] = pending.size;
            pending.size += pending.count[c];
        }
        for (int c = 0; c < 6; ++c)
            pending.after[c] = pending.size - pending.before[c] - pending.count[c];
    }
    for (int sign = 0; sign < 2; ++sign) {
        bool feasible = wins({full_mask, 0, sign, 0}, 18);
        cout << "sign " << sign << " wins " << feasible << " games " << games << endl;
        if (feasible) return 1;
    }
}
