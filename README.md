# Natural-Language-to-SQL Business Intelligence Assistant

A chat app that lets a non-technical user ask questions about an e-commerce database in plain English. An LLM turns each question into SQL, a safety layer checks the query, and the app runs it and shows the result as a table.

## Status

- [x] Load the Olist dataset into a SQLite database
- [x] Safe query runner (SELECT-only, read-only connection)
- [x] LLM text-to-SQL module, tested on sample questions
- [x] Streamlit chat interface connected to the LLM
- [ ] Evaluation on a hand-checked question set (accuracy results will go here)

## How it works

1. The user asks a question in the chat, for example "What are the top 5 product categories by items sold?"
2. The app reads the database schema (tables, columns, types) automatically.
3. The question and schema are sent to an LLM with rules: use only the given tables, write SQLite syntax, and return a single SELECT query.
4. The query passes through the safety layer.
5. It runs on a read-only database connection.
6. The app shows the generated SQL and the result table.

## LLM details

- **Provider:** Groq, through its OpenAI-compatible API
- **Model:** `openai/gpt-oss-120b` (configurable in `sql_assistant.py`)
- **Prompting:** a system prompt with the full schema and strict output rules, plus a note that product category names are in Portuguese and need the translation table for English names
- **Output cleaning:** markdown fences are stripped so only the SQL is returned

## Safety

- Only a single `SELECT` (or `WITH`) statement is allowed.
- Queries containing `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `PRAGMA` and similar keywords are blocked.
- The database is opened in read-only mode, so even a bad query cannot change the data.
- API keys are stored in a `.env` file that is excluded from git.

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle). It has several related tables (orders, customers, items, payments, reviews, products, sellers, category translations), which makes it good for testing joins. The data files are not included in this repository.

## Tech stack

Python, SQLite, pandas, Streamlit, Groq API (LLM)

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

1. Download the dataset from Kaggle and put the CSVs in a `data/` folder.
2. Build the database: `python load_data.py`
3. Get a free API key from [Groq](https://console.groq.com/keys) and create a `.env` file containing `GROQ_API_KEY=your_key`.
4. Run the app: `streamlit run app.py`


