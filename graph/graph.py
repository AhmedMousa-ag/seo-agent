from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END, START
from .schemas import State
from tools.search import get_search_tools
# from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from configs.config import GOOGLE_API_KEY
from langchain_core.messages import SystemMessage

memory = InMemorySaver()

# Set up Gemini LLM (requires API key in environment variable GOOGLE_API_KEY)
MODEL_NAME = "gemini-2.5-flash"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=GOOGLE_API_KEY)
llm.bind_tools([get_search_tools()])
# llm = init_chat_model(MODEL_NAME,model_provider="google_vertexai")


def chat_bot(state: State):
    print("Invoked chat bot")
    response = llm.invoke(state.messages)
    return {"messages": [response]}


def search_for_outline(state:State):
    print("Invoked search for outline")
    key_word = state.messages[1].content
    messages = state.messages
    messages.append(SystemMessage(content=f"Use the Search tool to find an outline and recent trends for {key_word}."))
    state.messages = messages
    print(f"Searching for outline for {state.messages[-1]}")
    response = llm.invoke(state.messages)
    state.messages.append(response)
    return {"messages": [response]}

def final_html_response(state:State):
    print("Invoked html response")
    state.messages.append(SystemMessage(content="Generate a final HTML response based on the search results and outline."))
    response = llm.invoke(state.messages)
    state.messages.append(response)
    return {"messages": [response]}

def attach_imgs_html(state:State):
    print("Invoked attach images to html")
    state.messages.append(SystemMessage(content="Attach images to the HTML response as needed, you can search for images and get back the proper urls then update the html content according to the new."))
    response = llm.invoke(state.messages)
    state.messages.append(response)
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chat_bot",chat_bot)
graph_builder.add_node("search_for_outline", search_for_outline)
graph_builder.add_node("final_html_response", final_html_response)
# graph_builder.add_node("attach_imgs_html", attach_imgs_html)
graph_builder.add_edge(START,"search_for_outline")
graph_builder.add_edge("search_for_outline", "chat_bot")
tool_node = ToolNode(tools=[get_search_tools()])

graph_builder.add_node("tools", tool_node)
# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "search_for_outline",
    tools_condition,
    
    {"tools": "tools", END: END},
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "search_for_outline")

graph_builder.add_edge("chat_bot", "final_html_response")
graph_builder.add_edge("final_html_response", END)
compiled_graph = graph_builder.compile(checkpointer=memory)

try:
    img:bytes = compiled_graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(img)
except Exception:
    # This requires some extra dependencies and is optional
    pass
