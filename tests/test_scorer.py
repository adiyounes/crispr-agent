import pytest
import tools
from tools.risk_scorer import score_off_target, mismatch_to_score
from unittest.mock import MagicMock, patch


def test_mismatch_zero():
    assert mismatch_to_score(0) == 1.0

def test_mismatch_one():
    assert mismatch_to_score(1) == 0.75

def test_mismatch_two():
    assert mismatch_to_score(2) == 0.5

def test_mismatch_three():
    assert mismatch_to_score(3) == 0.25

def test_mismatch_four():
    assert mismatch_to_score(4) == 0.0

def test_score_off_target_high_risk():
    from agent.state import OffTargetSite
    site = OffTargetSite(
        chromosome = 'chr17',
        position = 43026543,
        sequence = 'ACTGATCAGTACTTAGGGCAGT',
        mismatch_count = 0,
        in_exon=False,
        near_cancer_gene=False,
        cancer_gene_name=None,
        site_risk_score=0.0
    )

    with patch('tools.risk_scorer.in_exon', return_value=False), \
         patch('tools.risk_scorer.get_nearby_cancer_genes', return_value=['BRCA1']), \
         patch('tools.risk_scorer.is_near_clinvar_pathogenic', return_value=True):
        
        db = MagicMock()
        result = score_off_target(site, db)

        assert result.site_risk_score == 1.0

def test_score_off_target_high_risk():
    from agent.state import OffTargetSite
    site = OffTargetSite(
        chromosome = 'chr17',
        position = 43026543,
        sequence = 'ACTGATCAGTACTTAGGGCAGT',
        mismatch_count = 4,
        in_exon=False,
        near_cancer_gene=False,
        cancer_gene_name=None,
        site_risk_score=0.0
    )

    with patch('tools.risk_scorer.in_exon', return_value=False), \
         patch('tools.risk_scorer.get_nearby_cancer_genes', return_value=[]), \
         patch('tools.risk_scorer.is_near_clinvar_pathogenic', return_value=True):
        
        db = MagicMock()
        result = score_off_target(site, db)

        assert result.site_risk_score == 0.0