from __future__ import annotations
import pandas as pd
from typing import Dict, List, Tuple, Any
from .planner import choose_join_order, estimate_filter_selectivity

def load_tables(tables: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    dfs = {}
    for name, path in tables.items():
        dfs[name] = pd.read_csv(path)
    return dfs

def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    out = df
    for col, val in (filters or {}).items():
        out = out[out[col] == val]
    return out

def execute_query(query: Dict[str, Any], optimize: bool = True) -> pd.DataFrame:
    tables = query["tables"]
    filters = query.get("filters", {})
    joins = query.get("joins", [])
    select = query.get("select", [])

    dfs = load_tables(tables)
    for t, f in filters.items():
        dfs[t] = apply_filters(dfs[t], f)

    if optimize:
        order = choose_join_order(dfs, joins, filters)
    else:
        order = joins

    if not order:
        only_table = list(dfs.keys())[0]
        result = dfs[only_table]
    else:
        participating = set()
        for j in joins:
            participating.add(j['left'])
            participating.add(j['right'])
        start_table = min(participating, key=lambda t: len(dfs[t]))
        result = dfs[start_table].copy()
        used_tables = {start_table}

        if start_table not in (order[0]['left'], order[0]['right']):
            for i in range(len(order)):
                if start_table in (order[i]['left'], order[i]['right']):
                    order = [order[i]] + order[:i] + order[i+1:]
                    break

        i = 0
        limit = len(order) + 5  # safety to avoid infinite re-append
        while i < len(order) and i < limit:
            j = order[i]
            l, r = j['left'], j['right']
            lk, rk = j['on']
            if l in used_tables and r in dfs:
                right_df = dfs[r]; left_key, right_key = lk, rk
            elif r in used_tables and l in dfs:
                right_df = dfs[l]; left_key, right_key = rk, lk
            else:
                order.append(j); i += 1; continue

            result = result.merge(right_df, left_on=left_key, right_on=right_key, how='inner')
            used_tables.add(l); used_tables.add(r)
            i += 1

    if select:
        cols = []
        for sc in select:
            if "." in sc:
                _, c = sc.split(".", 1)
            else:
                c = sc
            if c in result.columns:
                cols.append(c)
        if cols:
            result = result[cols]

    return result

def explain(query: Dict[str, Any]) -> Dict[str, Any]:
    tables = query["tables"]
    filters = query.get("filters", {})
    joins = query.get("joins", [])

    dfs = load_tables(tables)
    filtered_sizes = {t: len(apply_filters(df, filters.get(t, {}))) for t, df in dfs.items()}

    plan_optimized = choose_join_order(dfs, joins, filters)
    plan_naive = joins

    return {
        "filtered_sizes": filtered_sizes,
        "naive_plan": plan_naive,
        "optimized_plan": plan_optimized,
    }