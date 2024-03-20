from collections import namedtuple
from typing import Dict, Iterable, Optional, Tuple, List, Sequence, Iterator

from whatshap.types import PhasingAlgorithm

Variant = namedtuple("Variant", "position allele quality")

class NumericSampleIds:
    def __getitem__(self, sample: str) -> int: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    def freeze(self) -> None: ...
    def inverse_mapping(self) -> Dict[int, str]: ...

class Read:
    def __init__(
        self,
        name: Optional[str] = ...,
        mapq: int = ...,
        source_id: int = ...,
        sample_id: int = ...,
        reference_start: int = ...,
        BX_tag: Optional[str] = ...,
        HP_tag: Optional[int] = ...,
        PS_tag: Optional[int] = ...,
    ): ...
    @property
    def mapqs(self) -> Tuple[int]: ...
    @property
    def name(self) -> str: ...
    @property
    def source_id(self) -> int: ...
    @property
    def sample_id(self) -> int: ...
    @property
    def reference_start(self) -> int: ...
    @property
    def BX_tag(self) -> str: ...
    def __iter__(self) -> Iterator[Variant]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: int) -> Variant: ...
    def __setitem__(self, index: int, variant: Variant): ...
    def __contains__(self, position: int) -> bool: ...
    def add_variant(self, position: int, allele: int, quality: int) -> None: ...
    def add_mapq(self, mapq: int) -> None: ...
    def sort(self) -> None: ...
    def is_sorted(self) -> bool: ...
    def has_BX_tag(self) -> bool: ...
    def HP_tag(self) -> int: ...
    def has_HP_tag(self) -> bool: ...
    def PS_tag(self) -> int: ...
    def has_PS_tag(self) -> bool: ...

class ReadSet:
    def add(self, read: Read) -> None: ...
    def __iter__(self) -> Iterator[Read]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: int) -> Read: ...
    def sort(self) -> None: ...
    def subset(self, reads_to_select: Iterable[int]) -> ReadSet: ...
    def get_positions(self) -> List[int]: ...

class PedigreeDPTable(PhasingAlgorithm):
    def __init__(
        self,
        readset: ReadSet,
        recombcost: Sequence[int],
        pedigree: Pedigree,
        distrust_genotypes: bool = ...,
        positions: Optional[Iterable[int]] = ...,
    ): ...
    def get_super_reads(self) -> Tuple[List[ReadSet], List[int]]: ...
    def get_optimal_cost(self) -> int: ...
    def get_optimal_partitioning(self) -> List[int]: ...

class Pedigree:
    def __init__(self, numeric_sample_ids: NumericSampleIds): ...
    def add_individual(
        self,
        id: str,
        genotypes: Iterable[Genotype],
        genotype_likelihoods: Optional[Iterable[PhredGenotypeLikelihoods]] = ...,
    ) -> None: ...
    def add_relationship(self, father_id: int, mother_id: int, child_id: int) -> None: ...
    @property
    def variant_count(self) -> int: ...
    def genotype(self, sample_id: int, variant_index: int) -> Genotype: ...
    def genotype_likelihoods(
        self, sample_id: int, variant_index: int
    ) -> Optional[PhredGenotypeLikelihoods]: ...
    def __len__(self) -> int: ...

class PhredGenotypeLikelihoods:
    def __init__(self, gl: Iterable[float], ploidy: int = ..., nr_alleles: int = ...): ...
    def __getitem__(self, genotype: Genotype) -> float: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[float]: ...
    def __eq__(self, other) -> bool: ...
    def genotypes(self) -> List[Genotype]: ...

def binomial_coefficient(n: int, k: int) -> int: ...

class Genotype:
    def __init__(self, alleles: List[int]): ...
    def is_none(self) -> bool: ...
    def get_index(self) -> int: ...
    def as_vector(self) -> List[int]: ...
    def is_homozygous(self) -> bool: ...
    def is_diploid_and_biallelic(self) -> bool: ...
    def get_ploidy(self) -> int: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    def __lt__(self, other) -> bool: ...

def get_max_genotype_ploidy() -> int: ...
def get_max_genotype_alleles() -> int: ...

class GenotypeDPTable:
    def __init__(
        self,
        numeric_sample_ids: NumericSampleIds,
        readset: ReadSet,
        recombcost: int,
        pedigree: Pedigree,
        positions: Optional[Iterable[int]] = ...,
    ): ...
    def get_genotype_likelihoods(self, sample_id: int, pos: int) -> PhredGenotypeLikelihoods: ...

def compute_genotypes(
    readset: ReadSet, positions: Optional[Iterable[int]] = ...
) -> Tuple[List[Genotype], List[Tuple[float, float, float]]]: ...

class HapChatCore(PhasingAlgorithm):
    def __init__(self, readset: ReadSet): ...
    def get_length(self) -> int: ...
    def get_super_reads(self) -> Tuple[List[ReadSet], Optional[List[int]]]: ...
    def get_optimal_cost(self) -> int: ...
    def get_optimal_partitioning(self) -> List[int]: ...

class Caller:
    def __init__(self, reference: str, k: int, window: int): ...
    def all_variants(self, variants_list: List[Tuple[int, int]]): ...
    def add_read(
        self,
        bam_alignment_pos: int,
        bam_alignment_cigartuples: List[List[int]],
        bam_alignment_query: str,
        outfile: str,
    ): ...
    def final_pop(self, outfile: str): ...
    def finish(self): ...

class PedMecHeuristic(PhasingAlgorithm):
    def __init__(
        self,
        readset: ReadSet,
        recombcost: Sequence[int],
        pedigree: Pedigree,
        row_limit: Optional[int] = ...,
        distrust_genotypes: bool = ...,
        positions: Optional[Iterable[int]] = ...,
        allow_mutations: Optional[bool] = ...,
        verbosity: Optional[int] = ...,
    ): ...
    def get_super_reads(self) -> Tuple[List[ReadSet], Optional[List[int]]]: ...
    def get_opt_transmission(self) -> List[int]: ...
    def get_optimal_cost(self) -> int: ...
    def get_optimal_partitioning(self) -> List[int]: ...
    def get_mutations(self) -> List[List[Tuple[int, int]]]: ...
    def solve(self): ...
