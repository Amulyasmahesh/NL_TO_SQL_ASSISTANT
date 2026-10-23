import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
DB_PATH = "olist.db"
MODEL = "gpt-4.1-mini"  # pick a small, cheap model from OpenAI's models page
client = OpenAI()  # reads OPENAI_API_KEY from .env

SYSTEM_PROMPT = """You are a SQLite expert. Convert the user's question into one SQL query.
Rules:
- Use only the tables and columns in the schema below.
- Write SQLite syntax.
- Return exactly one SELECT query and nothing else (no explanation, no markdown).
- Product category names are in Portuguese; join category_translation on
  product_category_name to get English names.

Schema:
{schema}
"""

def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")]
    lines = []
    for t in tables:
        cols = cur.execute(f"PRAGMA table_info({t})").fetchall()
        lines.append(f"{t}(" + ", ".join(f"{c[1]} {c[2]}" for c in cols) + ")")
    conn.close()
    return "\n".join(lines)

def generate_sql(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(schema=get_schema())},
            {"role": "user", "content": question},
        ],
    )
    sql = response.choices[0].message.content.strip()
    return sql.replace("```sql", "").replace("```", "").strip()

if __name__ == "__main__":
    questions = [
        "How many orders are there in total?",
        "What are the top 5 product categories by number of items sold?",
        "What is the average review score?",
    ]
    for q in questions:
        print("Q:", q)
        print(generate_sql(q))
        print()