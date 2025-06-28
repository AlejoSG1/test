from flask import Flask, request, Response

app = Flask(__name__)

# Replace with your real credentials
USERNAME = "admin"
PASSWORD = "supersecure"

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        "Authentication Required", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@app.route("/")
def home():
    return "✅ Welcome! You are authenticated."

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
