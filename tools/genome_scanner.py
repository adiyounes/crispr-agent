from Bio.Blast import NCBIWWW, NCBIXML
from agent.state import OffTargetSite


def blast_sequence(grna_sequence) -> list:
    
    result_handle = NCBIWWW.qblast(
        "blastn",
        "nt",
        grna_sequence,
        entrez_query = "Homo sapiens[Organism]",
        hitlist_size = 20
    )
    
    blast_records = NCBIXML.parse(result_handle)
    
    record = next(blast_records)

    off_targets = []

    for alignment in record.alignments:
            
        chrom = alignment.title.split("chromosome")[-1].strip().split()[0]
        chromosome = f"chr{chrom}"
            
        for hsp in alignment.hsps:
            
            if hsp.expect > 0.01:
                continue
            
            position = hsp.sbjct_start
            sequence = hsp.sbjct
            mismatches = hsp.align_length - hsp.identities
            
            off_targets.append(OffTargetSite(
                chromosome = chromosome,
                position = position,
                sequence = sequence,
                mismatch_count = mismatches,
                in_exon = False,
                near_cancer_gene = False,
                cancer_gene_name = None,
                site_risk_score = 0.0
            ))



    return off_targets
