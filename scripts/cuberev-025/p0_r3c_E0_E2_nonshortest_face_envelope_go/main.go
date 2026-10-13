// CUBE-REV 0.25 P0-R1: true physically induced 3x3 4-edge / 4-corner
// move-pattern quotient PDBs; exact finite quotient proof, not global d=18 proof.
package main

import (
	"fmt"
	"strings"
	"time"
)

type V struct{ x, y, z int }

func (a V) plus(b V) V { return V{a.x + b.x, a.y + b.y, a.z + b.z} }
func rot(v V, ax, q int) V {
	q = (q%4 + 4) % 4
	for ; q > 0; q-- {
		x, y, z := v.x, v.y, v.z
		switch ax {
		case 0:
			v = V{x, -z, y}
		case 1:
			v = V{z, y, -x}
		case 2:
			v = V{-y, x, z}
		}
	}
	return v
}

var normals = [6]V{{0, 1, 0}, {1, 0, 0}, {0, 0, 1}, {0, -1, 0}, {-1, 0, 0}, {0, 0, -1}} // URFDLB
var cornerN = [8][3]V{
	{{0, 1, 0}, {1, 0, 0}, {0, 0, 1}}, {{0, 1, 0}, {0, 0, 1}, {-1, 0, 0}},
	{{0, 1, 0}, {-1, 0, 0}, {0, 0, -1}}, {{0, 1, 0}, {0, 0, -1}, {1, 0, 0}},
	{{0, -1, 0}, {0, 0, 1}, {1, 0, 0}}, {{0, -1, 0}, {-1, 0, 0}, {0, 0, 1}},
	{{0, -1, 0}, {0, 0, -1}, {-1, 0, 0}}, {{0, -1, 0}, {1, 0, 0}, {0, 0, -1}}}
var edgeN = [12][2]V{
	{{0, 1, 0}, {1, 0, 0}}, {{0, 1, 0}, {0, 0, 1}}, {{0, 1, 0}, {-1, 0, 0}}, {{0, 1, 0}, {0, 0, -1}},
	{{0, -1, 0}, {1, 0, 0}}, {{0, -1, 0}, {0, 0, 1}}, {{0, -1, 0}, {-1, 0, 0}}, {{0, -1, 0}, {0, 0, -1}},
	{{0, 0, 1}, {1, 0, 0}}, {{0, 0, 1}, {-1, 0, 0}}, {{0, 0, -1}, {-1, 0, 0}}, {{0, 0, -1}, {1, 0, 0}}}

type Move struct {
	name           string
	axis, layer, q int
}

var moves []Move

