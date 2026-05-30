# CRISPR Safety Agent
[![Tests](https://github.com/adiyounes/crispr-agent/actions/workflows/tests.yml/badge.svg)](https://github.com/adiyounes/crispr-agent/actions/workflows/tests.yml)

An AI agent that predicts the safety of CRISPR gene edits by identifying 
off-target cut sites across the human genome.

Given a gene name and a pathogenic variant, the agent designs an optimal 
guide RNA sequence, scans the GRCh38 human genome for similar sequences 
that could be accidentally cut, scores each potential off-target site by 
risk, and returns a safety verdict — safe, caution, or unsafe.

## Why it matters

When a clinician considers gene therapy for a patient, the molecular 
scissors (Cas9) can accidentally cut at locations in the genome that look 
similar to the intended target. This is called off-target activity and it 
is the primary safety concern in gene therapy.

This agent helps clinicians decide whether a CRISPR edit is safe enough 
to proceed, or whether they should look for alternative approaches.

## Architecture

The agent is built as a LangGraph graph with four sequential nodes:

1. **design_grna**  calls the Anthropic API to design an optimal 20-nt 
   guide RNA sequence for the given gene and variant
2. **scan_genome**  uses BioPython to run NCBI BLAST against the human 
   genome, finding sequences similar to the gRNA
3. **score_sites**  scores each off-target site using a weighted formula 
   based on mismatch count, exon context, and proximity to cancer genes
4. **make_verdict**  returns a final safety verdict with reasoning

```
Input: gene + variant
↓
[design_grna] → [scan_genome] → [score_sites] → [make_verdict]
↓                                                ↓
gRNA sequence                              safe/caution/unsafe
```

## Risk Scoring Formula

Each off-target site is scored as:
risk = (mismatch_score × 0.5) + (context_penalty × 0.3) + (cancer_proximity × 0.2)

- **mismatch_score**  fewer mismatches = higher risk (0 mismatches = 1.0)
- **context_penalty**  1.0 if cut is inside an exon, 0.0 if intergenic
- **cancer_proximity**  1.0 if within 50kb of TP53, BRCA1, BRCA2, KRAS etc.

Scoring queries your local GRCh38 database  1.5M exons and 40K genes  
with no external API calls.

## Stack

| Layer | Technology |
|-------|-----------|
| AI agent | LangGraph |
| LLM | Anthropic API (claude-sonnet-4) |
| Genome scanning | BioPython + NCBI BLAST |
| API | FastAPI + Pydantic |
| Database | PostgreSQL + SQLAlchemy |
| Reference genome | GRCh38 (local) |

## Setup

```bash
# 1. Clone the repo
git clone git@github.com:adiyounes/crispr-agent.git
cd crispr-agent

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your database credentials and Anthropic API key

# 5. Run the database migration
psql -U your_user -d your_db -f database/crispr_migration.sql

# 6. Start the API
uvicorn main:app --reload
```

## API Usage

**POST** `/api/v1/crispr/analyze`

Request:
```json
{
    "gene": "BRCA1",
    "variant": "c.5266dupC",
    "variant_id": null
}
```

Response:
```json
{
    "gene": "BRCA1",
    "variant": "c.5266dupC",
    "grna_sequence": "GAAGATCAAAAGAATCTAGAGG",
    "grna_reasoning": "This gRNA targets the BRCA1 c.5266dupC region...",
    "verdict": "safe",
    "risk_score": 0.0,
    "reasoning": "Low overall risk. Off-target sites are minimal.",
    "off_targets": []
}
```

## Integration with GenomeDx

This agent is designed to work as a downstream microservice of 
[GenomeDx](https://github.com/adiyounes/genomics-dashboard)  a genomic 
variant analysis platform.

When GenomeDx identifies a pathogenic variant in a patient's VCF file, 
the CRISPR agent assesses whether gene therapy is a safe option:

```
Patient VCF
↓
GenomeDx — variant annotation + ClinVar matching
↓
Pathogenic variant identified (e.g. BRCA1 c.5266dupC)
↓
CRISPR Agent — gRNA design + off-target safety analysis
↓
Safety verdict returned to clinician
```

The `variant_id` field in the request links results back to the 
GenomeDx `variants` table, keeping both systems in sync.