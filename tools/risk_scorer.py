from sqlalchemy.orm import Session
from agent.state import OffTargetSite
import db
from db.queries import in_exon, get_nearby_cancer_genes, is_near_clinvar_pathogenic


def mismatch_to_score(mismatch_count: int) -> float:
    if mismatch_count == 0:
        return 1.0
    elif mismatch_count == 1:
        return 0.75
    elif mismatch_count == 2:
        return 0.5
    elif mismatch_count == 3:
        return 0.25
    else:
        return 0.0


def score_off_target(site: OffTargetSite, db: Session) -> OffTargetSite:


    mismatch_score = mismatch_to_score(site.mismatch_count)

    in_exon_result = in_exon(db, site.chromosome, site.position)
    context_penalty = 1.0 if in_exon_result else 0.0

    nearby_genes = get_nearby_cancer_genes(db, site.chromosome, site.position)
    cancer_proximity = 1.0 if nearby_genes else 0.0

    site.site_risk_score = (
        (mismatch_score   * 0.5) +
        (context_penalty  * 0.3) +
        (cancer_proximity * 0.2)
    )

    site.in_exon = in_exon
    site.near_cancer_gene = bool(nearby_genes)
    site.cancer_gene_name = nearby_genes[0] if nearby_genes else None

    return site