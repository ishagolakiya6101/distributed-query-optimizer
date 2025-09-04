import time
from dqo.engine import execute_query, explain

query = {
    "tables": {
        "customers": "data/customers.csv",
        "orders": "data/orders.csv"
    },
    "filters": {
        "customers": {"country": "US"},
        "orders": {"status": "PAID"}
    },
    "joins": [
        {"left": "customers", "right": "orders", "on": ["id", "customer_id"]}
    ],
    "select": ["customers.id", "customers.name", "orders.amount"]
}

plan_info = explain(query)
print("Filtered sizes:", plan_info["filtered_sizes"])
print("Naive plan:", plan_info["naive_plan"])
print("Optimized plan:", plan_info["optimized_plan"])

t0 = time.time()
res_naive = execute_query(query, optimize=False)
t1 = time.time()
res_opt = execute_query(query, optimize=True)
t2 = time.time()

print(f"Naive rows: {len(res_naive)} | time: {t1-t0:.4f}s")
print(f"Optimized rows: {len(res_opt)} | time: {t2-t1:.4f}s")

assert set(map(tuple, res_naive.values)) == set(map(tuple, res_opt.values))
print("✅ Result sets are equal (as unordered sets).")
print(res_opt.head().to_string(index=False))