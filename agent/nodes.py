from agent.state import AgentState, OffTargetSite
from tools.grna_designer import design_grna as design_grna_tool
from tools.genome_scanner import blast_sequence
from tools.risk_scorer import score_off_target

def design_grna(state: AgentState) -> dict:
    """
    Node 1:
        Design the guide RNA sequence 
    """

    gene = state["gene"]
    variant = state["variant"]

    grna_sequence, grna_reasoning = design_grna_tool(gene, variant)

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

    off_targets = blast_sequence(grna_sequence)

    return {
        "off_targets": off_targets
    }    

def score_sites(state: AgentState) -> dict:
    """
    Node 3:
        Score the on-target and off-target sites
    """

    off_targets = state["off_targets"]
    db = state["db"]

    scored_sites = [score_off_target(site, db) for site in off_targets]

    risk_score = max([site.site_risk_score for site in scored_sites]) if scored_sites else 0.0
    
    return {
        "off_targets": scored_sites,
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