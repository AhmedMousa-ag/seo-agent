from dotenv import load_dotenv
import os
load_dotenv()
# Import langchain system messages
from langchain_core.messages import SystemMessage

SYSTEM_MESSAGE = SystemMessage(content="You are a helpful assistant who is required to provide a blog based on user input. Use the available tools to help you find outline the blog content first, then start writing down each section. Return your output in html format.")



MEMORY_CONFIG = {"configurable": {"thread_id": ""}}


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")