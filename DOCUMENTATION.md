# Junior Data Scientist Assessment  
## Documentation

## 1. Tools & Libraries

The solution was implemented in **Python 3.11** using the following libraries:

- **pandas** – data loading, cleaning, transformation, and joins  
- **numpy** – numerical operations and similarity calculations  
- **openpyxl** – reading Excel files (`.xlsx`)  
- **re (regex)** – parsing numeric values from strings  
- **itertools** – Cartesian product for pairwise similarity comparisons  

Dependencies are listed in `requirements.txt`.

---

## 2. Process Overview

The assessment required solving **two complementary scenarios**:

1. **Supplier Data Cleaning (Scenario A)**  
2. **RFQ Similarity (Scenario B)**  

The pipeline is modular, with separate scripts for each step, orchestrated by `run.py`.

---

## 3. Scenario A – Supplier Data Cleaning

### Objective
Unify two messy supplier Excel datasets into a single clean inventory dataset.

### Input
- `supplier_data1.xlsx`  
- `supplier_data2.xlsx`

### Steps
1. **Load & Inspect** – Read both supplier files into pandas DataFrames.  
2. **Standardize Schema**  
   - Renamed columns to consistent names.  
   - Created missing placeholder columns in each dataset.  
3. **Clean & Normalize**  
   - Parsed numeric values (e.g., `"2.5 mm"` → `2.5`).  
   - Converted text fields to lowercase and trimmed whitespace.  
   - Standardized weight units (all in kilograms).  
4. **Merge**  
   - Concatenated supplier1 and supplier2 into a single dataset.  
   - Added `supplier` column to track origin.  
5. **Export**  
   - Saved unified dataset as `inventory_dataset.csv`.

### Output
- `output/inventory_dataset.csv`  
  → Contains all supplier inventory rows with a clean, standardized schema.

---

## 4. Scenario B – RFQ Similarity

### Objective
Enrich RFQs with grade properties and compute similarity between RFQ lines.

### Input
- `rfq.csv`  
- `reference_properties.tsv`

### Steps
1. **Normalize Grades**  
   - Standardized grade keys (uppercased, trimmed suffixes).  
2. **Reference Join**  
   - Joined RFQs with reference grade properties.  
   - Parsed ranges (e.g., `"200–400 MPa"`) into numeric min/max.  
3. **Feature Engineering**  
   - **Dimensions**: Represented as intervals; overlap calculated using **IoU**.  
   - **Categorical fields**: Coating, form, finish → exact match (1/0).  
   - **Grade properties**: Converted ranges into midpoints (e.g., tensile strength).  
4. **Similarity Calculation**  
   - Defined weighted similarity score:  

     ```
     similarity = 0.4 * dimension_overlap
                + 0.3 * categorical_match
                + 0.3 * grade_similarity
     ```

   - For each RFQ, computed similarity with all others.  
   - Selected **top-3 most similar RFQs** per line (excluding self).  
5. **Export**  
   - Saved results as `top3.csv`.

### Output
- `output/top3.csv`  
  → Each RFQ has exactly 3 matches (`1000 RFQs × 3 = 3000 rows`).

---

## 5. Assumptions

- Units are consistent across suppliers (weights in kg, dimensions in mm).  
- Missing values are preserved as `NaN` rather than imputed, unless required for numeric parsing.  
- Only **tensile strength** was used as the grade-level numeric similarity feature for simplicity, but the pipeline can be extended to other properties (yield strength, hardness, etc.).  
- IoU overlap is the chosen metric for dimensional similarity.  
- Equal weights (0.4 / 0.3 / 0.3) were used; these can be tuned.  

---

## 6. Validation

- `inventory_dataset.csv` row count = rows from supplier1 + supplier2.  
- `top3.csv` row count = 3 × number of RFQs.  
- Each `rfq_id` appears **exactly 3 times**.  
- No self-matches (`rfq_id != match_id`).  
- All similarity scores fall within [0, 1].

---

## 7. Extension Ideas

- **Ablation analysis**: Compare similarity using only dimensions vs. only grade.  
- **Alternative similarity metrics**: Cosine similarity, Jaccard index for categoricals.  
- **Clustering**: Group RFQs into families based on similarity scores.  

---

## 8. Conclusion

This pipeline demonstrates:  
- Data cleaning and normalization across messy supplier files.  
- Enrichment of RFQs with reference properties.  
- Feature engineering and similarity scoring with reproducible results.  
