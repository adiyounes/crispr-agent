from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from agent.graph import app as graph_app
from api.schemas import AnalyzeRequest, AnalyzeResponse, ErrorResponse, OffTargetResponse
from db.session import get_db
from db.models import CrisprOffTarget, CrisprSimulation
from datetime import datetime


router = APIRouter()

@router.post("/analyze")
async def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    result = graph_app.invoke({
        "gene": request.gene,
        "variant": request.variant,
        "variant_id": request.variant_id,
        "off_targets": [],
        "grna_sequence": None,
        "grna_reasoning": None,
        "verdict": None,
        "risk_score": None,
        "reasoning": None,
        "db": db
    })

    simulation = CrisprSimulation(
        gene = result["gene"],
        variant = result["variant"],
        grna_sequence = result["grna_sequence"],
        grna_reasoning = result["grna_reasoning"],
        verdict = result["verdict"],
        risk_score = result["risk_score"],
        reasoning = result["reasoning"],
        analyzed_at = datetime.utcnow(),
        variant_id = request.variant_id,
    )


    db.add(simulation)

    db.commit()
    db.refresh(simulation)

    for off_target in result["off_targets"]:
        ot = CrisprOffTarget(
            simulation_id=simulation.simulation_id,
            chromosome=off_target.chromosome,
            position=off_target.position,
            sequence=off_target.sequence,
            mismatch_count=off_target.mismatch_count,
            in_exon=off_target.in_exon,
            near_cancer_gene=off_target.near_cancer_gene,
            cancer_gene_name=off_target.cancer_gene_name,
            site_risk_score=off_target.site_risk_score
        )
        db.add(ot)
    db.commit()

    return AnalyzeResponse(
        gene=result["gene"],
        variant=result["variant"],
        grna_sequence=result["grna_sequence"],
        grna_reasoning=result["grna_reasoning"],
        verdict=result["verdict"],
        risk_score=result["risk_score"],
        reasoning=result["reasoning"],
        off_targets=[OffTargetResponse(
            chromosome=ot.chromosome,
            position=ot.position,
            sequence=ot.sequence,
            mismatch_count=ot.mismatch_count,
            in_exon=ot.in_exon,
            near_cancer_gene=ot.near_cancer_gene,
            cancer_gene_name=ot.cancer_gene_name,
            site_risk_score=ot.site_risk_score
        ) for ot in result["off_targets"]]
    ) 