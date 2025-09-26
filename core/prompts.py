from langchain.prompts import PromptTemplate

intent_classification_prompt = PromptTemplate.from_template("""
Given the following user request, classify the intended database operation as one of the following:
- "read" (query existing data)
- "create" (add new data)
- "update" (modify existing data)
- "delete" (remove existing data)

User request: {input}

Respond only with one word: read, create, update, or delete.
""")

read_query_generation_prompt = PromptTemplate.from_template("""
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

read_query_validation_prompt = PromptTemplate.from_template("""
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


read_result_formatting_prompt = PromptTemplate.from_template("""
You are an assistant helping users understand database results.
- Only use the data in {results} to answer the user's question.
- Write your reply in clear, natural language suitable for non-technical users.
- Do NOT mention or reference the SQL query, code, database structure, or how the answer was found.
- If the result is a single value, state it directly and naturally (e.g., "Robert Kim's email address is robert.kim@freelancer.net.").
- If there are multiple results, present them as a simple sentence, a readable list, or a plain table—whichever feels easiest to understand.
- Never repeat, copy, or explain any technical details.

Data: {results}
""")


# -----CREATE-----
create_query_generation_prompt = PromptTemplate.from_template("""
You are an expert SQL developer.
Given the following SQLite database schema and a natural language request, generate a syntactically valid SQL INSERT query that adds a new row into the appropriate table.

Schema:
users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, is_active INTEGER NOT NULL, created_at TEXT NOT NULL)
products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL)
orders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_status TEXT NOT NULL, order_date TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(product_id) REFERENCES products(id))

Instructions:
- Only use the tables and columns that appear in the schema above.
- Avoid making assumptions about table or column names.
- Use only valid SQLite SQL syntax.
- When inserting into a table, do NOT provide a value for the `id` column (it autoincrements).
- Use realistic placeholder values if exact values are not provided in the question (e.g., `"Sample Name"`, `"sample@email.com"`, `1`, `100.0`, etc.).
- When inserting text values (such as names, emails, categories, or statuses), ensure they are wrapped in single quotes.
- Always provide values for all NOT NULL columns.

Natural language request: {input}

SQL Query:   """)


create_query_validation_prompt = PromptTemplate.from_template("""
You are a meticulous SQL validator.
Check the provided SQL INSERT query for common mistakes, including:
- Syntax errors
- Use of non-existent columns or tables
- Missing required NOT NULL fields
- Attempting to insert into AUTOINCREMENT primary keys (id columns should not be manually inserted)
- Incorrect value types for columns (e.g., string vs number)
- SQLite dialect mismatches

**If string fields (e.g., names, emails, categories, statuses) are present, ensure they are wrapped in single quotes.**  
**If the query is missing required fields, rewrite it to include placeholders or realistic defaults (e.g., 'Sample Name', 'sample@email.com', 1, 100.0, '2025-01-01').**

If you spot an issue, rewrite the query so it is valid for the schema and dialect below.  
Do not return explanations—just the validated query.

Schema:
users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, is_active INTEGER NOT NULL, created_at TEXT NOT NULL)
products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL)
orders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_status TEXT NOT NULL, order_date TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(product_id) REFERENCES products(id))

Dialect: SQLite

Original SQL Query:
{query}

Validated and (if needed) corrected SQL Query:
""")

create_result_formatting_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Summarize the result of this database operation for the user:
- If a new item was created, clearly state what was added and include all relevant details from {results}.
- If the operation was not successful, provide a friendly, plain-language explanation of the error.
- Do not mention SQL, technical steps, or system details.
- Make your reply natural, brief, and easy for a non-technical user to understand.

Data: {results}
""")

#----UPDATE-----
update_query_generation_prompt = PromptTemplate.from_template("""
You are an expert SQL developer.
Given the following SQLite database schema and a natural language request, generate a syntactically valid SQL UPDATE query to modify existing data in the appropriate table.

Schema:
users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, is_active INTEGER NOT NULL, created_at TEXT NOT NULL)
products(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL)
orders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_status TEXT NOT NULL, order_date TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(product_id) REFERENCES products(id))

Instructions:
- Only use the tables and columns listed in the schema above.
- Avoid making assumptions about table or column names.
- Use valid SQLite SQL syntax.
- Include a WHERE clause to specify which rows should be updated. Never update all rows unless the request is explicit.
- Use realistic placeholder values if exact new values are not specified in the request (e.g., `'Sample Name'`, `'sample@email.com'`, `100.0`, etc.).
- When updating text fields (such as names, emails, categories, statuses), wrap values in single quotes.
- Do not update the `id` column or any PRIMARY KEY columns.
                                                              
**When comparing text fields (such as names or emails), always make the comparison case-insensitive by using COLLATE NOCASE or by applying the LOWER() function to both sides of the comparison.** This ensures user queries work regardless of capitalization.                                                        

Natural language request: {input}

SQL Query:
""")

update_query_validation_prompt = PromptTemplate.from_template("""
You are a meticulous SQL validator.
Check the provided SQL UPDATE query for common mistakes, including:
- Syntax errors
- Use of non-existent columns or tables
- Missing required NOT NULL fields in SET clause if applicable
- Attempting to update AUTOINCREMENT primary keys (id columns should not be manually updated)
- Incorrect value types for columns (e.g., string vs number)
- SQLite dialect mismatches

**If string fields (e.g., names, emails, categories, statuses) are present, ensure they are wrapped in single quotes.**
**If the query is missing updated values, rewrite it to include realistic values or placeholders (e.g., 'Sample Name', 'sample@email.com', 100.0, '2025-01-01').**
**Ensure the query always includes a WHERE clause so only specific rows are updated (never update all rows unless explicitly requested).**

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

update_result_formatting_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Summarize the result of this database UPDATE operation for the user:
- If the update was successful, clearly state what was changed or updated, mentioning the updated fields and the number of affected items if possible (based on {results}).
- If the operation was not successful, provide a friendly, plain-language explanation of the error.
- Do not mention SQL, technical steps, or system details in your response.
- Make your reply natural, brief, and easy for a non-technical user to understand.

Data: {results}
""")



