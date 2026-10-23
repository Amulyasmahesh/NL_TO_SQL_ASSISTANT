# Natural-Language-to-SQL Business Intelligence Assistant

A chat app that lets a non-technical user ask questions about an e-commerce database. The goal is to turn a plain-English question into SQL, run it safely, and show the result as a table.

## Status

- [x] Load the Olist dataset into a SQLite database
- [x] Safe query runner (SELECT-only, read-only connection)
- [x] Streamlit chat interface (currently runs SQL typed by hand)
- [x] LLM text-to-SQL module written (`sql_assistant.py`)
- [ ] LLM module tested end to end
- [ ] Evaluation on a hand-checked question set (accuracy results will go here)

## How it works

1. The user asks a question in the chat.
2. The app sends the question and the database schema to an LLM, which returns one SQL query.
3. The query is checked by a safety layer.
4. The query runs on a read-only database connection.
5. The app shows the SQL and the result table.

## Safety

- Only a single `SELECT` (or `WITH`) statement is allowed.
- Queries containing keywords like `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER` and `PRAGMA` are blocked.
- The database is opened in read-only mode, so even a bad query cannot change the data.

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle). It is split into several related tables (orders, customers, items, payments, reviews, products, sellers, category translations), which makes it good for testing joins.

The data files are not included in this repository. Download them from Kaggle and put the CSVs in a `data/` folder.

## Tech stack

Python, SQLite, pandas, Streamlit, OpenAI API (for the LLM step)

## Project structure

```
load_data.py       # loads the CSVs into olist.db
query_runner.py    # safety checks + read-only query execution
sql_assistant.py   # schema reader + LLM text-to-SQL
app.py             # Streamlit chat interface
requirements.txt   # dependencies
```

## Setup

```bash
git clone <your-repo-url>
cd nl_to_sql_assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Download the dataset from Kaggle and put the CSV files in a `data/` folder.
2. Build the database:
   ```bash
   python load_data.py
   ```
3. For the LLM step, create a `.env` file containing `OPENAI_API_KEY=your_key`.
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Limitations

- The LLM step has not been evaluated yet, so generated SQL may be wrong. Results should be checked before being trusted.
- The safety layer uses keyword checks plus a read-only connection. It is a reasonable first defence, not a complete security solution.

## Next steps

- Write 15-20 test questions with hand-checked answers and measure how often the generated SQL is correct.
- Record failure cases and improve the prompt based on them.
- Add support for follow-up questions.

  Python, SQLite, pandas, Streamlit, [OpenAI API](https://platform.openai.com/) (LLM for text-to-SQL)
