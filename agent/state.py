from typing import TypedDict, Optional
from dataclasses import dataclass, field

@dataclass
class OffTargetSite:
    chromosome: str
    position: int
    sequence: str
    mismatch_count: int
    in_exon: bool
    near_cancer_gene: bool
    cancer_gene_name: Optional[str]
    site_risk_score: float

class AgentState(TypedDict):
    gene: str
    variant:str
    variant_id: Optional[str]

    grna_sequence: Optional[str]
    grna_reasoning: Optional[str]

    off_targets: list[OffTargetSite]

    risk_score: Optional[float]

    verdict: Optional[str]
    reasoning: Optional[str]

    