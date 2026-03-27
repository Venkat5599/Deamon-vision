"""
Quick system test to verify backend API and frontend connectivity
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_tracks():
    """Test tracks endpoint"""
    print("\nTesting tracks endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/tracks", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tracks endpoint working: {len(data.get('tracks', []))} tracks")
            return True
        else:
            print(f"❌ Tracks endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tracks endpoint error: {e}")
        return False

def test_video_exists():
    """Check if video file exists"""
    print("\nChecking video file...")
    import os
    video_path = "data/uploaded_video.mp4"
    if os.path.exists(video_path):
        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"✅ Video file exists: {video_path} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"❌ Video file not found: {video_path}")
        return False

def main():
    print("=" * 60)
    print("DAEMON VISION - System Test")
    print("=" * 60)
    
    results = []
    
    # Test backend
    results.append(("Health Check", test_health()))
    time.sleep(0.5)
    results.append(("Tracks API", test_tracks()))
    time.sleep(0.5)
    results.append(("Video File", test_video_exists()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\n📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
