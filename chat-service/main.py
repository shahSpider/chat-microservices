from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.websocket_manager import ConnectionManager
from app.routers import messages
from app.database import Base, engine
from app import models

app = FastAPI()
manager = ConnectionManager()
app.include_router(messages.router, prefix="/api", tags=["messages"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Chat service is running"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_id, f"Room {room_id} | {data}")
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
