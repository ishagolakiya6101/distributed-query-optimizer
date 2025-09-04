# Distributed Query Optimizer (DQO-Mini)

A lightweight query execution engine prototype that demonstrates how different query planning strategies—Naive, Heuristic, and optionally AI-based—affect performance. Works on CSV datasets using `pandas`, simulating aspects of modern database optimizers.

---

## Features

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

## Query Execution Flow

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

## Installation

```bash
git clone https://github.com/ishagolakiya6101/distributed-query-optimizer.git
cd distributed-query-optimizer
pip install -r requirements.txt
