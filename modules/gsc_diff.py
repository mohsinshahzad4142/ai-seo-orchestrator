from typing import List, Dict, Any
import pandas as pd

def calculate_gsc_position_diff(
    baseline_df: pd.DataFrame, current_df: pd.DataFrame, position_threshold: float = 3.0
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Merge baseline and current GSC query-level metrics and detect position shifts.
    Expected columns: ['query', 'clicks', 'impressions', 'ctr', 'position']
    """
    merged = pd.merge(
        baseline_df, current_df, on="query", suffixes=("_base", "_curr"), how="inner"
    )

    # Positive diff means rank improved (moved up closer to position 1)
    merged["pos_diff"] = merged["position_base"] - merged["position_curr"]

    ranked_up = merged[merged["pos_diff"] >= position_threshold].sort_values(by="pos_diff", ascending=False)
    deranked = merged[merged["pos_diff"] <= -position_threshold].sort_values(by="pos_diff", ascending=True)

    return {
        "ranked_up": ranked_up[["query", "position_base", "position_curr", "pos_diff", "clicks_curr"]].to_dict(orient="records"),
        "deranked": deranked[["query", "position_base", "position_curr", "pos_diff", "clicks_curr"]].to_dict(orient="records"),
    }