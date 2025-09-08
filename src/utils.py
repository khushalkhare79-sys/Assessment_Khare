import re
import numpy as np
import pandas as pd


def parse_range(val):
    if pd.isna(val):
        return (np.nan, np.nan)
    s = str(val).replace("≤", "").replace("≥", "")
    nums = re.findall(r"[\d\.]+", s)
    if len(nums) == 1:
        return (float(nums[0]), float(nums[0]))
    elif len(nums) >= 2:
        return (float(nums[0]), float(nums[1]))
    return (np.nan, np.nan)


# Return midpoint of min/max if available
def safe_mid(val_min, val_max):
    if pd.isna(val_min) and pd.isna(val_max):
        return np.nan
    if pd.isna(val_min):
        return val_max
    if pd.isna(val_max):
        return val_min
    return (val_min + val_max) / 2
