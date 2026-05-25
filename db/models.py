from sqlalchemy import Column, BigInteger, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CrisprSimulation(Base):
    __tablename__ = "crispr_simulations"

    simulation_id = Column(Integer, primary_key=True, index=True)
    gene = Column(String)
    variant = Column(String)
    grna_sequence = Column(String)
    grna_reasoning = Column(String)
    verdict = Column(String)
    risk_score = Column(Float)
    reasoning = Column(String)
    analyzed_at = Column(DateTime)
    variant_id = Column(Integer, ForeignKey("variants.variant_id"))
    upload_id = Column(Integer, ForeignKey("vcf_uploads.upload_id"))
    off_targets = relationship("CrisprOffTarget", back_populates="simulation")


class CrisprOffTarget(Base):
    __tablename__ = "crispr_off_targets"

    off_target_id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(Integer, ForeignKey("crispr_simulations.simulation_id"))
    chromosome = Column(String)
    position = Column(BigInteger)
    sequence = Column(String)
    mismatch_count = Column(Integer)
    in_exon = Column(Boolean)
    near_cancer_gene = Column(Boolean)
    cancer_gene_name = Column(String)
    site_risk_score = Column(Float)
    simulation = relationship("CrisprSimulation", back_populates="off_targets")


