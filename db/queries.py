from sqlalchemy.orm import Session
from sqlalchemy import text

def in_exon(db: Session, chrom: str, pos: int) -> bool:
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM exon_coordinates
            WHERE chromosome = :chrom
              AND start_pos <= :pos
              AND end_pos >= :pos)""")
    result = db.execute(query, {"chrom": chrom, "pos": pos}).scalar()
    return result

def is_near_clinvar_pathogenic(db: Session, chrom: str, pos: int) -> bool:
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM clinvar_annotations
            WHERE chromosome = :chrom
            AND position = :pos
            AND clinical_significance ILIKE '%Pathogenic%'
        )
    """)
    return db.execute(query, {"chrom": chrom, "pos": pos}).scalar()

def get_nearby_cancer_genes(db: Session, chrom: str, pos: int, distance: int = 50000) -> list:
    query = text("""
        SELECT gene_name
        FROM gene_coordinates
        WHERE chromosome = :chrom
        AND start_pos - :distance <= :pos
        AND end_pos + :distance >= :pos
        AND gene_name IN ('TP53', 'BRCA1', 'BRCA2', 'KRAS', 'PTEN', 'RB1', 'APC', 'MLH1')
    """)
    result = db.execute(query, {"chrom": chrom, "pos": pos, "distance": distance}).fetchall()
    return [row[0] for row in result]