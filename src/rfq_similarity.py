import pandas as pd
import numpy as np
from itertools import product
from src.utils import parse_range
from src.utils import safe_mid

def normalize_grade(g):
    if pd.isna(g): return None
    return str(g).strip().upper()

def enrich_rfq(rfq_file, ref_file):
    rfq = pd.read_csv(rfq_file)
    ref = pd.read_csv(ref_file, sep="\t")

    rfq["grade_norm"] = rfq["grade"].apply(normalize_grade)
    ref["Grade/Material"] = ref["Grade/Material"].apply(normalize_grade)

    # Parse tensile strength ranges
    ref[["Rm_min", "Rm_max"]] = ref["Tensile strength (Rm)"].apply(
        lambda x: pd.Series(parse_range(x))
    )

    enriched = rfq.merge(ref, left_on="grade_norm", right_on="Grade/Material", how="left")
    return enriched

def interval_overlap(min1, max1, min2, max2):
    if pd.isna(min1) or pd.isna(max1) or pd.isna(min2) or pd.isna(max2):
        return 0
    inter = max(0, min(max1, max2) - max(min1, min2))
    union = max(max1, max2) - min(min1, min2)
    return inter / union if union > 0 else 0

def compute_similarity(df):
    results = []
    for i, j in product(range(len(df)), repeat=2):
        if i == j:
            continue
        r1, r2 = df.iloc[i], df.iloc[j]

        # Dimension similarity (IoU)
        dim_sim = 0.5 * interval_overlap(r1["thickness_min"], r1["thickness_max"],
                                         r2["thickness_min"], r2["thickness_max"]) \
                + 0.5 * interval_overlap(r1["width_min"], r1["width_max"],
                                         r2["width_min"], r2["width_max"])

        # Categorical
        cat_sim = int(r1["form"] == r2["form"]) + int(r1["coating"] == r2["coating"])
        cat_sim /= 2.0

        # Grade similarity
        g1 = safe_mid(r1.get("Rm_min"), r1.get("Rm_max"))
        g2 = safe_mid(r2.get("Rm_min"), r2.get("Rm_max"))

        if pd.notna(g1) and pd.notna(g2) and g1 > 0 and g2 > 0:
            grade_sim = 1 - abs(g1 - g2) / max(g1, g2)
        else:
            grade_sim = 0

        score = 0.4 * dim_sim + 0.3 * cat_sim + 0.3 * grade_sim
        results.append((r1["id"], r2["id"], score))

    sim_df = pd.DataFrame(results, columns=["rfq_id", "match_id", "similarity_score"])
    top3 = sim_df.sort_values("similarity_score", ascending=False) \
        .groupby("rfq_id", group_keys=False) \
        .head(3)
    return top3