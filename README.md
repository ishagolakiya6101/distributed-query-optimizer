🗂️ Distributed Query Optimizer (DQO-Mini)

A lightweight distributed query optimizer prototype that demonstrates how different query execution strategies (Naive, Heuristic, and optional AI-based) affect performance.
It operates on CSV-based datasets using pandas and simulates query planning similar to modern database optimizers.

🚀 Features

JSON-based Query Specs
Define tables, filters, joins, and projections in a simple JSON format.

Predicate Pushdown
Applies filters before joins to reduce intermediate table sizes.

Multiple Planning Strategies

Naive Plan: Executes joins in the specified order.

Heuristic Plan: Reorders joins based on estimated filtered sizes.

AI Plan (Optional): Uses a trained ML model to predict the best plan.

Explain Plan
Shows intermediate table sizes, chosen join orders, and other insights.

🔄 Query Execution Flow

Input Query Spec (JSON)

Defines tables, filters, joins, and projection.

Load Tables

CSVs are read into pandas DataFrames.

Predicate Pushdown

Filters applied before joins to shrink table sizes.

Plan Generation

Naive Plan: executes joins in given order.

Heuristic Plan: reorders joins based on estimated filtered sizes.

AI Plan (optional): uses trained ML model to predict best plan.

Execution

Joins are executed according to chosen plan.

Results are projected to selected columns.

Explain Plan (Optional)

Prints table sizes after filtering, and join orders chosen.

📊 Example Query Spec
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

⚙️ Installation
git clone https://github.com/your-username/dqo-mini.git
cd dqo-mini
pip install -r requirements.txt

▶️ Usage

Run a query:

python main.py --query examples/query1.json --plan heuristic --explain


--query: Path to JSON query spec

--plan: naive, heuristic, or ai

--explain: Show intermediate steps and join order

📂 Project Structure
dqo-mini/
│── data/               # Sample CSV datasets
│── examples/           # Example JSON query specs
│── optimizer/          # Query optimizer logic
│   │── planner.py      # Naive / heuristic / AI planners
│   │── executor.py     # Execution engine
│   │── utils.py        # Helper functions
│── main.py             # Entry point
│── requirements.txt    # Dependencies
│── README.md           # Project documentation

🛠️ Roadmap / Future Work

 Add cost-based optimizer with statistics collection.

 Support more join algorithms (hash join, sort-merge join).

 Extend beyond CSV to SQL/Parquet backends.

 Improve AI planner with reinforcement learning.

 Add benchmarking scripts.
