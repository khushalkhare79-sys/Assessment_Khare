from src.clean_suppliers import clean_suppliers
from src.rfq_similarity import enrich_rfq, compute_similarity

if __name__ == "__main__":
    # Question 1
    inventory = clean_suppliers("data/supplier_data1.xlsx", "data/supplier_data2.xlsx",
                                "output/inventory_dataset.csv")

    # Question 2
    enriched = enrich_rfq("data/rfq.csv", "data/reference_properties.tsv")
    top3 = compute_similarity(enriched)
    top3.to_csv("output/top3.csv", index=False)
    print("Top-3 similarity results saved to outputs/top3.csv")