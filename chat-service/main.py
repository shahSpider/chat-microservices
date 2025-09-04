from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Chat service is running"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received in room {room_id}: {data}")
