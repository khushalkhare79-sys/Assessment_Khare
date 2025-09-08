import pandas as pd
import numpy as np
import re

def parse_number(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, str):
        nums = re.findall(r"[\d\.]+", x)
        return float(nums[0]) if nums else np.nan
    return float(x)

def clean_suppliers(file1, file2, output_path):
    # Load
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Clean df1
    df1.rename(columns={
        "Quality/Choice": "quality",
        "Grade": "grade",
        "Finish": "finish",
        "Thickness (mm)": "thickness_mm",
        "Width (mm)": "width_mm",
        "Description": "description",
        "Gross weight (kg)": "weight_kg",
        "Quantity": "quantity",
        "RP02": "rp02",
        "RM": "rm",
        "AG": "ag",
        "AI": "ai"
    }, inplace=True)

    df1["thickness_mm"] = df1["thickness_mm"].apply(parse_number)
    df1["width_mm"] = df1["width_mm"].apply(parse_number)
    df1["weight_kg"] = df1["weight_kg"].apply(parse_number)

    df1["material"] = df1["grade"]
    df1["article_id"] = None
    df1["reserved"] = False
    df1["supplier"] = "supplier1"

    # Clean df2
    df2.rename(columns={
        "Material": "material",
        "Description": "description",
        "Article ID": "article_id",
        "Weight (kg)": "weight_kg",
        "Quantity": "quantity",
        "Reserved": "reserved"
    }, inplace=True)

    for col in ["quality", "grade", "finish"]:
        df2[col] = pd.Series(dtype="object")  # text

    for col in ["thickness_mm", "width_mm", "rp02", "rm", "ag", "ai"]:
        df2[col] = pd.Series(dtype="float")  # numeric
    df2["supplier"] = "supplier2"

    # Merge
    common_cols = ["supplier", "article_id", "material", "quality", "grade", "finish",
                   "thickness_mm", "width_mm", "description", "weight_kg", "quantity",
                   "reserved", "rp02", "rm", "ag", "ai"]

    df1 = df1[common_cols]
    df2 = df2[common_cols]

    inventory = pd.concat([df1, df2], ignore_index=True)

    # Normalize text
    for col in ["material", "grade", "finish", "quality", "description"]:
        inventory[col] = inventory[col].astype(str).str.strip().str.lower().replace("nan", np.nan)

    inventory.to_csv(output_path, index=False)
    print(f"Inventory dataset saved to {output_path}")
    return inventory
