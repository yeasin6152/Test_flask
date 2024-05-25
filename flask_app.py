from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    if request.method == 'GET':
        # Handle GET requests
        return "This is a GET request"
    elif request.method == 'POST':
        # Handle POST requests
        return "This is a POST request"

if __name__ == "__main__":
    app.run(debug=True)
