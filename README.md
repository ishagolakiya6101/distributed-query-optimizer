# Distributed Query Optimizer (DQO-Mini)

A lightweight query execution engine prototype that demonstrates how different query planning strategies—Naive, Heuristic, and optionally AI-based—affect performance. Works on CSV datasets using `pandas`, simulating aspects of modern database optimizers.

---

##  Features

- **JSON-based Query Specifications**  
  Define tables, filters, joins, and projections via JSON format.

- **Predicate Pushdown**  
  Applies filters before joins to shrink intermediate results.

- **Planning Strategies**  
  - **Naive Plan**: Executes joins in specified order.  
  - **Heuristic Plan**: Reorders joins based on estimated filtered sizes to improve efficiency.  
  - **AI Plan (Optional)**: Uses a trained ML model to predict the optimal join plan.

- **Explain Mode**  
  Outputs intermediate table sizes, join order decisions, and other execution details for debugging and analysis.

---

##  Query Execution Flow

1. **Input**: JSON spec defining:
   - Tables (CSV paths)
   - Filters
   - Join relationships
   - Output projection

2. **Load Tables**: Imports CSVs into `pandas` DataFrames.

3. **Predicate Pushdown**: Stores data volume and reduces join input sizes pre-join.

4. **Plan Generation**:
   - **Naive**: Executes joins sequentially as specified.
   - **Heuristic**: Reorders joins strategically based on estimated sizes.
   - **AI**: Optionally applies ML model to predict best plan (if available).

5. **Execution**: Performs joins following chosen plan and applies final projection.

6. **Explain (Optional)**: Reports key intermediate stats and join ordering.

---

##  Example JSON Query Spec

```json
{
  "tables": {
    "customers": "data/customers.csv",
    "orders": "data/orders.csv"
  },
  "filters": {
    "customers": { "country": "US" },
    "orders": { "status": "PAID" }
  },
  "joins": [
    {
      "left": "customers",
      "right": "orders",
      "on": ["id", "customer_id"]
    }
  ],
  "select": ["customers.id", "customers.name", "orders.amount"]
}

## Installation

```bash
git clone https://github.com/ishagolakiya6101/distributed-query-optimizer.git
cd distributed-query-optimizer
pip install -r requirements.txt

## Usage

python run_demo.py \
  --query examples/query1.json \
  --plan heuristic \
  --explain


## Project Structure

distributed-query-optimizer/
│── data/            # Sample CSV datasets
│── examples/        # Example JSON query specs
│── dqo/
│   │── planner.py   # Naive / heuristic / AI planning logic
│   │── executor.py  # Execution engine
│   │── utils.py     # Helper functions
│── run_demo.py      # CLI entrypoint
│── requirements.txt # Required dependencies
│── README.md        # Project documentation (this file)
