#!/usr/bin/env python3
"""R14-P8.6 constructive 20-frame bound for physical P48 paired six-color probes.

Fully finite-checkable combinatorial strategy:
  frames 1..12: one first-index facelet at every edge position; concurrently
                 first two facelets of six distinct corner positions.
  frames 13..14: adaptive edge mate queries; finish two corner facelets at
                 the seventh corner position, infer full corner state/parity.
  frames 15..20: remaining edge mate queries; in the exceptional count orbit
                 use revealed corner parity after the first two mate queries.

Edge first-color count vectors 867, paired under 48 source-color edge-graph
symmetries into 39 orbits. Exact AND-OR and policy replay over every canonical
residual; full candidate-state maps/replays over all 867 canonical color-count
patterns. All mathematical symmetries are about the *edge observation game*,
not claimed as 48 combined corner chirality cube symmetries.
"""
from itertools import permutations,product
from collections import Counter,defaultdict
from functools import lru_cache
from math import factorial,prod
from pathlib import Path
import hashlib,json,time

HERE=Path(__file__).resolve().parent
E=('DL','BL','FL','UL','DB','DF','UB','UF','DR','BR','FR','UR')
C=('DLB','DFL','UBL','ULF','DBR','DRF','URB','UFR')
COLORS='URFDLB'
OPPOSITES={frozenset(s) for s in ('UD','RL','FB')}

def parity(t):return sum(t[i]>t[j] for i in range(len(t)) for j in range(i+1,len(t)))%2

def enumerate_sector(first):
    """All full edge matching words (second sticker at every position) with even flip sum.

    Permutation parity deliberately NOT restricted: corner observations later
    reveal the correct common parity and every even-flip edge permutation has
    some legal corner completion.
    """
    options=[[(label,word[1-flip],flip) for label,word in enumerate(E)
              for flip in (0,1) if word[flip]==color] for color in first]
    out=[]
    def dfs(i,used,flip_sum,second,perm):
        if i==12:
            if flip_sum==0:out.append((''.join(second),parity(perm)))
            return
        for label,other,flip in options[i]:
            if not (used>>label)&1:
                dfs(i+1,used|(1<<label),flip_sum^flip,second+[other],perm+[label])
    dfs(0,0,0,[],[])
    assert len({(w,p) for w,p in out})==len(out)
    return tuple(out)

def all_count_vectors():
    orientation_counts=Counter()
    for flips in product((0,1),repeat=12):
        if sum(flips)%2:continue
        colors=tuple(E[i][flips[i]] for i in range(12))
        orientation_counts[tuple(colors.count(c) for c in COLORS)]+=1
    counts={c:v*prod(factorial(a) for a in c) for c,v in orientation_counts.items()}
    assert len(counts)==867 and sum(counts.values())==609376
    return counts

def color_symmetries():
    maps=[]
    for perm in permutations(COLORS):
        trans=dict(zip(COLORS,perm))
        if {frozenset(trans[c] for c in pair) for pair in OPPOSITES}!=OPPOSITES:continue
        tau=[];eps=[]
        for word in E:
            transformed=''.join(trans[c] for c in word)
            target=next(i for i,w in enumerate(E) if frozenset(w)==frozenset(transformed))
            assert transformed in (E[target],E[target][::-1])
            tau.append(target)
            eps.append(int(transformed!=E[target]))
        assert len(set(tau))==12
        assert sum(eps)%2==0,('color symmetry violates edge flip sum',trans)
        maps.append((trans,tuple(tau),parity(tau),tuple(eps)))
    assert len(maps)==48
    return maps

def transform_counts(count,m):
    return tuple(count[COLORS.index(next(c for c in COLORS if m[c]==target))] for target in COLORS)

