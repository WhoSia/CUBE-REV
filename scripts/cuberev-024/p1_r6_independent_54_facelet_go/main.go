// CUBE-REV 0.24 P1-R6: INDEPENDENT 54-physical-sticker full18 HTM ball oracle.
// Does NOT import prior C++ cubie model. Complete board keys [54]uint8.
// Exhaustive two-sided radius-five: if disjoint, d18>=11 globally for this source.
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type Vec struct{ x, y, z int }
type Cell struct {
	p, n Vec
	face uint8
}
type State [54]uint8
type Action struct {
	face   byte
	suffix byte
	perm   [54]uint8
}

var faces = "URFDLB"
var acts []Action

func normal(f byte) Vec {
	switch f {
	case 'U':
		return Vec{0, 1, 0}
	case 'R':
		return Vec{1, 0, 0}
	case 'F':
		return Vec{0, 0, 1}
	case 'D':
		return Vec{0, -1, 0}
	case 'L':
		return Vec{-1, 0, 0}
	default:
		return Vec{0, 0, -1}
	}
}
func rot(v Vec, axis, q int) Vec {
	q = (q%4 + 4) % 4
	for ; q > 0; q-- {
		x, y, z := v.x, v.y, v.z
		switch axis {
		case 0:
			v = Vec{x, -z, y}
		case 1:
			v = Vec{z, y, -x}
		case 2:
			v = Vec{-y, x, z}
		}
	}
	return v
}
func geom() (State, []Cell) {
	var solved State
	cells := make([]Cell, 0, 54)
	for f := 0; f < 6; f++ {
		n := normal(faces[f])
		for a := -1; a <= 1; a++ {
			for b := -1; b <= 1; b++ {
				p := Vec{}
				if n.x != 0 {
					p = Vec{n.x, a, b}
				} else if n.y != 0 {
					p = Vec{a, n.y, b}
				} else {
					p = Vec{a, b, n.z}
				}
				solved[len(cells)] = uint8(f)
				cells = append(cells, Cell{p, n, uint8(f)})
			}
		}
	}
	return solved, cells
}
func makeMoves(cells []Cell) {
	idx := map[[6]int]uint8{}
	for i, c := range cells {
		idx[[6]int{c.p.x, c.p.y, c.p.z, c.n.x, c.n.y, c.n.z}] = uint8(i)
	}
	for _, face := range []byte(faces) {
		for _, suf := range []byte{' ', '\'', '2'} {
			axis, layer, q := 0, 0, 0
			switch face {
			case 'U':
				axis, layer, q = 1, 1, -1
			case 'D':
				axis, layer, q = 1, -1, 1
			case 'R':
				axis, layer, q = 0, 1, -1
			case 'L':
				axis, layer, q = 0, -1, 1
			case 'F':
				axis, layer, q = 2, 1, -1
			case 'B':
				axis, layer, q = 2, -1, 1
			}
			power := 1
			if suf == '\'' {
				power = 3
			}
			if suf == '2' {
				power = 2
			}
			action := Action{face: face, suffix: suf}
			for i, c := range cells {
				p, n := c.p, c.n
				level := p.x
				if axis == 1 {
					level = p.y
				}
				if axis == 2 {
					level = p.z
				}
				if level == layer {
					p = rot(p, axis, q*power)
					n = rot(n, axis, q*power)
				}
				key := [6]int{p.x, p.y, p.z, n.x, n.y, n.z}
				pos, ok := idx[key]
				if !ok {
					panic("original sticker geometry not bijective")
				}
				action.perm[i] = pos
			}
			acts = append(acts, action)
		}
	}
}
func move(s State, a Action) State {
	var out State
	for i, k := range a.perm {
		out[k] = s[i]
	}
	return out
}
func actIndex(t string) int {
	for i, a := range acts {
		str := string(a.face)
		if a.suffix != ' ' {
			str += string(a.suffix)
		}
		if str == t {
			return i
		}
	}
	panic("not an actual HTM move: " + t)
}
func fromMoves(word string, goal State) State {
	s := goal
	for _, t := range strings.Fields(word) {
		s = move(s, acts[actIndex(t)])
	}
	return s
}
func exactGoalBall(goal State, r int) (map[State]struct{}, []int) {
	visited := map[State]struct{}{goal: {}}
	cur := []State{goal}
	sizes := []int{1}
	for d := 1; d <= r; d++ {
		next := make([]State, 0, len(cur)*11)
		for _, s := range cur {
			for _, a := range acts {
				v := move(s, a)
				if _, ok := visited[v]; ok {
					continue
				}
				visited[v] = struct{}{}
				next = append(next, v)
			}
		}
		sizes = append(sizes, len(next))
		cur = next
		fmt.Printf("P1R6_GO_INDEPENDENT_54STICKER_GOAL_LAYER %d DISTINCT %d TOTAL %d\n", d, len(cur), len(visited))
	}
	return visited, sizes
}
func legal(last, intNext int) bool {
	if last < 0 {
		return true
	}
	f, g := last/3, intNext/3
	if f == g {
		return false
	}
	if (f == 0 && g == 3) || (f == 3 && g == 0) || (f == 1 && g == 4) || (f == 4 && g == 1) || (f == 2 && g == 5) || (f == 5 && g == 2) {
		return g >= f
	}
	return true
}
func sourceTraverse(source State, goalSet map[State]struct{}, r int) (bool, []uint64) {
	var visits uint64
	found := false
	layers := []uint64{}
	var rec func(State, int, int, int)
	rec = func(s State, depth, maxD, last int) {
		if found {
			return
		}
		visits++
		if _, ok := goalSet[s]; ok {
			found = true
			return
		}
		if depth == maxD {
			return
		}
		for j, a := range acts {
			if !legal(last, j) {
				continue
			}
			rec(move(s, a), depth+1, maxD, j)
			if found {
				return
			}
		}
	}
	for d := 0; d <= r; d++ {
		before := visits
		rec(source, 0, d, -1)
		layers = append(layers, visits-before)
		fmt.Printf("P1R6_GO_INDEPENDENT_54STICKER_SOURCE_BOUND %d NODES %d MATCH %v\n", d, visits-before, found)
		if found {
			break
		}
	}
	return found, layers
}
func main() {
	rad := 5
	if len(os.Args) > 1 {
		r, e := strconv.Atoi(os.Args[1])
		if e != nil || r < 0 || r > 5 {
			panic("go exact full-sticker proof limited radius<=5")
		}
		rad = r
	}
	t0 := time.Now()
	identity, cells := geom()
	makeMoves(cells)
	if len(acts) != 18 {
		panic("original physical move generator count")
	}
	scramble := "R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2"
	witness := "F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2"
	source := fromMoves(scramble, identity)
	solved := fromMoves(scramble+" "+witness, identity)
	if solved != identity {
		panic("prior genuine 18 HTM witness does NOT solve physical 54-sticker source")
	}
	fmt.Println("P1R6_GO_INDEPENDENT_TRUE_54_STICKER_WCA_18_WITNESS PASS")
	ball, counts := exactGoalBall(identity, rad)
	if rad >= 4 && counts[4] != 43239 {
		panic("independent original 54-facelet global layer4 differs")
	}
	if rad == 5 && counts[5] != 574908 {
		panic("independent layer5 differs")
	}
	found, visits := sourceTraverse(source, ball, rad)
	if found {
		fmt.Println("P1R6_GO_SOURCE_COMPLETENESS_INTERSECTION_FOUND")
		os.Exit(1)
	}
	fmt.Printf("P1R6_GO_COMPLETE_SOURCE_GLOBAL_EXCLUSION ALL18_MOVES 1 STRICT_54_FACELET_KEYS 1 EXCLUDED_LENGTH_LEQ %d LOWER_BOUND %d UPPER_BOUND 18 GOAL_DISTINCT %d SOURCE_BOUND_VISITS %v DURATION_MS %d\n", 2*rad, 2*rad+1, len(ball), visits, time.Since(t0).Milliseconds())
}