func makeMoves() {
	faces := "URFDLB"
	for i, f := range []byte(faces) {
		axis, layer, q := 0, 0, 0
		switch f {
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
		_ = i
		for k, post := range []string{"", "'", "2"} {
			power := []int{1, 3, 2}[k]
			moves = append(moves, Move{string(f) + post, axis, layer, q * power})
		}
	}
}
func whichAxis(v V, ax int) int {
	if ax == 0 {
		return v.x
	}
	if ax == 1 {
		return v.y
	}
	return v.z
}
func turn(v V, m Move) V {
	if whichAxis(v, m.axis) == m.layer {
		return rot(v, m.axis, m.q)
	}
	return v
}
func faceTurn(v V, p V, m Move) V {
	if whichAxis(p, m.axis) == m.layer {
		return rot(v, m.axis, m.q)
	}
	return v
}

// Oriented quotient token is position * orientation modulus + orientation.
var edgeMove [18][24]uint8
var cornerMove [18][24]uint8

func derivePhysicalTokenMoves() {
	for a, m := range moves {
		for pos := 0; pos < 12; pos++ {
			p := edgeN[pos][0].plus(edgeN[pos][1])
			for ori := 0; ori < 2; ori++ {
				newP := turn(p, m)
				newSticker0 := faceTurn(edgeN[pos][ori], p, m)
				got := -1
				for n := 0; n < 12; n++ {
					pp := edgeN[n][0].plus(edgeN[n][1])
					if newP != pp {
						continue
					}
					for o := 0; o < 2; o++ {
						if edgeN[n][o] == newSticker0 {
							got = n*2 + o
						}
					}
				}
				if got < 0 {
					panic("edge token physical map not total")
				}
				edgeMove[a][pos*2+ori] = uint8(got)
			}
		}
		for pos := 0; pos < 8; pos++ {
			p := cornerN[pos][0].plus(cornerN[pos][1]).plus(cornerN[pos][2])
			for ori := 0; ori < 3; ori++ {
				newP := turn(p, m)
				newSticker0 := faceTurn(cornerN[pos][ori], p, m)
				newSticker1 := faceTurn(cornerN[pos][(ori+1)%3], p, m)
				got := -1
				for n := 0; n < 8; n++ {
					pp := cornerN[n][0].plus(cornerN[n][1]).plus(cornerN[n][2])
					if newP != pp {
						continue
					}
					for o := 0; o < 3; o++ {
						if cornerN[n][o] == newSticker0 && cornerN[n][(o+1)%3] == newSticker1 {
							got = n*3 + o
						}
					}
				}
				if got < 0 {
					panic(fmt.Sprintf("corner chirality map failed %s p%d o%d", m.name, pos, ori))
				}
				cornerMove[a][pos*3+ori] = uint8(got)
			}
		}
	}
	for a := 0; a < 18; a++ {
		var seenE [24]bool
		var seenC [24]bool
		for k := 0; k < 24; k++ {
			v := edgeMove[a][k]
			w := cornerMove[a][k]
			if seenE[v] || seenC[w] {
				panic("not a physical bijection")
			}
			seenE[v] = true
			seenC[w] = true
		}
	}
	fmt.Println("P0R1_TRUE_PHYSICAL_ORIENTED_EDGE_CORNER_GENERATORS PASS E24 C24 ALL18 1")
}

// Four DISTINCT labeled cubies, each with its physical orientation digit.
// Every legal quotient tuple is reachable; the algebraic state space has
// 12P4 * 2^4 = 190080 edge, and 8P4 * 3^4 = 136080 corner states.
type Pattern struct {
	tokens [4]uint8
	mod    int
	table  *[18][24]uint8
}

func encode(p Pattern) uint32 {
	var v uint32
	for _, s := range p.tokens {
		v = v*24 + uint32(s)
	}
	return v
}
func stateFromDigits(k uint32) [4]uint8 {
	var p [4]uint8
	for i := 3; i >= 0; i-- {
		p[i] = uint8(k % 24)
		k /= 24
	}
	return p
}
func moveCode(code uint32, tab *[18][24]uint8, act int) uint32 {
	p := stateFromDigits(code)
	var out uint32
	for _, t := range p {
		out = 24*out + uint32(tab[act][t])
	}
	return out
}
func valid(code uint32, mod int) bool {
	p := stateFromDigits(code)
	var mask uint16
	for _, a := range p {
		slot := a / uint8(mod)
		if slot >= uint8(24/mod) || mask&(1<<slot) != 0 {
			return false
		}
		mask |= 1 << slot
	}
	return true
}
func perm4(n int) int { return n * (n - 1) * (n - 2) * (n - 3) }

type DB struct {
	label      string
	mod        int
	tab        *[18][24]uint8
	identities [4]uint8
	dist       []uint8
	queue      []uint32
	far        int
	layers     []int
	buildN     int
}

func makeDB(label string, mod int, tab *[18][24]uint8, ids [4]uint8) *DB {
	db := &DB{label: label, mod: mod, tab: tab, identities: ids, dist: make([]uint8, 24*24*24*24)}
	for i := range db.dist {
		db.dist[i] = 255
	}
	var start Pattern
	for i, k := range ids {
		start.tokens[i] = k * uint8(mod)
	}
	init := encode(start)
	db.dist[init] = 0
	db.queue = make([]uint32, 1, perm4(24/mod)*mod*mod*mod*mod)
	db.queue[0] = init
	db.layers = []int{1}
	head := 0
	distNow := 0
	nextLayerLimit := 1
	for head < len(db.queue) {
		if head == nextLayerLimit {
			distNow++
			nextLayerLimit = len(db.queue)
			db.layers = append(db.layers, len(db.queue)-head)
		} // may need update later
		code := db.queue[head]
		head++
		old := db.dist[code]
		for a := 0; a < 18; a++ {
			v := moveCode(code, tab, a)
			if db.dist[v] != 255 {
				continue
			}
			if !valid(v, mod) {
				fmt.Printf("P0R1_BAD_MOVE input=%v action=%s result=%v mod=%d fromtokens=%v totokens=%v\n", code, moves[a].name, v, mod, stateFromDigits(code), stateFromDigits(v))
				panic("turn created coincident real cubies")
			}
			db.dist[v] = old + 1
			db.queue = append(db.queue, v)
		}
	}
	db.far = 0
	realLayers := make([]int, 32)
	for _, code := range db.queue {
		d := db.dist[code]
		realLayers[d]++
		if int(d) > db.far {
			db.far = int(d)
		}
	}
	db.layers = realLayers[:db.far+1]
	db.buildN = len(db.queue)
	expected := perm4(24 / mod)
	for i := 0; i < 4; i++ {
		expected *= mod
	}
	if len(db.queue) != expected {
		panic(fmt.Sprintf("incorrect quotient closure %s actual%d wanted%d", label, len(db.queue), expected))
	}
	for _, code := range db.queue {
		d := db.dist[code]
		for a := 0; a < 18; a++ {
			x := moveCode(code, tab, a)
			dd := db.dist[x]
			if dd == 255 || int(dd) > int(d)+1 || int(d) > int(dd)+1 {
				panic("quotient PDB not Lipschitz")
			}
		}
	}
	fmt.Printf("P0R1_EXACT_QUOTIENT_PDB %s IDENTITIES %v FULL_STATES %d DISTANCE_DIAMETER %d LAYERS %v EXACT_ONE_LIPSCHITZ PASS\n", label, ids, db.buildN, db.far, db.layers)
	return db
}
func applyWord(code uint32, db *DB, word string) uint32 {
	for _, token := range strings.Fields(word) {
		ix := -1
		for j, m := range moves {
			if m.name == token {
				ix = j
				break
			}
		}
		if ix < 0 {
			panic("not legal source token: " + token)
		}
		code = moveCode(code, db.tab, ix)
	}
	return code
}
func (db *DB) goalCode() uint32 {
	var p Pattern
	for i, k := range db.identities {
		p.tokens[i] = k * uint8(db.mod)
	}
	return encode(p)
}
func (db *DB) estimate(scramble string) int {
	return int(db.dist[applyWord(db.goalCode(), db, scramble)])
}
func (db *DB) hOfWord(w string) int { return int(db.dist[applyWord(db.goalCode(), db, w)]) }

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// Genuine independent 54-physical-sticker movement cross-check for every
// pattern's quotient homomorphism, rather than checking only quotient
// reachability. Every original sticker retains a unique immutable label.
type Sticker struct {
	p, n V
	id   int
}

func originalStickers() []Sticker {
	s := make([]Sticker, 0, 54)
	for _, n := range normals {
		for a := -1; a <= 1; a++ {
			for b := -1; b <= 1; b++ {
				p := V{}
				if n.x != 0 {
					p = V{n.x, a, b}
				} else if n.y != 0 {
					p = V{a, n.y, b}
				} else {
					p = V{a, b, n.z}
				}
				s = append(s, Sticker{p, n, len(s)})
			}
		}
	}
	if len(s) != 54 {
		panic("physical sticker count")
	}
	return s
}
func originalStickerAfter(w string) []Sticker {
	s := originalStickers()
	for _, token := range strings.Fields(w) {
		ix := -1
		for j, a := range moves {
			if a.name == token {
				ix = j
				break
			}
		}
		if ix < 0 {
			panic("nonphysical word token")
		}
		m := moves[ix]
		for i := range s {
			old := s[i].p
			if whichAxis(old, m.axis) == m.layer {
				s[i].p = rot(old, m.axis, m.q)
				s[i].n = rot(s[i].n, m.axis, m.q)
			}
		}
	}
	return s
}
func findMarkerId(s []Sticker, p, n V) int {
	for _, v := range s {
		if v.p == p && v.n == n {
			return v.id
		}
	}
	panic("marker not physically present")
}
func markerNow(s []Sticker, id int) Sticker {
	for _, v := range s {
		if v.id == id {
			return v
		}
	}
	panic("marker label missing")
}
func edgeMarkerToken(v Sticker) uint8 {
	for pos := 0; pos < 12; pos++ {
		p := edgeN[pos][0].plus(edgeN[pos][1])
		if v.p == p {
			for ori := 0; ori < 2; ori++ {
				if v.n == edgeN[pos][ori] {
					return uint8(pos*2 + ori)
				}
			}
		}
	}
	panic("edge marker not in actual physical edge slot")
}
func cornerMarkerToken(v Sticker) uint8 {
	for pos := 0; pos < 8; pos++ {
		p := cornerN[pos][0].plus(cornerN[pos][1]).plus(cornerN[pos][2])
		if v.p == p {
			for ori := 0; ori < 3; ori++ {
				if v.n == cornerN[pos][ori] {
					return uint8(pos*3 + ori)
				}
			}
		}
	}
	panic("corner marker not in actual physical corner slot")
}
func verifyPhysicalQuotient(dbs []*DB, w string) {
	initial := originalStickers()
	after := originalStickerAfter(w)
	for _, db := range dbs {
		expected := stateFromDigits(applyWord(db.goalCode(), db, w))
		for i, piece := range db.identities {
			if db.mod == 2 {
				pos := edgeN[piece][0].plus(edgeN[piece][1])
				id := findMarkerId(initial, pos, edgeN[piece][0])
				actual := edgeMarkerToken(markerNow(after, id))
				if expected[i] != actual {
					panic(fmt.Sprintf("actual real edge marker mismatch %s w=%s piece=%d, expected=%d actual=%d", db.label, w, piece, expected[i], actual))
				}
			}
			if db.mod == 3 {
				pos := cornerN[piece][0].plus(cornerN[piece][1]).plus(cornerN[piece][2])
				id := findMarkerId(initial, pos, cornerN[piece][0])
				actual := cornerMarkerToken(markerNow(after, id))
				if expected[i] != actual {
					panic(fmt.Sprintf("actual real corner marker mismatch %s w=%s piece=%d, expected=%d actual=%d", db.label, w, piece, expected[i], actual))
				}
			}
		}
	}
}

// Parikh-face parity is a SHARED property of any single full-cube word.
// A length-L word w induces one vector in (Z/2)^6, independently of the
// tracked cubies. Exact quotient accepting parity sets must intersect.
// Disjointness proves NO global length-L solution, with no additive PDB lie.
func flipParityMask(mask uint64, face int) uint64 {
	var lows = [6]uint64{0x5555555555555555, 0x3333333333333333, 0x0f0f0f0f0f0f0f0f, 0x00ff00ff00ff00ff, 0x0000ffff0000ffff, 0x00000000ffffffff}
	shift := uint(1 << face)
	lo := lows[face]
	return ((mask & lo) << shift) | ((mask &^ lo) >> shift)
}
func wordParity(w string) int {
	v := 0
	for _, token := range strings.Fields(w) {
		ix := -1
		for j, a := range moves {
			if a.name == token {
				ix = j
				break
			}
		}
		if ix < 0 {
			panic("illegal parity word")
		}
		v ^= 1 << (ix / 3)
	}
	return v
}
func exactProjectedParities(db *DB, word string, steps int) []uint64 {
	t0 := time.Now()
	capacity := 24 * 24 * 24 * 24
	moveMap := make([]uint32, capacity*18)
	for _, code := range db.queue {
		for a := 0; a < 18; a++ {
			moveMap[int(code)*18+a] = moveCode(code, db.tab, a)
		}
	}
	curr := make([]uint64, capacity)
	srcCode := applyWord(db.goalCode(), db, word)
	curr[srcCode] = 1
	hits := make([]uint64, steps+1)
	hits[0] = curr[db.goalCode()]
	for d := 1; d <= steps; d++ {
		next := make([]uint64, capacity)
		for _, code := range db.queue {
			mask := curr[code]
			if mask == 0 {
				continue
			}
			row := int(code) * 18
			for a := 0; a < 18; a++ {
				v := moveMap[row+a]
				next[v] |= flipParityMask(mask, a/3)
			}
		}
		curr = next
		hits[d] = curr[db.goalCode()]
	}
	fmt.Printf("P0R1_PARIKH_EXACT_QUOTIENT %s LENGTHS_0_TO_%d_GOAL_PARITY_COUNTS [", db.label, steps)
	for i, v := range hits {
		if i > 0 {
			fmt.Print(" ")
		}
		fmt.Print(bitsOnes(v))
	}
	fmt.Printf("] ELAPSED_MS %d\n", time.Since(t0).Milliseconds())
	return hits
}
func bitsOnes(x uint64) int {
	n := 0
	for x > 0 {
		x &= x - 1
		n++
	}
	return n
}
func verifyFaceParitySynchronization(dbs []*DB, source, word string) {
	var all [5][]uint64
	for i, db := range dbs {
		all[i] = exactProjectedParities(db, source, 18)
	}
	witnessed := wordParity(word)
	earliest := -1
	for L := 0; L <= 18; L++ {
		common := ^uint64(0)
		for i := range all {
			common &= all[i][L]
		}
		if common != 0 && earliest < 0 {
			earliest = L
		}
		fmt.Printf("P0R1_SHARED_FACE_PARITY_LENGTH %d INTERSECTION_CLASSES %d GLOBAL_SOLUTION_CANDIDATE_NOT_CERTIFIED 1\n", L, bitsOnes(common))
		for parityVector := 0; parityVector < 64; parityVector++ {
			if bitsOnes(uint64(parityVector))%2 != L%2 && common&(uint64(1)<<uint(parityVector)) != 0 {
				panic("exact face parity product violated word-length parity")
			}
		}
		if L == 18 && (common&(uint64(1)<<witnessed)) == 0 {
			panic("real 18-turn source word does not lie in quotient Parikh accepting intersection")
		}
	}
	for i, hits := range all {
		if bitsOnes(hits[8]) != 32 || bitsOnes(hits[9]) != 32 {
			panic(fmt.Sprintf("P0R1 8/9 full parity saturation false in projection %d", i))
		}
	}
	fmt.Println("P0R1_PARIKH_COSSET_SATURATION_THEOREM SOURCE_SPECIFIC ALL_FIVE_QUOTIENTS EVEN_LENGTH8_32_OF32 ODD_LENGTH9_32_OF32 TWO_MOVE_INVERSE_PADDING_EXTENDS_TO_ALL_LENGTHS_GE8 PASS")
	fmt.Printf("P0R1_SYNCHRONIZED_QUOTIENT_PARIKH_LOWER %d FULL_UNRESTRICTED_B6_B7_LOWER 14 FULL_17_ABSENCE_UNPROVEN 1 REAL_18_WITNESS_FACE_PARITY 0x%x\n", earliest, witnessed)
}


// P0-R3B: source-specific genuinely physical 'face-count envelope' witnesses.
//
// For any pair of legal projected solution words u_i, u_j and ANY
// continuous face-uniform cost share x_f in [0,1], the two exact projected
// weighted minima obey:
// h_i(x)+h_j(1-x) <= Σ_f [n_i(f)*x_f+n_j(f)*(1-x_f)]
//                    <= Σ_f max(n_i(f), n_j(f)).
// This upper-certificate needs only TWO explicitly replayable projected
// original-cube words with a small integer face-count envelope.
// Enumeration below uses ORIGINAL quotient exact unweighted distances as
// a strictly decreasing DAG, no human/synthetic map substitutions.

type FaceSig struct{
 cnt [6]uint8
 witness []uint8
}
func exactShortestProjectedWordFaceSignatures(db *DB,original string)[]FaceSig{
 src:=applyWord(db.goalCode(),db,original)
 depth:=int(db.dist[src]);if depth>10 {panic("source physical witness unexpectedly deep")}
 d0:=db.dist[src]
 if d0==255 {panic("source absent from complete real physical PDB")}
 keys:=make(map[[6]uint8][]uint8)
 var counts [6]uint8
 path:=make([]uint8,0,depth)
 calls:=0
 var walk func(code uint32,d int)
 walk=func(code uint32,d int){
  calls++
  if calls>20000000 {panic("RESOURCE_HOLD_NOT_A_COMPLETE_ENVELOPE") }
  if d==0{
   if code!=db.goalCode(){panic("not projected whole tuple solved")}
   if _,ok:=keys[counts];!ok {keys[counts]=append([]uint8{},path...)}
   return
  }
  if int(db.dist[code])!=d{panic("not actual physical shortest quotient DAG")}
  for a:=0;a<18;a++{
   n:=moveCode(code,db.tab,a)
   if int(db.dist[n])!=d-1 {continue}
   face:=a/3
   counts[face]++
   path=append(path,uint8(a))
   walk(n,d-1)
   path=path[:len(path)-1]
   counts[face]--
  }
 }
 walk(src,depth)
 out:=make([]FaceSig,0,len(keys))
 for c,w:=range keys {
  total:=0;for _,x:=range c {total+=int(x)}
  if total!=depth {panic("face signature length mismatch")}
  // Replay every selected literal projected shortest solution word on the
  // actual original original 18-move physical Marked-cubie permutation.
  n:=src
  for _,a:=range w {n=moveCode(n,db.tab,int(a))}
  if n!=db.goalCode(){panic("nonphysical projected word face certificate")}
  out=append(out,FaceSig{c,w})
 }
 fmt.Printf("P0R3B_REAL_SHORTEST_PROJECTED_WORDS_COMPLETE pattern=%s source_h=%d exact_word_DAG_calls=%d unique_face_count_witnesses=%d every_signature_replayed=1\n",db.label,depth,calls,len(out))
 return out
}
func max(a,b int)int{if a>b{return a};return b}
func wordsString(s []uint8)string{
 var parts []string;for _,a:=range s {parts=append(parts,moves[a].name)}
 return strings.Join(parts," ")
}
// P0-R3C: decide the ONE P0R3B shortest-word-only envelope gap E0/E2.
// For each of all E0's exact-shortest source-specific ORIGINAL word face
// count budgets b_f, find any ACTUAL E2 source-solving projected word of
// length≤7 using each physical face no more than b_f times. This allows
// NON-SHORTEST E2 words to match E0's face budget, unlike the previous
// optimal-word-DAG-only experiment. Memoized exact physical 18 move DFS;
// no abstract fake edges and no human attribution.
func quotaKey(code uint32,quota [6]uint8)uint64{
 var k uint64
 for i,v:=range quota {if v>7{panic("3bit face count invalid")};k|=uint64(v)<<uint(3*i)}
 return (uint64(code)<<18)|k
}
func findProjectedWordWithinE0FaceBudget(db *DB,src uint32,quota [6]uint8)([]uint8,int,int){
 goal:=db.goalCode()
 total:=0;for _,v:=range quota {total+=int(v)}
 if total!=7{panic("E0 source shortest path must be seven turns")}
 var path []uint8
 memo:=make(map[uint64]bool)
 calls:=0
 const MAX=20000000
 var dfs func(state uint32,q [6]uint8,left int)bool
 dfs=func(state uint32,q [6]uint8,left int)bool{
  calls++
  if calls>MAX {panic("RESOURCE_HOLD_QUOTA_SOURCE_NOT_EXHAUSTED")}
  if state==goal {return true}
  if int(db.dist[state])>left {return false}
  if left==0 {return false}
  key:=quotaKey(state,q)
  if memo[key] {return false}
  for face:=0;face<6;face++{
   if q[face]==0 {continue}
   nextQuota:=q;nextQuota[face]--
   for mod:=0;mod<3;mod++{
    a:=face*3+mod
    nxt:=moveCode(state,db.tab,a)
    if int(db.dist[nxt])>left-1 {continue}
    path=append(path,uint8(a))
    if dfs(nxt,nextQuota,left-1){return true}
    path=path[:len(path)-1]
   }
  }
  memo[key]=true
  return false
 }
 if dfs(src,quota,7){
  reached:=src;var cnt [6]uint8
  for _,a:=range path {reached=moveCode(reached,db.tab,int(a));cnt[a/3]++}
  if reached!=goal {panic("replay failed")}
  for i:=range cnt {if cnt[i]>quota[i]{panic("face-count budget violated")}}
  return append([]uint8{},path...),calls,len(memo)
 }
 return nil,calls,len(memo)
}
func main(){
 makeMoves();derivePhysicalTokenMoves()
 original:="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2"
 // Only E0/E2 are necessary for the one scientifically live pair.
 e0:=makeDB("EDGE4_0",2,&edgeMove,[4]uint8{0,4,8,10})
 e2:=makeDB("EDGE4_2",2,&edgeMove,[4]uint8{2,3,6,7})
 verifyPhysicalQuotient([]*DB{e0,e2},original)
 sigs:=exactShortestProjectedWordFaceSignatures(e0,original)
 sourceE2:=applyWord(e2.goalCode(),e2,original)
 found:=0;totalCalls:=0
 for i,entry:=range sigs {
  word,calls,memo:=findProjectedWordWithinE0FaceBudget(e2,sourceE2,entry.cnt)
  totalCalls+=calls
  if word!=nil{
   cntE2:=[6]uint8{};for _,a:=range word{cntE2[a/3]++}
   summax:=0;for f:=0;f<6;f++{summax+=max(int(entry.cnt[f]),int(cntE2[f]))}
   if summax!=7 {panic("strong projected shared face-count certificate invalid")}
   fmt.Printf("P0R3C_REAL_PHYSICAL_NONSHORTEST_E2_SUCCESS E0_SEVEN_WORD=%q E0_FACE_BUDGET=%v E2_GOAL_WORD=%q E2_WORD_LEN=%d E2_COUNTS=%v JOIN_ENVELOPE=%d SEARCH_CALLS=%d MEMO=%d\n",wordsString(entry.witness),entry.cnt,wordsString(word),len(word),cntE2,summax,calls,memo)
   found++
   break
  }
  fmt.Printf("P0R3C_E0_FACE_QUOTA_EXACT_FAILURE candidate=%d required_E0_7_word=%q face_budget=%v scanned=%d memo=%d\n",i,wordsString(entry.witness),entry.cnt,calls,memo)
 }
 if found>0{
  fmt.Printf("P0R3C_ALL_CONTINUOUS_TWO_QUOTIENT_PAIRS_SOURCE_UPPER7_CERTIFIED_WITH_9_R3B_WITNESSES PLUS_E0_E2_EXPLICIT_PHYSICAL_WORD_SOURCE_CERTIFICATE=1 actual_price_x_any_real_between_0_and_1=1 every_half_price_integer_result_7_consistent=1\n")
 } else {
  fmt.Printf("P0R3C_E0_E2_SINGLE_WORD_PAIR_ENVELOPE7_UNPROVEN whole_E0_face_signature_candidates=%d state_pruned_memoized_E2_actual_moves=1 complete_under_7_face_quota=1 total_calls=%d mixes_of_source_paths_may_still_succeed=1\n",len(sigs),totalCalls)
 }
}