class Court:
    def __init__(self,pattern):
        self.pattern=pattern
        self.states=enumerate_sector(pattern)
        self.index={s:i for i,s in enumerate(self.states)}
        self.full=(1<<len(self.states))-1
        self.mask=[]
        for query in range(12):
            cells={}
            for i,(word,p) in enumerate(self.states):
                color=word[query]
                cells[color]=cells.get(color,0)|(1<<i)
            assert sum(x.bit_count() for x in cells.values())==len(self.states)
            self.mask.append(cells)
        self.parity_masks=tuple(sum(1<<i for i,(_,pp) in enumerate(self.states) if pp==p) for p in (0,1))
        assert self.parity_masks[0]|self.parity_masks[1]==self.full
        self.hard=False
    def actions(self,B,k,prune=True):
        result=[]
        for query,cells in enumerate(self.mask):
            children=[B&mask for mask in cells.values() if B&mask]
            if len(children)<=1:continue
            worst=max(x.bit_count() for x in children)
            if prune and worst>4**(k-1):continue
            result.append(((worst,len(children),sum(z.bit_count()**2 for z in children),query),tuple(children)))
        result.sort()
        return result
    @lru_cache(None)
    def winning(self,B,k):
        if B.bit_count()<=1:return True
        if k<=0 or B.bit_count()>4**k:return False
        for score,children in self.actions(B,k):
            if all(self.winning(z,k-1) for z in sorted(children,key=int.bit_count,reverse=True)):
                return True
        return False
    @lru_cache(None)
    def winning_action(self,B,k):
        assert self.winning(B,k)
        if B.bit_count()<=1:return None
        for score,children in self.actions(B,k):
            if all(self.winning(z,k-1) for z in sorted(children,key=int.bit_count,reverse=True)):
                return score[-1]
        raise AssertionError('No winning action')
    @lru_cache(None)
    def delayed_win(self,B,early):
        """After EXACTLY early edge queries, reveal common parity at zero time cost;
        six further edge queries are allowed. At early=0 the corner sensor
        finishes its 14th observation and makes parity known.
        """
        if B.bit_count()<=1:return True
        if early==0:
            return all(self.winning(B&P,6) for P in self.parity_masks if B&P)
        for score,children in self.actions(B,early,prune=False):
            if all(self.delayed_win(z,early-1) for z in children):return True
        return False
    @lru_cache(None)
    def delayed_action(self,B,early):
        assert self.delayed_win(B,early)
        if B.bit_count()<=1:return None
        for score,children in self.actions(B,early,prune=False):
            if all(self.delayed_win(z,early-1) for z in children):return score[-1]
        raise AssertionError('No delayed action')
    def replay(self,word,p):
        """Policy uses outputs only; parity argument is read ONLY after two
        additional mate queries in the unique exceptional orbit.
        """
        i=self.index[(word,p)]
        B=self.full;reads=[]
        if self.hard:
            for early in (2,1):
                if B.bit_count()==1:break
                q=self.delayed_action(B,early)
                assert q is not None
                observed=word[q]
                B&=self.mask[q][observed]
                reads.append((q,observed))
            # Corner sensor has now read 14 facelets and independently supplies
            # the complete corner permutation and its sign.
            B&=self.parity_masks[p]
            budget=6
        else:
            budget=self.optimal_depth
        while B.bit_count()>1:
            q=self.winning_action(B,budget)
            assert q is not None
            observed=word[q]
            B&=self.mask[q][observed]
            reads.append((q,observed))
            budget-=1
        assert B==(1<<i)
        assert len(reads)<=8
        return reads

def color_first(count):return ''.join(color*n for color,n in zip(COLORS,count))

def color_map_for_member(member,representative,maps):
    return next(x for x in maps if transform_counts(member,x[0])==representative)

def transport(member,repmap,courts,maps,observed_first=None):
    """Exact source-color and spatial-slot bijection from member first-color
    canonical observations to canonical orbit representative observations."""
    rep,mapping=repmap[member]
    color,tau,tau_par,eps=mapping
    first=color_first(member) if observed_first is None else observed_first
    assert len(first)==12 and tuple(first.count(c) for c in COLORS)==member
    sigma=tuple(i for c in COLORS for i in range(12) if color[first[i]]==c)
    assert sorted(sigma)==list(range(12))
    assert ''.join(color[first[i]] for i in sigma)==color_first(rep)
    return courts[rep],color,tau_par^parity(sigma),sigma

