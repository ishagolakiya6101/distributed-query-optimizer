
---

## 🔄 Query Execution Flow

1. **Input Query Spec (JSON)**  
   - Defines tables, filters, joins, and projection.

2. **Load Tables**  
   - CSVs are read into pandas DataFrames.

3. **Predicate Pushdown**  
   - Filters applied before joins to shrink table sizes.

4. **Plan Generation**  
   - **Naive Plan**: executes joins in given order.  
   - **Heuristic Plan**: reorders joins based on estimated filtered sizes.  
   - **AI Plan (optional)**: uses trained ML model to predict best plan.

5. **Execution**  
   - Joins are executed according to chosen plan.  
   - Results are projected to selected columns.

6. **Explain Plan (Optional)**  
   - Prints table sizes after filtering, and join orders chosen.

---

## 📊 Example Query Spec

```json
{
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
