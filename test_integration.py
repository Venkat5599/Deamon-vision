"""
Integration test script for Daemon Vision full stack.
Tests backend API and frontend connectivity.
"""
import asyncio
import requests
import websockets
import json
import time
from typing import Dict, Any

API_BASE = "http://localhost:8000"
WS_URL = "ws://localhost:8000/stream"
FRONTEND_URL = "http://localhost:3000"


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_test(name: str, passed: bool, message: str = ""):
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} | {name}")
    if message:
        print(f"       {message}")


def test_backend_health() -> bool:
    """Test backend health endpoint."""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        data = response.json()
        print_test("Backend Health Check", response.status_code == 200, 
                   f"Status: {data.get('status', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print_test("Backend Health Check", False, str(e))
        return False


def test_get_tracks() -> bool:
    """Test GET /tracks endpoint."""
    try:
        response = requests.get(f"{API_BASE}/tracks", timeout=5)
        data = response.json()
        tracks = data.get('tracks', [])
        print_test("GET /tracks", response.status_code == 200,
                   f"Found {len(tracks)} tracks")
        return response.status_code == 200
    except Exception as e:
        print_test("GET /tracks", False, str(e))
        return False


def test_lock_unlock() -> bool:
    """Test lock/unlock functionality."""
    try:
        # Get tracks first
        response = requests.get(f"{API_BASE}/tracks", timeout=5)
        tracks = response.json().get('tracks', [])
        
        if not tracks:
            print_test("Lock/Unlock", False, "No tracks available to test")
            return False
        
        track_id = tracks[0]['track_id']
        
        # Lock
        lock_response = requests.post(f"{API_BASE}/lock/{track_id}", timeout=5)
        if lock_response.status_code != 200:
            print_test("Lock/Unlock", False, "Failed to lock")
            return False
        
        # Unlock
        unlock_response = requests.delete(f"{API_BASE}/lock", timeout=5)
        if unlock_response.status_code != 200:
            print_test("Lock/Unlock", False, "Failed to unlock")
            return False
        
        print_test("Lock/Unlock", True, f"Locked and unlocked track {track_id}")
        return True
    except Exception as e:
        print_test("Lock/Unlock", False, str(e))
        return False


def test_trajectory() -> bool:
    """Test trajectory endpoint."""
    try:
        # Get tracks first
        response = requests.get(f"{API_BASE}/tracks", timeout=5)
        tracks = response.json().get('tracks', [])
        
        if not tracks:
            print_test("Trajectory", False, "No tracks available")
            return False
        
        track_id = tracks[0]['track_id']
        
        # Get trajectory
        traj_response = requests.get(f"{API_BASE}/track/{track_id}/trajectory", timeout=5)
        data = traj_response.json()
        
        print_test("Trajectory", traj_response.status_code == 200,
                   f"Track {track_id} has {len(data.get('trajectory', []))} points")
        return traj_response.status_code == 200
    except Exception as e:
        print_test("Trajectory", False, str(e))
        return False


async def test_websocket() -> bool:
    """Test WebSocket connection."""
    try:
        async with websockets.connect(WS_URL, timeout=10) as ws:
            # Wait for connected message
            message = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(message)
            
            if data.get('type') == 'connected':
                print_test("WebSocket Connection", True, "Connected successfully")
                
                # Wait for track update
                message = await asyncio.wait_for(ws.recv(), timeout=10)
                data = json.loads(message)
                
                if data.get('type') == 'track_update':
                    tracks = data.get('tracks', [])
                    print_test("WebSocket Track Update", True, 
                               f"Received {len(tracks)} tracks")
                    return True
                else:
                    print_test("WebSocket Track Update", False, 
                               f"Unexpected message type: {data.get('type')}")
                    return False
            else:
                print_test("WebSocket Connection", False, 
                           f"Unexpected message: {data.get('type')}")
                return False
    except Exception as e:
        print_test("WebSocket Connection", False, str(e))
        return False


def test_frontend() -> bool:
    """Test frontend accessibility."""
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        print_test("Frontend Accessibility", response.status_code == 200,
                   f"Frontend is accessible at {FRONTEND_URL}")
        return response.status_code == 200
    except Exception as e:
        print_test("Frontend Accessibility", False, str(e))
        return False


def test_cors() -> bool:
    """Test CORS headers."""
    try:
        response = requests.options(f"{API_BASE}/tracks", 
                                     headers={'Origin': FRONTEND_URL},
                                     timeout=5)
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        print_test("CORS Configuration", cors_header is not None,
                   f"CORS header: {cors_header}")
        return cors_header is not None
    except Exception as e:
        print_test("CORS Configuration", False, str(e))
        return False


async def run_all_tests():
    """Run all integration tests."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}DAEMON VISION - INTEGRATION TEST SUITE{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Testing Backend API...{Colors.END}\n")
    
    results = []
    
    # Backend tests
    results.append(("Backend Health", test_backend_health()))
    time.sleep(0.5)
    
    results.append(("GET /tracks", test_get_tracks()))
    time.sleep(0.5)
    
    results.append(("Lock/Unlock", test_lock_unlock()))
    time.sleep(0.5)
    
    results.append(("Trajectory", test_trajectory()))
    time.sleep(0.5)
    
    results.append(("CORS", test_cors()))
    time.sleep(0.5)
    
    # WebSocket test
    print(f"\n{Colors.YELLOW}Testing WebSocket...{Colors.END}\n")
    results.append(("WebSocket", await test_websocket()))
    time.sleep(0.5)
    
    # Frontend test
    print(f"\n{Colors.YELLOW}Testing Frontend...{Colors.END}\n")
    results.append(("Frontend", test_frontend()))
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {status} | {name}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}✓ ALL TESTS PASSED ({passed}/{total}){Colors.END}")
        print(f"\n{Colors.GREEN}System is fully operational!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠ {passed}/{total} TESTS PASSED{Colors.END}")
        print(f"\n{Colors.YELLOW}Some components may need attention.{Colors.END}")
    
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    return passed == total


if __name__ == "__main__":
    print(f"\n{Colors.BLUE}Starting integration tests...{Colors.END}")
    print(f"{Colors.YELLOW}Ensure backend and frontend are running:{Colors.END}")
    print(f"  Backend:  {API_BASE}")
    print(f"  Frontend: {FRONTEND_URL}")
    print(f"  WebSocket: {WS_URL}\n")
    
    input("Press Enter to continue...")
    
    success = asyncio.run(run_all_tests())
    
    exit(0 if success else 1)
