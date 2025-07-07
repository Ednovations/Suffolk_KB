from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from typing import List

app = FastAPI()

# Path to the knowledge base JSON file
KB_JSON_PATH = os.path.join(os.path.dirname(__file__), '../suffolk_kb_json.json')

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

def load_kb():
    with open(KB_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_kb(data):
    with open(KB_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get('/kb', response_class=JSONResponse)
def get_kb():
    return load_kb()

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Admin panel (basic, for demo)
templates = Jinja2Templates(directory="templates")

@app.get('/admin', response_class=HTMLResponse)
def admin_panel(request: Request):
    kb = load_kb()
    return templates.TemplateResponse("admin.html", {"request": request, "kb": kb})

@app.post('/admin/update')
def update_kb(request: Request, content: str = Form(...)):
    data = json.loads(content)
    save_kb(data)
    # Notify all clients
    import asyncio
    asyncio.create_task(manager.broadcast("update"))
    return RedirectResponse(url="/admin", status_code=303)

# Mount static files for admin panel
app.mount("/static", StaticFiles(directory="static"), name="static")
