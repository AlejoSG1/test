from flask import Flask, request, jsonify, Response
import psycopg2

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

# CONEXIÓN A POSTGRESQL
def get_connection():
    return psycopg2.connect(
        dbname="cruddb",
        user="alejo",
        password="1234",
        host="127.0.0.1",
        port="5432"
    )

# RUTAS CRUD

@app.route("/")
def home():
    return "✅ Bienvenido, estás autenticado."

@app.route("/contacts", methods=["GET"])
def list_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM contacts ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "email": r[2]} for r in rows])

@app.route("/contacts", methods=["POST"])
def create_contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, email) VALUES (%s, %s) RETURNING id;", (name, email))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Contact created", "id": new_id}), 201

@app.route("/contacts/<int:id>", methods=["PUT"])
def update_contact(id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET name=%s, email=%s WHERE id=%s;", (name, email, id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Contact updated"})

@app.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Contact deleted"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)