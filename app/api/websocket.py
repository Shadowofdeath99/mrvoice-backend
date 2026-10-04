import json
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.pitch_service import pitch_service
from app.services.feedback_service import feedback_service

router = APIRouter()

@router.websocket('/ws/stream')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_array = np.frombuffer(data, dtype=np.float32)
            
            pitch_data = pitch_service.analyze_chunk(audio_array)
            feedback = feedback_service.generate_feedback(pitch_data)
            
            response = {
                'pitch': pitch_data,
                'feedback': feedback
            }
            
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print('Client disconnected from stream')
    except Exception as e:
        print(f'WebSocket error: {e}')
