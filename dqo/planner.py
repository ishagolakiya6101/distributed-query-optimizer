from __future__ import annotations
import pandas as pd
from typing import Dict, List, Any, Tuple

def estimate_filter_selectivity(df: pd.DataFrame, filters: Dict[str, Any]) -> float:
    """Very rough selectivity estimate for equality filters"""
    if not filters:
        return 1.0
    sel = 1.0
    for col, val in filters.items():
        if col in df.columns:
            # P(col == val) ~ 1 / n_unique(col)
            nuniq = df[col].nunique(dropna=False)
            if nuniq > 0:
                sel *= 1.0 / nuniq
    return max(sel, 1e-9)

def choose_join_order(dfs: Dict[str, pd.DataFrame], joins: List[Dict[str, Any]], filters: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Heuristic: sort joins by ascending estimated output size of the partial join.
    For each join (A join B on A.k = B.k):
      est_size(A) = |A| * selectivity(A)
      est_size(B) = |B| * selectivity(B)
      est_join = min(est_size(A), est_size(B))  # cheap heuristic assuming key uniqueness on one side
    """
    def est_table_size(tname: str) -> float:
        df = dfs[tname]
        sel = estimate_filter_selectivity(df, filters.get(tname, {}))
        return len(df) * sel

    scored = []
    for j in joins:
        a, b = j["left"], j["right"]
        score = min(est_table_size(a), est_table_size(b))
        scored.append((score, j))

    # Smaller estimated result first
    scored.sort(key=lambda x: x[0])
    return [j for _, j in scored]