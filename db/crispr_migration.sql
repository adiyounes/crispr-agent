CREATE TABLE IF NOT EXISTS crispr_simulations (
    simulation_id SERIAL PRIMARY KEY,
    gene VARCHAR(255) NOT NULL,
    variant VARCHAR(255) NOT NULL,
    grna_sequence TEXT,
    grna_reasoning TEXT,
    verdict VARCHAR(10),
    risk_score DOUBLE PRECISION,
    reasoning TEXT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    variant_id INT REFERENCES variants(variant_id) ON DELETE CASCADE,
    upload_id INT REFERENCES vcf_uploads(upload_id) ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_crispr_simulations_gene ON crispr_simulations(gene);
CREATE INDEX IF NOT EXISTS idx_crispr_simulations_variant ON crispr_simulations(variant_id);