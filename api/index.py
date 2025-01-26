from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Prepare the response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Parse the query string for ?name=...
        query = urlparse(self.path).query
        query_params = parse_qs(query)
        # If multiple "name" params: /api?name=Alice&name=Bob, parse_qs gives a list
        names = query_params.get('name', [])

        # Load JSON array from q-vercel-python.json
        file_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')
        with open(file_path, 'r') as f:
            data = json.load(f)  # data is a list of dicts: [{"name":"...", "marks":...}, ...]

        # For each requested name, find the first matching record's "marks"
        marks_list = []
        for name in names:
            found_marks = None
            for item in data:
                if item["name"] == name:
                    found_marks = item["marks"]
                    break
            marks_list.append(found_marks)

        # Create the JSON response
        response_body = {"marks": marks_list}
        self.wfile.write(json.dumps(response_body).encode())
