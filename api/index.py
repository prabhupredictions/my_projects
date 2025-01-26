import json
import os

def handler(request, response):
    # Enable CORS for all origins
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    # Load the JSON array from file: [ { "name": "...", "marks": ... }, ... ]
    file_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')
    with open(file_path, 'r') as f:
        data = json.load(f)  # This will be a list of dicts

    # Get the 'name' query parameters, e.g. /api?name=Alice&name=Bob
    names = request.query_params.getlist("name")  # in some runtimes, .getlist("name") may differ

    # For each requested 'name', find the *first* matching record's "marks".
    # If multiple items share the same name, you'll only get the first match.
    marks_list = []
    for name in names:
        found_marks = None
        for item in data:
            if item["name"] == name:
                found_marks = item["marks"]
                break
        marks_list.append(found_marks)

    # Build the response as JSON
    response.body = json.dumps({"marks": marks_list})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    return response
