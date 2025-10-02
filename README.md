# MiniAgenticBot

A natural language interface for database operations with human-in-the-loop verification for critical operations. Built with LangGraph, FastAPI, and vanilla JavaScript.

**Detailed Documentation**- https://docs.google.com/document/d/1G18ska1G8mPRY0l8XXyWt9mhXYXxTwMILJcrSQgNweE/edit?usp=sharing

**Demo video** → https://drive.google.com/file/d/14j-a6spF0MNO2ex3DZrT9e3TIIcGtO0b/view?usp=sharing

**Graph Architecture Flowchart**→ https://www.figma.com/board/ecYEwxJgvjFnsOTZYmlHLj/DB-Agent?node-id=0-1&t=M9FT7iyH1t4ogV7U-1

## ✨ Features

-  **Natural Language Interface** - Interact with your database using plain English
-  **Human-in-the-Loop** - Requires approval for Create, Update, and Delete operations
-  **Intent Classification** - Automatically routes queries to appropriate handlers
-  **Query Validation** - LLM-powered SQL query generation and validation
-  **Modern UI** - Beautiful gradient-based chat interface
-  **Real-time Status** - Connection status indicator
-  **Structured Workflow** - LangGraph-based agent architecture

## 📋 Prerequisites

- Python 3.10
- SQLite3
- OpenAI API Key (or compatible LLM provider)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/aitch-cmd/MiniAgenticBot.git
cd agentic-crud-bot
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
```

### 5. Initialize the database

```bash
python setup_db.py  
```
# 🎮 Usage  

## Development Mode (Recommended for Testing)  

### Start backend  
``` uvicorn main:app --host 0.0.0.0 --port 8000 --reload ```

Server runs at: [http://localhost:8000](http://localhost:8000)  

### Start frontend  
Open `templates/index.html` in your browser or run:  

## Docker Deployment  

### Run with Docker Compose

Make sure you have **Docker** and **Docker Compose** installed.  
From the project root, run:
``` docker compose up --build ```

This will:
- Build **backend** and **frontend** images.
- Create a shared **app-network**.
- Start containers:
  - **crud-backend** on port `8000` (with ./data volume).
  - **crud-frontend** on port `80`.
- Restart services automatically unless stopped.

## 📁 Project Structure

```
agentic-crud-bot/
├── agents/
│   ├── __init__.py
│   ├── graph.py              # LangGraph workflow definition
│   ├── states.py             # State management
│   └── nodes/
│       ├── react.py          # Intent classification
│       ├── read.py           # READ operations
│       ├── create.py         # CREATE operations
│       ├── update.py         # UPDATE operations
│       └── delete.py         # DELETE operations
├── core/
│   ├── __init__.py
│   ├── llm.py               # LLM configuration
│   └── prompts.py           # Prompt templates
├── data/
│   └── app.db               # SQLite database
├── index.html               # Frontend interface
├── main.py                  # FastAPI server
├── requirements.txt
└── README.md
```

### 3. Example queries

**Read Operations** (No approval required):
- "Show me all users"
- "Find users older than 25"
- "Get the email of user with ID 5"

**Create Operations** (Requires approval):
- "Add a new user named John with email john@example.com"
- "Insert a product called Laptop with price 999"

**Update Operations** (Requires approval):
- "Update user John's email to newemail@example.com"
- "Change the price of product with ID 3 to 799"

**Delete Operations** (Requires approval):
- "Delete user with ID 5"
- "Remove the product named Laptop"

## 🔧 Configuration

### Database Configuration

Update the database path in `agents/nodes/*.py`:

```python
conn = sqlite3.connect("data/app.db")
```

### LLM Configuration

Modify `core/llm.py` to use different models:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",  # or gpt-3.5-turbo
    temperature=0
)
```

### Prompts

Customize prompts in `core/prompts.py` for different behaviors.

## 🛡️ Security Features

- **Human-in-the-Loop**: All CUD operations require explicit approval
- **Query Validation**: LLM validates generated SQL before execution
- **CORS Protection**: Configurable CORS middleware
- **SQL Injection Prevention**: Parameterized queries via LLM validation

## 🎨 Frontend Features

- Modern gradient-based UI
- Real-time connection status
- Smooth animations and transitions
- Loading indicators
- Error handling with user-friendly messages
- Responsive design for mobile devices

## 📊 API Endpoints

### POST `/query`

Execute a natural language database query.

**Request Body:**
```json
{
  "input": "Show me all users",
  "human_verified": null
}
```

**Response (Read):**
```json
{
  "status": "completed",
  "final_answer": "Here are all the users...",
  "validated_query": "SELECT * FROM users"
}
```

**Response (CUD - Verification Required):**
```json
{
  "status": "verification_required",
  "validated_query": "UPDATE users SET name='John' WHERE id=5",
  "final_answer": null
}
```

## 🧪 Testing

Run tests:

```bash
pytest tests/
```

Test the API directly:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"input": "show me all users"}'
```

## 🐛 Troubleshooting

### Frontend shows "Unexpected response from server"

1. Check if FastAPI server is running
2. Verify CORS configuration in `main.py`
3. Check browser console for detailed errors
4. Ensure `verification_required` field is in `states.py`

### Database connection errors

1. Verify database path exists
2. Check file permissions
3. Ensure SQLite is installed

### LLM errors

1. Verify API key is set correctly
2. Check API rate limits
3. Review prompt formatting in `core/prompts.py`
