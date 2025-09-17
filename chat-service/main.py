from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.websocket_manager import ConnectionManager
from app.routers import messages
from app.database import Base, engine, SessionLocal
from app import models
from jose import jwt, JWTError
import sys

SECRET_KEY="django-insecure-snckc&+mm8=rcp3ku%)c=pa7y7n=na7-(9r!eb)yii!03q$jm)"
ALGORITHM = "HS256"


app = FastAPI()
manager = ConnectionManager()
app.include_router(messages.router, prefix="/api", tags=["messages"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Chat service is running"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        # Optionally check room membership here
    except JWTError:
        await websocket.close(code=1008)
        return
    
    # only connect after successfull authentication
    await manager.connect(room_id, websocket)
    
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_text()
            # Store message in DB
            msg = models.Message(room_id=room_id, sender_id=user_id, content=data)
            db.add(msg)
            db.commit()
            db.refresh(msg)
            await manager.broadcast(room_id, f"Room {room_id} | {data}")
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    finally:
        db.close()
