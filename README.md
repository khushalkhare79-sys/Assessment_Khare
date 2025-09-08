Vanilla Steel - Junior Data Scientist Assessment

The solution covers two scenarios:

1. Supplier Data Cleaning - unify two messy supplier Excel datasets into a single clean inventory.
2. RFQ Similarity - enrich RFQs with reference grade properties and compute similarity between RFQs.

Repository Structure

Assessment_Khare/
│
├── data/ 
│ ├── supplier_data1.xlsx
│ ├── supplier_data2.xlsx
│ ├── rfq.csv
│ ├── reference_properties.tsv
│
├── output/
│ ├── inventory_dataset.csv # Scenario A result
│ ├── top3.csv # Scenario B result
│
├── src/
│ ├── clean_suppliers.py # Cleans and merges supplier files
│ ├── rfq_similarity.py # RFQ enrichment + similarity
│ ├── utils.py # Shared helper functions
│
├── run.py
├── requirements.txt
└── README.md

1. Setup
Clone the repository and install dependencies:
git clone <your_repo_url>
cd Assessment_Khare
pip install -r requirements.txt

2. Running the pipeline
python run.py
This will:
- Clean and merge supplier datasets → outputs/inventory_dataset.csv
- Enrich RFQs with reference properties
- Compute similarities between RFQs
- Export top-3 matches per RFQ → outputs/top3.csv

3. Deliverables
- inventory_dataset.csv:
A unified supplier inventory with standardized schema:
  supplier (source file indicator)
  article_id
  material
  quality
  grade
  finish
  thickness_mm
  width_mm
  description
  weight_kg
  quantity
  reserved
  rp02, rm, ag, ai

Missing or inconsistent values were normalized (numeric parsing, lowercased text, NaN for missing).

- top3.csv:
Contains the top-3 most similar RFQs per RFQ line, with columns:
rfq_id: the original RFQ
match_id: the most similar RFQ candidate
similarity_score: aggregated similarity (0–1)
Since there are 1000 RFQs in the input, the output contains 3000 rows (1000 × 3 matches each)

4. Methodology:
- Supplier Cleaning
- Standardized numeric values (thickness_mm, width_mm, weight_kg)
- Normalized text (lowercase, trimmed)
- Unified schema across both supplier files
- Concatenated into one dataset


5. RFQ Similarity:
- Reference join: Normalized grades, joined RFQs with grade-level reference properties
- Feature engineering:
- Dimensions → intervals with IoU overlap metric
- Categoricals → exact match (1/0)
- Grade properties → numeric midpoints (e.g. tensile strength)
- Similarity score: weighted average
- similarity = 0.4 * dimension_overlap
           + 0.3 * categorical_match
           + 0.3 * grade_similarity
For each RFQ: selected top-3 matches (excluding self)


Author
Prepared by: Khushal Khare
