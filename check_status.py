"""Quick status check for Daemon Vision system."""
import requests
import json

def check_backend():
    """Check if backend is running."""
    try:
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.status_code == 200:
            data = response.json()
            print("✓ Backend is running")
            print(f"  - Active tracks: {data.get('active_tracks', 0)}")
            print(f"  - WebSocket connections: {data.get('websocket_connections', 0)}")
            return True
        else:
            print("✗ Backend returned error:", response.status_code)
            return False
    except Exception as e:
        print("✗ Backend is not running:", str(e))
        return False

def check_tracks():
    """Check current tracks."""
    try:
        response = requests.get('http://localhost:8000/tracks', timeout=2)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', [])
            print(f"\n✓ Tracks endpoint working")
            print(f"  - Current tracks: {len(tracks)}")
            if tracks:
                for track in tracks[:3]:  # Show first 3
                    print(f"    • Track #{track['track_id']}: {track['class_name']} "
                          f"@ ({track['bbox']['x']:.0f}, {track['bbox']['y']:.0f})")
            return True
        else:
            print("✗ Tracks endpoint error:", response.status_code)
            return False
    except Exception as e:
        print("✗ Tracks endpoint failed:", str(e))
        return False

def main():
    print("=" * 60)
    print("DAEMON VISION - System Status Check")
    print("=" * 60)
    
    backend_ok = check_backend()
    if backend_ok:
        check_tracks()
    
    print("\n" + "=" * 60)
    if backend_ok:
        print("✓ System is operational!")
        print("\nOpen your browser to: http://localhost:3000")
        print("The video feed should be visible with real-time tracking.")
    else:
        print("✗ System has issues. Check if backend is running:")
        print("  python main.py --device cuda")
    print("=" * 60)

if __name__ == '__main__':
    main()
