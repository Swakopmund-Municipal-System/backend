#!/usr/bin/env python3

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import traceback

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database.database import SessionLocal
from app.services.accommodation_service import get_accommodations, get_accommodation_by_id, add_review
from app.models.schemas import ReviewCreate

class AccommodationAPIHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_params = parse_qs(parsed_path.query)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            db = SessionLocal()
            
            if path == '/':
                # Root endpoint
                response = {
                    "service": "Accommodation API Service",
                    "version": "1.0.0",
                    "description": "Provides information about accommodation options in Swakopmund",
                    "endpoints": {
                        "GET /api/accommodations/": "Get list of accommodations",
                        "GET /api/accommodations/{id}": "Get accommodation details",
                        "POST /api/accommodations/{id}/reviews": "Add a review"
                    }
                }
                
            elif path == '/api/accommodations/' or path == '/api/accommodations':
                # Get accommodations
                name_filter = query_params.get('name', [None])[0]
                accommodations = get_accommodations(db, name_filter)
                
                response = []
                for acc in accommodations:
                    response.append({
                        "id": acc.id,
                        "name": acc.name,
                        "description": acc.description,
                        "location": acc.location,
                        "website_url": acc.website_url,
                        "mobile": acc.mobile,
                        "telephone": acc.telephone,
                        "email": acc.email,
                        "images": [{"id": img.id, "document_id": img.document_id, "image_url": img.image_url, "accommodation_id": img.accommodation_id} for img in acc.images]
                    })
                    
            elif path.startswith('/api/accommodations/') and path.count('/') == 3:
                # Get accommodation details
                try:
                    acc_id = int(path.split('/')[-1])
                    accommodation = get_accommodation_by_id(db, acc_id)
                    
                    if accommodation:
                        response = {
                            "id": accommodation.id,
                            "name": accommodation.name,
                            "description": accommodation.description,
                            "location": accommodation.location,
                            "website_url": accommodation.website_url,
                            "mobile": accommodation.mobile,
                            "telephone": accommodation.telephone,
                            "email": accommodation.email,
                            "images": [{"id": img.id, "document_id": img.document_id, "image_url": img.image_url, "accommodation_id": img.accommodation_id} for img in accommodation.images],
                            "reviews": [{"id": rev.id, "user_id": rev.user_id, "rating": rev.rating, "comment": rev.comment, "accommodation_id": rev.accommodation_id} for rev in accommodation.reviews]
                        }
                    else:
                        self.send_response(404)
                        self.end_headers()
                        response = {"error": "Accommodation not found"}
                        
                except ValueError:
                    self.send_response(400)
                    self.end_headers()
                    response = {"error": "Invalid accommodation ID"}
                    
            else:
                self.send_response(404)
                self.end_headers()
                response = {"error": "Endpoint not found"}
            
            db.close()
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {"error": f"Internal server error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
            print(f"Error: {e}")
            traceback.print_exc()
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            # Check if it's a review endpoint
            if '/reviews' in path and path.startswith('/api/accommodations/'):
                # Extract accommodation ID
                parts = path.split('/')
                if len(parts) >= 4:
                    try:
                        acc_id = int(parts[3])
                        
                        # Read request body
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        review_data = json.loads(post_data.decode('utf-8'))
                        
                        # Validate required fields
                        if not all(key in review_data for key in ['user_id', 'rating', 'comment']):
                            self.send_response(400)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            response = {"error": "Missing required fields: user_id, rating, comment"}
                            self.wfile.write(json.dumps(response).encode())
                            return
                        
                        db = SessionLocal()
                        
                        # Check if accommodation exists
                        accommodation = get_accommodation_by_id(db, acc_id)
                        if not accommodation:
                            self.send_response(404)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            response = {"error": "Accommodation not found"}
                            self.wfile.write(json.dumps(response).encode())
                            db.close()
                            return
                        
                        # Create review
                        review = ReviewCreate(
                            user_id=review_data['user_id'],
                            rating=review_data['rating'],
                            comment=review_data['comment']
                        )
                        
                        add_review(db, acc_id, review)
                        db.close()
                        
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        response = {"status": "success", "status_code": 200}
                        self.wfile.write(json.dumps(response).encode())
                        
                    except ValueError:
                        self.send_response(400)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        response = {"error": "Invalid accommodation ID"}
                        self.wfile.write(json.dumps(response).encode())
                        
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Endpoint not found"}
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {"error": f"Internal server error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
            print(f"Error: {e}")
            traceback.print_exc()

def run_server(port=8585):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AccommodationAPIHandler)
    print(f"🚀 Accommodation API Server starting on http://localhost:{port}")
    print(f"📋 Available endpoints:")
    print(f"   GET  http://localhost:{port}/api/accommodations/")
    print(f"   GET  http://localhost:{port}/api/accommodations/{{id}}")
    print(f"   POST http://localhost:{port}/api/accommodations/{{id}}/reviews")
    print(f"\n✅ Database connected with 3 sample accommodations!")
    print(f"🔗 Try: http://localhost:{port}/api/accommodations/")
    print(f"Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server() 