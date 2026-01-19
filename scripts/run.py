import socket
import subprocess
import sys

def find_available_port(start_port=8000, max_attempts=10):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return None

def main():
    port = find_available_port()
    if not port:
        print("Error: Could not find an available port in the range 8000-8010.")
        sys.exit(1)
    
    print(f"Starting server on http://localhost:{port}")
    cmd = [
        "uvicorn", "app.main:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--reload"
    ]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nStopping server...")

if __name__ == "__main__":
    main()
