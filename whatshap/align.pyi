from collections.abc import Sequence
from typing import Dict, Tuple

def edit_distance(s: str, t: str, maxdiff: int = ...) -> int: ...
def edit_distance_affine_gap(
    query: str, ref: str, mismatch_cost: int, gap_start: int = ..., gap_extend: int = ...
) -> int: ...
def kmer_align(
    seq1: Sequence[int],
    seq2: Sequence[int],
    costs: Dict[Tuple[int, int], float],
    gap_penalty: float,
): ...
def enumerate_all_kmers(reference: bytes, k: int): ...
