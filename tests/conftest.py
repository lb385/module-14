"""
Conftest file for pytest configuration and fixtures.
"""
import pytest
import subprocess
import time
import sys

@pytest.fixture(scope="session", autouse=True)
def start_services():
    """Start backend and frontend services for E2E tests."""
    print("\n" + "="*50)
    print("Starting services for E2E tests...")
    print("="*50)
    
    # Start backend
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start frontend server
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000"],
        cwd="frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for services to start
    time.sleep(3)
    
    yield
    
    # Cleanup
    print("\n" + "="*50)
    print("Stopping services...")
    print("="*50)
    backend_process.terminate()
    frontend_process.terminate()
    backend_process.wait(timeout=5)
    frontend_process.wait(timeout=5)
