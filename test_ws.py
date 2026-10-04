import asyncio
import websockets
import json

async def test_ws():
    uri = 'ws://localhost:8501/_stcore/stream'
    try:
        async with websockets.connect(uri) as websocket:
            print('Connected to websocket')
            
            # Send an initial message to start the script run
            # For Streamlit 1.30+, a BackMsg to start might just be a window size update or empty BackMsg
            msg = {'backMsg': {'setWindowSize': {'width': 1000, 'height': 800}}}
            await websocket.send(json.dumps(msg))
            
            while True:
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received message length: {len(message)}")
    except asyncio.TimeoutError:
        print('Timeout')
    except Exception as e:
        print('Exception:', type(e).__name__, e)

asyncio.run(test_ws())
