"""
Test WebSocket connection and data flow
"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/stream"
    
    print("Connecting to WebSocket...")
    async with websockets.connect(uri) as websocket:
        print("✅ Connected!")
        
        # Send ping
        await websocket.send("ping")
        print("Sent ping")
        
        # Receive messages
        message_count = 0
        try:
            while message_count < 5:
                message = await asyncio.wait_for(websocket.recv(), timeout=10)
                data = json.loads(message)
                
                message_count += 1
                print(f"\n📨 Message {message_count}:")
                print(f"  Type: {data.get('type')}")
                print(f"  Tracks: {len(data.get('tracks', []))}")
                print(f"  Has frame: {'frame' in data}")
                print(f"  Has metrics: {'metrics' in data}")
                
                if 'metrics' in data:
                    metrics = data['metrics']
                    print(f"  FPS: {metrics.get('fps', 'N/A')}")
                    print(f"  Latency: {metrics.get('latency', 'N/A')}ms")
                
                if 'frame' in data:
                    frame_size = len(data['frame'])
                    print(f"  Frame size: {frame_size} bytes ({frame_size/1024:.1f} KB)")
                    
        except asyncio.TimeoutError:
            print("\n⏱️  Timeout waiting for messages")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print(f"\n✅ Test complete! Received {message_count} messages")

if __name__ == "__main__":
    asyncio.run(test_websocket())
