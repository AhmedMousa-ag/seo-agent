from fastapi import FastAPI, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from graph.graph import compiled_graph as graph, State
from langchain_core.messages import HumanMessage
from configs.config import SYSTEM_MESSAGE, MEMORY_CONFIG

app = FastAPI(docs_url="/")

@app.get("/{username}/{keyword}", response_class=HTMLResponse)
def invoke_endpoint(username: str, keyword: str):
	MEMORY_CONFIG["configurable"]["thread_id"] = username
	response = graph.invoke(
		State(messages=[SYSTEM_MESSAGE, HumanMessage(content=keyword)]),
		config=MEMORY_CONFIG
	)
	article = response["messages"][-1].content
	article = article.replace("```html", "").replace("```", "")
	return article

@app.post("/redirect", response_class=HTMLResponse)
async def redirect_to_article(username: str = Form(...), keyword: str = Form(...)):
	return RedirectResponse(url=f"/{username}/{keyword}", status_code=303)

@app.get("/blog_generator", response_class=HTMLResponse)
def redirect_form():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Redirect Form</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .form-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 400px;
                transform: translateY(0);
                transition: transform 0.3s ease;
            }
            
            .form-container:hover {
                transform: translateY(-5px);
            }
            
            h2 {
                text-align: center;
                margin-bottom: 30px;
                color: #333;
                font-weight: 600;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 500;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            input[type="text"] {
                width: 100%;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 12px;
                font-size: 16px;
                background: #f8f9fa;
                transition: all 0.3s ease;
                outline: none;
            }
            
            input[type="text"]:focus {
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                transform: translateY(-2px);
            }
            
            input[type="text"]::placeholder {
                color: #adb5bd;
                font-style: italic;
            }
            
            .submit-btn {
                width: 100%;
                padding: 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
                position: relative;
                overflow: hidden;
            }
            
            .submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            
            .submit-btn:active {
                transform: translateY(0);
            }
            
            .submit-btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .submit-btn:hover::before {
                left: 100%;
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .form-container {
                animation: fadeIn 0.6s ease-out;
            }
            
            .decorative-element {
                position: absolute;
                width: 100px;
                height: 100px;
                background: linear-gradient(45deg, #ff6b6b, #feca57);
                border-radius: 50%;
                opacity: 0.1;
                animation: float 6s ease-in-out infinite;
            }
            
            .decorative-element:nth-child(1) {
                top: 10%;
                left: 10%;
                animation-delay: 0s;
            }
            
            .decorative-element:nth-child(2) {
                top: 20%;
                right: 10%;
                animation-delay: 2s;
            }
            
            .decorative-element:nth-child(3) {
                bottom: 10%;
                left: 15%;
                animation-delay: 4s;
            }
            
            @keyframes float {
                0%, 100% {
                    transform: translateY(0px);
                }
                50% {
                    transform: translateY(-20px);
                }
            }
        </style>
    </head>
    <body>
        <div class="decorative-element"></div>
        <div class="decorative-element"></div>
        <div class="decorative-element"></div>
        
        <div class="form-container">
            <h2>Blogs Generator</h2>
            <form action="/redirect" method="post">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" placeholder="Enter your username" required>
                </div>
                
                <div class="form-group">
                    <label for="keyword">Keyword</label>
                    <input type="text" id="keyword" name="keyword" placeholder="Enter keyword" required>
                </div>
                
                <button type="submit" class="submit-btn">Go</button>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, port=8000)