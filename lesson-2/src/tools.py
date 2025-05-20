from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv
import os

load_dotenv()

tavily_search_tool = TavilySearchResults(
  max_results=2,
  api_key=os.getenv("TAVILY_API_KEY"),
)