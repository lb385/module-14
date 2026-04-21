"""
Conftest file for pytest configuration and fixtures.
"""
import pytest
import subprocess
import time
import sys
import os

@pytest.fixture(scope="session", autouse=True)
def start_services():
    """Start backend and frontend services for E2E tests."""
    print("\n" + "="*50)
    print("Starting services for E2E tests...")
    print("="*50)
    
    # Start backend
    backend_env = os.environ.copy()
    backend_env.setdefault("DATABASE_URL", "postgresql://authuser:authpassword@localhost:5432/auth_db")
    backend_env.setdefault("FLASK_ENV", "development")
    backend_env.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
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