def main():
    start=time.monotonic()
    counts=all_count_vectors();maps=color_symmetries()
    unseen=set(counts);orb=[];repmap={}
    while unseen:
        rep=min(unseen)
        members={transform_counts(rep,m[0]) for m in maps}
        assert members<=set(counts)
        for member in members:
            repmap[member]=(rep,color_map_for_member(member,rep,maps))
        orb.append((rep,members))
        unseen-=members
    assert len(orb)==39 and len(repmap)==867
    courts={};class_rows=[]
    for ix,(rep,members) in enumerate(orb):
        court=Court(color_first(rep))
        assert len(court.states)==counts[rep]
        depth=next(k for k in range(1,11) if court.winning(court.full,k))
        assert not court.winning(court.full,depth-1)
        court.optimal_depth=depth
        court.hard=depth>8
        if court.hard:
            assert depth==9
            assert court.delayed_win(court.full,2),('parity arrives too late',rep)
            assert all(court.winning(P,8) for P in court.parity_masks)
            assert all(not court.winning(P,7) for P in court.parity_masks)
        hist=Counter()
        for word,p in court.states:
            hist[len(court.replay(word,p))]+=1
        courts[rep]=court
        class_rows.append({'index':ix,'count_vector':rep,'representative_first_colors':color_first(rep),
                           'color_count_vectors_in_orbit':len(members),'states_in_canonical_game':len(court.states),
                           'exact_edge_mate_minimax_without_parity':depth,
                           'uses_parity_after_second_extra_edge_read':court.hard,
                           'replay_depth_histogram':dict(sorted(hist.items())),
                           'all_representative_states_decoded':sum(hist.values()),
                           'AND_OR_cache_nodes':court.winning.cache_info().currsize})
    assert len(courts)==39
    assert Counter({d:sum(r['color_count_vectors_in_orbit'] for r in class_rows if r['exact_edge_mate_minimax_without_parity']==d) for d in (6,7,8,9)})==Counter({6:72,7:636,8:156,9:3})
    assert sum(r['uses_parity_after_second_extra_edge_read'] for r in class_rows)==1
    # Explicit sound policy transport for EVERY realizable count vector (not
    # just one member per orbit). Full 609376 canonical hidden edge states.
    transported=0;parity_transport=0;lengths=Counter();group_sizes=Counter()
    for count in sorted(counts):
        first=color_first(count)
        candidate=enumerate_sector(first)
        assert len(candidate)==counts[count]
        court,color,parity_adjust,sigma=transport(count,repmap,courts,maps)
        mapped=[]
        for word,p in candidate:
            new=''.join(color[word[i]] for i in sigma)
            pp=p^parity_adjust
            assert (new,pp) in court.index
            mapped.append((new,pp))
            lengths[len(court.replay(new,pp))]+=1
            transported+=1
            parity_transport+=int(pp!=p)
        assert len(set(mapped))==len(candidate)
        assert set(mapped)==set(court.states),('Transport not surjective',count)
        group_sizes[len(candidate)]+=1
    assert transported==609376
    assert max(lengths)<=8
    hard=next(r for r in class_rows if r['uses_parity_after_second_extra_edge_read'])
    receipt={
        'result':'R14_P86_CONSTRUCTIVE_20_FRAME_EDGE_CORNER_PARITY_DELAYED_POLICY_PASS',
        'model':'P5.1 physical canonical cubie orientations, edge-first-facelet scan on all 12 positions; corner two facelets on each of seven positions in first 14 paired frames',
        'all_realisable_first_edge_color_count_vectors':len(counts),
        'all_source_edge_color_automorphisms_preserving_flip_residue':len(maps),
        'count_vector_orbits':len(orb),
        'orbit_exact_adaptive_no_oracle_depth_histogram':dict(Counter({d:sum(r['color_count_vectors_in_orbit'] for r in class_rows if r['exact_edge_mate_minimax_without_parity']==d) for d in (6,7,8,9)})),
        'hard_count_orbit':hard,
        'hard_orbit_parity_free_depth':8,
        'hard_orbit_parity_delayed_after_two_reads_then_six_possible':True,
        'all_39_orbit_exact_negative_depth_minus_one_proofs':True,
        'all_39_orbit_representative_state_decoders':sum(r['all_representative_states_decoded'] for r in class_rows),
        'all_867_canonical_color_count_profiles_full_bijection_and_decoder_replays':transported,
        'transported_policy_edge_extra_reads_depth_histogram':dict(sorted(lengths.items())),
        'max_additional_edge_reads_after_initial_12':max(lengths),
        'max_full_paired_frames':12+max(lengths),
        'parity_revealed_from_corner_sensor_after_14th_frame':True,
        'physical_corner_schedule':'two ordered local facelets per corner position 0..6 in frames 1..14, eighth corner fixed by the twist and cubie uniqueness laws; later corner reads may repeat a known facelet',
        'corner_chirality_uniqueness_assumption':'must be independently verified on genuine P51 8 original physical corner word orders',
        'paired_slot_access_assumption':'P5.1 legal 18-HTM transitivity of all 24x24=576 paired facelet targets, turns free and frames counted',
        'research_limitation':'Constructive upper h_adaptive<=20 conditional on independent P5.1 geometric corner chirality and 576-pair legal routing checks; does not prove h>=20 or published priority.',
        'orbits':class_rows,
        'elapsed_s':round(time.monotonic()-start,3)
    }
    path=HERE/'R14_P86_CONSTRUCTIVE_20_FRAME_POLICY_RECEIPT.json'
    path.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
    print('RESULT',receipt['result'],'max_frames',receipt['max_full_paired_frames'],
          'orbits',len(orb),'profiles',len(counts),'tested_states',transported,
          'elapsed',receipt['elapsed_s'],flush=True)

if __name__=='__main__':main()
