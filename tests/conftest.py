"""
Conftest file for pytest configuration and fixtures.
"""
import pytest
import subprocess
import time
import sys
import os
import tempfile
import requests

@pytest.fixture(scope="session", autouse=True)
def start_services():
    """Start backend and frontend services for E2E tests."""
    print("\n" + "="*50)
    print("Starting services for E2E tests...")
    print("="*50)
    
    # Start backend
    backend_env = os.environ.copy()
    test_db_path = os.path.join(tempfile.gettempdir(), "module13-test.db")
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    backend_env.setdefault("DATABASE_URL", f"sqlite:///{test_db_path}")
    backend_env.setdefault("FLASK_ENV", "development")
    backend_env.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
    backend_env.setdefault("PORT", "5050")
    backend_process = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd="backend",
        env=backend_env,
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
    backend_ready = False
    frontend_ready = False

    for _ in range(30):
        if not backend_ready:
            try:
                backend_ready = requests.get("http://localhost:5050/health", timeout=1).ok
            except requests.RequestException:
                backend_ready = False

        if not frontend_ready:
            try:
                frontend_ready = requests.get("http://localhost:3000", timeout=1).ok
            except requests.RequestException:
                frontend_ready = False

        if backend_ready and frontend_ready:
            break

        time.sleep(1)

    if not backend_ready or not frontend_ready:
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait(timeout=5)
        frontend_process.wait(timeout=5)
        raise RuntimeError("Backend or frontend did not become ready in time")
    
    yield
    
    # Cleanup
    print("\n" + "="*50)
    print("Stopping services...")
    print("="*50)
    backend_process.terminate()
    frontend_process.terminate()
    backend_process.wait(timeout=5)
    frontend_process.wait(timeout=5)
