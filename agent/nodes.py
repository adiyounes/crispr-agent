from agent.state import AgentState, OffTargetSite

def design_grna(state: AgentState) -> dict:
    """
    Node 1:
        Design the guide RNA sequence 
    """

    gene = state["gene"]
    variant = state["variant"]

    grna_sequence = "AGCTTAGCTAGCTAGCTAGC"
    grna_reasoning = f"stub gRNA designed for {gene}  {variant}"

    return {
        "grna_sequence": grna_sequence,
        "grna_reasoning": grna_reasoning
    }

def scan_genome(state: AgentState) -> dict:
    """
    Node 2:
        Scan the genome for potential off-target sites
    """

    grna_sequence = state["grna_sequence"]

    off_targets = [
        OffTargetSite(
            chromosome="chr1",
            position=123456,
            sequence="AGCTTAGCTAGCTAGCTAGT",
            mismatch_count=1,
            in_exon=True,
            near_cancer_gene=True,
            cancer_gene_name="TP53",
            site_risk_score=0.8
        ),
        OffTargetSite(
            chromosome="chr2",
            position=789012,
            sequence="AGCTTAGCTAGCTAGCTAGG",
            mismatch_count=2,
            in_exon=False,
            near_cancer_gene=False,
            cancer_gene_name=None,
            site_risk_score=0.3
        )
    ]

    return {
        "off_targets": off_targets
    }    

def score_sites(state: AgentState) -> dict:
    """
    Node 3:
        Score the on-target and off-target sites
    """

    off_targets = state["off_targets"]

    risk_score = max([site.site_risk_score for site in off_targets])

    return {
        "off_targets": off_targets,
        "risk_score": risk_score
    }

def make_verdict (state: AgentState) -> dict:
    """
    Node 4:
        Make a final verdict on whether to proceed with the designed gRNA
    """

    risk_score = state["risk_score"]

    if risk_score < 0.3:
        verdict = "safe"
        reasoning = "Low overall risk. Off-target sites are minimal and non-critical."
    elif risk_score < 0.7:
        verdict = "caution"
        reasoning = "Moderate risk detected. Review off-target sites before proceeding."
    else:
        verdict = "unsafe"
        reasoning = "High risk. Critical off-target sites detected near coding regions or cancer genes."

    return {
        "verdict": verdict,
        "reasoning": reasoning
    }