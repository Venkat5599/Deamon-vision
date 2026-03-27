"""
Upload test video to start processing
"""
import requests
import time

def upload_video():
    """Upload the test video to the API"""
    url = "http://localhost:8000/upload/video"
    video_path = "data/uploaded_video.mp4"
    
    print("=" * 60)
    print("Uploading test video to Daemon Vision...")
    print("=" * 60)
    print(f"Video: {video_path}")
    print(f"Target: {url}")
    print()
    
    try:
        with open(video_path, 'rb') as f:
            files = {'file': ('uploaded_video.mp4', f, 'video/mp4')}
            print("Uploading... (this may take a moment)")
            response = requests.post(url, files=files, timeout=30)
            
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Upload successful!")
            print(f"Message: {result.get('message', 'Video uploaded')}")
            print(f"Filename: {result.get('filename', 'N/A')}")
            print()
            print("=" * 60)
            print("🎬 Video processing started!")
            print("=" * 60)
            print()
            print("Check the frontend at: http://localhost:3001")
            print("You should now see:")
            print("  - Video frames being displayed")
            print("  - Bounding boxes around detected objects")
            print("  - FPS and latency metrics updating")
            print("  - Active tracks in the sidebar")
            print()
            return True
        else:
            print(f"\n❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except FileNotFoundError:
        print(f"\n❌ Video file not found: {video_path}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to backend API")
        print("Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    upload_video()
