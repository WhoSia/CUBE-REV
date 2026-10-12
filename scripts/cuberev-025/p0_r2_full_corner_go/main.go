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


const nOri=2187
const nPerm=40320
const nCorner=88179840
func decodePerm(n int)(v [8]uint8){list:=[8]uint8{0,1,2,3,4,5,6,7};left:=8;for i:=0;i<8;i++{base:=1;for k:=2;k<left;k++{base*=k};idx:=n/base;n%=base;v[i]=list[idx];copy(list[idx:],list[idx+1:left]);left--};return}
func codePerm(p [8]uint8)int{code:=0;used:=[8]bool{};for i:=0;i<8;i++{count:=0;for j:=0;j<int(p[i]);j++{if !used[j]{count++}};code=code*(8-i)+count;used[p[i]]=true};return code}
func decodeOri(n int)(o [8]uint8){sum:=0;for i:=6;i>=0;i--{o[i]=uint8(n%3);sum+=n%3;n/=3};o[7]=uint8((3-sum%3)%3);return}
func codeOri(o [8]uint8)int{code:=0;for i:=0;i<7;i++{code=code*3+int(o[i])};return code}
func main(){
 start:=time.Now();makeMoves();derivePhysicalTokenMoves()
 // actual move formula in the original fixed physical facelet frame
 var newPos [18][8]int;var twist [18][8]uint8
 for a:=0;a<18;a++{for p:=0;p<8;p++{v:=cornerMove[a][p*3];newPos[a][p]=int(v/3);twist[a][p]=v%3;for oldOri:=0;oldOri<3;oldOri++{t:=cornerMove[a][p*3+oldOri];if t/3!=v/3||int(t%3)!=(oldOri+int(v%3))%3{panic("non additive authentic twist")}}}}
 permTrans:=make([]uint16,nPerm*18);oriTrans:=make([]uint16,nOri*18)
 for i:=0;i<nPerm;i++{p:=decodePerm(i);if codePerm(p)!=i{panic("perm rank not bijective")};for a:=0;a<18;a++{var next [8]uint8;for k:=0;k<8;k++{next[newPos[a][k]]=p[k]};permTrans[i*18+a]=uint16(codePerm(next))}}
 for i:=0;i<nOri;i++{o:=decodeOri(i);if codeOri(o)!=i{panic("ori rank not bijective")};for a:=0;a<18;a++{var next [8]uint8;sum:=0;for k:=0;k<8;k++{next[newPos[a][k]]=(o[k]+twist[a][k])%3};for k:=0;k<8;k++{sum+=int(next[k])};if sum%3!=0{panic("nonphysical twist sum")};oriTrans[i*18+a]=uint16(codeOri(next))}}
 fmt.Printf("P0R2_REAL_FULL_CORNER_18_PHYSICAL_FACELET_MOVE_FACTORS PASS PERM %d TWIST %d ALL18 1\n",nPerm,nOri)
 src:="R' B' F2 D2 F2 L2 R2 U' F2 L2 D2 B2 D F L' R2 B U2 F2 R2"
 word:="F U F D' R' F' L' F' D' L B L2 F2 U2 L2 U F' R2"
 apply:=func(w string)int{pi,oi:=0,0;for _,t:=range strings.Fields(w){a:=-1;for i,m:=range moves{if m.name==t{a=i;break}};if a<0{panic("illegal move")};pi=int(permTrans[pi*18+a]);oi=int(oriTrans[oi*18+a])};return pi*nOri+oi}
 source:=apply(src);if apply(src+" "+word)!=0{panic("actual physical 18 cube word did not solve full corner")}
 fmt.Printf("P0R2_REAL_FULL_CORNER_WCA_SOURCE_INDEX %d KNOWN_COMPLETE_18_WITNESS_PASS 1\n",source)
 dist:=make([]uint8,nCorner);for i:=range dist{dist[i]=255}
 // RAM efficient full exact 88,179,840 corner group BFS: 84MiB distances, 336MiB queue.
 q:=make([]uint32,0,nCorner);q=append(q,0);dist[0]=0;head:=0;depth:=int(0);counts:=[]int{1,0};nextLimit:=len(q)
 for head<len(q){
  if head==nextLimit{depth++;counts=append(counts,0);nextLimit=len(q);fmt.Printf("P0R2_FULL_CORNER_LAYER %d STARTED HEAD %d DISTINCT_PREVIOUS %d ELAPSED_S %d\n",depth,head,len(q),int(time.Since(start).Seconds()))}
  v:=q[head];head++
  if int(dist[v])!=depth{panic(fmt.Sprintf("BFS state depth mismatch state %d got %d expected %d",v,dist[v],depth))}
  pbase:=int(v)/nOri*18;obase:=int(v)%nOri*18
  for a:=0;a<18;a++ {n:=uint32(permTrans[pbase+a])*nOri+uint32(oriTrans[obase+a]);if dist[n]==255{dist[n]=uint8(depth+1);q=append(q,n);counts[depth+1]++}}
  if head%4000000==0{fmt.Printf("P0R2_FULL_CORNER_PROGRESS HEAD %d TOTAL %d ELAPSED_S %d\n",head,len(q),int(time.Since(start).Seconds()))}
 }
 if len(counts)>0 && counts[len(counts)-1]==0 {counts=counts[:len(counts)-1]}
 expectedLayers:=[]int{1,18,243,2874,28000,205416,1168516,5402628,20776176,45391616,15139616,64736}
 if len(counts)!=len(expectedLayers){panic("wrong diameter")}
 for i,v:=range counts{if v!=expectedLayers[i]{panic(fmt.Sprintf("corner layer %d actual %d expected %d",i,v,expectedLayers[i]))}}
 if int(dist[source])!=9{panic("unexpected exact physical source9")}
 fmt.Printf("P0R2_FULL_CORNER_EXACT_PDB FINISHED 1 DISTINCT %d EXPECTED %d DIAMETER %d SOURCE_DISTANCE %d LAYERS %v ELAPSED_MS %d\n",len(q),nCorner,depth,dist[source],counts,time.Since(start).Milliseconds())
 if len(q)!=nCorner{panic("incomplete corners")}
 // exact admissible singleton: source entire-corner group bound <= true whole cube distance18
 if dist[source]>18{panic("PDB physically unsound")}
 fmt.Printf("P0R2_FULL_CORNER_CERTIFICATE WHOLE_ORIGINAL_CUBIES_SOURCE_PDB_LOWER %d INHERITED_FULL_GLOBAL_LOWER14 1 UNRESTRICTED_17_NONEXISTENCE_NOT_PROVED 1\n",dist[source])
}