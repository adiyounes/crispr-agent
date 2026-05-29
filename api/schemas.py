from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AnalyzeRequest(BaseModel):
    gene: str = Field(..., example="BRCA1")
    variant: str = Field(..., example="c.5266dupC")
    variant_id: Optional[int] = Field(
        None,
        description="FK to genomedxvariant table."
    )

class OffTargetResponse(BaseModel):
    chromosome: str
    position: int
    sequence: str
    mismatch_count: int
    in_exon: bool
    near_cancer_gene: bool
    cancer_gene_name : Optional[str]
    site_risk_score: float

class AnalyzeResponse(BaseModel):
    gene: str
    variant: str
    variant_id: Optional[int] = None
    simulation_id: Optional[int] = None
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)

    grna_sequence: Optional[str]
    grna_reasoning: Optional[str]

    off_targets: list[OffTargetResponse]

    risk_score: Optional[float]

    verdict: Optional[str]
    reasoning: Optional[str]

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SimulationSummary(BaseModel):
    simulation_id: int
    gene: str
    variant: str
    grna_sequence: Optional[str]
    verdict: Optional[str]
    risk_score: Optional[float]
    analyzed_at: datetime

class SimulationDetail(SimulationSummary):
    grna_reasoning: Optional[str]
    reasoning: Optional[str]
    off_targets: list[OffTargetResponse]