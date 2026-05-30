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
    variant_id INT,
    upload_id  INT
);


CREATE INDEX IF NOT EXISTS idx_crispr_simulations_gene ON crispr_simulations(gene);
CREATE INDEX IF NOT EXISTS idx_crispr_simulations_variant ON crispr_simulations(variant_id);

CREATE TABLE IF NOT EXISTS crispr_off_targets (
    off_target_id    SERIAL PRIMARY KEY,
    simulation_id    INT NOT NULL REFERENCES crispr_simulations(simulation_id) ON DELETE CASCADE,
    chromosome       TEXT NOT NULL,
    position         BIGINT NOT NULL,
    sequence         TEXT,
    mismatch_count   INT,
    in_exon          BOOLEAN DEFAULT FALSE,
    near_cancer_gene BOOLEAN DEFAULT FALSE,
    cancer_gene_name TEXT,
    site_risk_score  DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_off_targets_simulation ON crispr_off_targets(simulation_id);
CREATE INDEX IF NOT EXISTS idx_off_targets_position ON crispr_off_targets(chromosome, position);