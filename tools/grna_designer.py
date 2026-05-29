import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def design_grna(gene: str, variant: str) -> tuple:
    prompt = f"""
        You are a grna designer.
        
        Given 
        - Gene:{gene}
        - Variant:{variant}
        
        design a grna sequence that can be used
        to target the variant for CRISPR editing. Provide a brief
        reasoning for your choice of grna sequence.

        RULES:
        - PAM site: the sequence must end with NGG
        - GC content: between 40% and 70%
        - Uniqueness: the sequence should not match too many other
            places in the genome to minimize off-targets
        
        Return oyur answer in JSON format with exactly two fileds:
        -grna_sequence
        -reasoning
    """

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    if not raw:
        raise ValueError("Empty response from Anthropic API")
     
    data = json.loads(raw)

    if "grna_sequence" not in data or "reasoning" not in data:
        raise ValueError(f"Invalid response format: {raw}") 

    return (data["grna_sequence"], data["reasoning"])