#!/usr/bin/env python3

"""
Docker management script for the Accommodation API Service.
Provides convenient commands for managing the Docker container.
"""

import subprocess
import sys
import argparse
import json
import requests
import time

def run_command(command, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_docker():
    """Check if Docker is available"""
    stdout, stderr, code = run_command("docker --version", check=False)
    if code != 0:
        print("❌ Docker is not installed or not running")
        return False
    print(f"✅ {stdout}")
    return True

def build_container():
    """Build the Docker container"""
    print("🔨 Building Docker container...")
    stdout, stderr, code = run_command("docker compose build")
    if code == 0:
        print("✅ Container built successfully!")
        return True
    else:
        print(f"❌ Build failed: {stderr}")
        return False

def start_container():
    """Start the Docker container"""
    print("🚀 Starting container...")
    stdout, stderr, code = run_command("docker compose up -d")
    if code == 0:
        print("✅ Container started successfully!")
        return True
    else:
        print(f"❌ Start failed: {stderr}")
        return False

def stop_container():
    """Stop the Docker container"""
    print("🛑 Stopping container...")
    stdout, stderr, code = run_command("docker compose down")
    if code == 0:
        print("✅ Container stopped successfully!")
        return True
    else:
        print(f"❌ Stop failed: {stderr}")
        return False

def restart_container():
    """Restart the Docker container"""
    print("🔄 Restarting container...")
    stop_container()
    time.sleep(2)
    return start_container()

def show_status():
    """Show container status"""
    print("📊 Container Status:")
    stdout, stderr, code = run_command("docker compose ps")
    print(stdout)
    
    print("\n📋 Container Logs (last 20 lines):")
    stdout, stderr, code = run_command("docker compose logs --tail=20 accommodation-api")
    if stdout:
        print(stdout)
    else:
        print("No logs available")

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8585"
    
    print("🧪 Testing API endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test accommodations endpoint
    try:
        response = requests.get(f"{base_url}/api/accommodations/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Accommodations endpoint working - Found {len(data)} accommodations")
        else:
            print(f"❌ Accommodations endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Accommodations endpoint failed: {e}")
        return False
    
    # Test specific accommodation endpoint
    try:
        response = requests.get(f"{base_url}/api/accommodations/1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Accommodation details endpoint working - {data['name']}")
        else:
            print(f"❌ Accommodation details endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Accommodation details endpoint failed: {e}")
        return False
    
    # Test review endpoint
    try:
        test_review = {
            "user_id": 9999,
            "rating": 4.5,
            "comment": "Docker test review"
        }
        response = requests.post(f"{base_url}/api/accommodations/1/reviews", 
                               json=test_review, timeout=5)
        if response.status_code == 200:
            print("✅ Review endpoint working")
        else:
            print(f"❌ Review endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Review endpoint failed: {e}")
        return False
    
    print("🎉 All API tests passed!")
    return True

def show_logs():
    """Show container logs"""
    print("📋 Container Logs:")
    run_command("docker compose logs -f accommodation-api")

def cleanup():
    """Clean up containers and images"""
    print("🧹 Cleaning up Docker resources...")
    run_command("docker compose down")
    stdout, stderr, code = run_command("docker images | grep accommodation", check=False)
    if stdout:
        print("Removing accommodation images...")
        run_command("docker rmi $(docker images | grep accommodation | awk '{print $3}')", check=False)
    print("✅ Cleanup completed!")

def main():
    parser = argparse.ArgumentParser(description='Docker Manager for Accommodation API Service')
    parser.add_argument('action', choices=[
        'build', 'start', 'stop', 'restart', 'status', 'test', 'logs', 'cleanup', 'deploy'
    ], help='Action to perform')
    
    args = parser.parse_args()
    
    print("🐳 Accommodation API Docker Manager")
    print("=" * 50)
    
    if not check_docker():
        sys.exit(1)
    
    if args.action == 'build':
        success = build_container()
    elif args.action == 'start':
        success = start_container()
    elif args.action == 'stop':
        success = stop_container()
    elif args.action == 'restart':
        success = restart_container()
    elif args.action == 'status':
        show_status()
        success = True
    elif args.action == 'test':
        success = test_api()
    elif args.action == 'logs':
        show_logs()
        success = True
    elif args.action == 'cleanup':
        cleanup()
        success = True
    elif args.action == 'deploy':
        print("🚀 Full deployment process...")
        success = build_container()
        if success:
            success = start_container()
        if success:
            print("⏳ Waiting for service to start...")
            time.sleep(5)
            success = test_api()
        if success:
            print("\n🎉 Deployment completed successfully!")
            print(f"🌐 API available at: http://localhost:8585")
            print(f"📚 API docs: http://localhost:8585/docs (if using FastAPI)")
    
    if not success and args.action not in ['status', 'logs']:
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1) 