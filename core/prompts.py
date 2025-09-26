from langchain.prompts import PromptTemplate

query_generation_prompt = PromptTemplate.from_template("""
You are an expert SQL developer.
Given the following SQLite database schema and a natural language question, generate a syntactically valid SQL query that answers the question.

Schema:
users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, is_active INTEGER NOT NULL, created_at TEXT NOT NULL)
products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL)
orders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_status TEXT NOT NULL, order_date TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(product_id) REFERENCES products(id)

Only use the tables and columns that appear in the schema above.
Avoid making assumptions about table or column names.
Use only valid SQLite SQL syntax.

**When comparing text fields (such as names or emails), always make the comparison case-insensitive by using COLLATE NOCASE or by applying the LOWER() function to both sides of the comparison.** This ensures user queries work regardless of capitalization.

Question: {input}

SQL Query:
""")

query_validation_prompt = PromptTemplate.from_template("""
You are a meticulous SQL validator.
Check the provided SQL query for common mistakes, including:
- Syntax errors
- Use of non-existent columns or tables
- SQL injection risks
- Incorrect joins, where clauses, or aggregations
- SQLite dialect mismatches

**If string comparison fields (e.g., names, emails) are present in WHERE clauses, ensure the query uses case-insensitive comparison such as COLLATE NOCASE or LOWER(). If the query is case-sensitive, rewrite it to be case-insensitive.**

If you spot an issue, rewrite the query so it is valid for the schema and dialect below.
Do not return explanations—just the validated query.

Schema:
users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, is_active INTEGER NOT NULL, created_at TEXT NOT NULL)
products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL)
orders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_status TEXT NOT NULL, order_date TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(product_id) REFERENCES products(id)

Dialect: SQLite

Original SQL Query:
{query}

Validated and (if needed) corrected SQL Query:
""")


result_formatting_prompt = PromptTemplate.from_template("""
You are an assistant helping users understand database results.
- Only use the data in {results} to answer the user's question.
- Write your reply in clear, natural language suitable for non-technical users.
- Do NOT mention or reference the SQL query, code, database structure, or how the answer was found.
- If the result is a single value, state it directly and naturally (e.g., "Robert Kim's email address is robert.kim@freelancer.net.").
- If there are multiple results, present them as a simple sentence, a readable list, or a plain table—whichever feels easiest to understand.
- Never repeat, copy, or explain any technical details.

Data: {results}
""")

