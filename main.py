from fastapi import FastAPI, Query
from graph.graph import compiled_graph as graph, State
from langchain_core.messages import HumanMessage
from configs.config import SYSTEM_MESSAGE, MEMORY_CONFIG
from fastapi.responses import HTMLResponse

app = FastAPI(docs_url="/")

@app.get("/{username}/{keyword}", response_class=HTMLResponse)
def invoke_endpoint(username: str, keyword: str):
	MEMORY_CONFIG["configurable"]["thread_id"] = username
	response = graph.invoke(
		State(messages=[SYSTEM_MESSAGE, HumanMessage(content=keyword)]),
		config=MEMORY_CONFIG
	)
	print(response)
	article = response["messages"][-1].content
	article = article.replace("```html","").replace("```","")
	return article


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, port=8000)