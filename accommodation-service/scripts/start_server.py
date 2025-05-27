#!/usr/bin/env python3

"""
Convenient script to start the Accommodation API server.
This script handles environment setup and provides multiple startup options.
"""

import sys
import os
import subprocess
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def check_database():
    """Check if database exists and has data"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'accommodation.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found. Creating database...")
        return False
    
    try:
        from app.database.database import SessionLocal
        from app.models.accommodation import Accommodation
        
        db = SessionLocal()
        count = db.query(Accommodation).count()
        db.close()
        
        if count == 0:
            print("❌ Database is empty. Seeding required...")
            return False
        
        print(f"✅ Database found with {count} accommodations")
        return True
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def seed_database():
    """Run the database seeding script"""
    script_path = os.path.join(os.path.dirname(__file__), 'seed_data.py')
    
    try:
        print("🌱 Seeding database...")
        subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Database seeding failed: {e}")
        return False

def start_simple_server(port=8585):
    """Start the simple HTTP server"""
    try:
        from simple_server import run_server
        run_server(port)
    except ImportError:
        script_path = os.path.join(os.path.dirname(__file__), 'simple_server.py')
        subprocess.run([sys.executable, script_path], check=True)

def start_fastapi_server(port=8585):
    """Start the FastAPI server using uvicorn"""
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '0.0.0.0', 
            '--port', str(port),
            '--reload'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ FastAPI server failed to start: {e}")
        print("💡 Falling back to simple HTTP server...")
        start_simple_server(port)

def run_tests():
    """Run the API tests"""
    test_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'test_api.py')
    
    try:
        print("🧪 Running API tests...")
        subprocess.run([sys.executable, test_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Accommodation API Server Startup Script')
    parser.add_argument('--port', '-p', type=int, default=8585, help='Port to run the server on (default: 8585)')
    parser.add_argument('--server', '-s', choices=['simple', 'fastapi', 'auto'], default='auto', 
                       help='Server type to use (default: auto)')
    parser.add_argument('--seed', action='store_true', help='Force database seeding')
    parser.add_argument('--test', action='store_true', help='Run tests before starting server')
    parser.add_argument('--no-check', action='store_true', help='Skip database checks')
    
    args = parser.parse_args()
    
    print("🚀 Accommodation API Server Startup")
    print("=" * 50)
    
    # Database setup
    if not args.no_check:
        if args.seed or not check_database():
            if not seed_database():
                print("❌ Failed to setup database. Exiting.")
                sys.exit(1)
    
    # Run tests if requested
    if args.test:
        if not run_tests():
            response = input("Tests failed. Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    # Start server
    print(f"\n🌐 Starting server on port {args.port}...")
    
    if args.server == 'simple':
        start_simple_server(args.port)
    elif args.server == 'fastapi':
        start_fastapi_server(args.port)
    else:  # auto
        try:
            # Try FastAPI first
            print("🔄 Attempting to start FastAPI server...")
            start_fastapi_server(args.port)
        except (ImportError, subprocess.CalledProcessError):
            print("💡 FastAPI failed, using simple HTTP server...")
            start_simple_server(args.port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Server startup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Startup failed: {e}")
        sys.exit(1) 