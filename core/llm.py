from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")

# llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-pro",
#             temperature=0.5,
#             api_key=google_api_key
#         )


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)