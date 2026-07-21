from flask import Flask, request, jsonify
import psycopg2
import os
import socket

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "barangdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "pass123")
    )

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS barang (
        id SERIAL PRIMARY KEY,
        nama VARCHAR(100),
        harga INT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/health")
def health():
    try:
        conn = get_conn()
        conn.close()

        return jsonify({
            "status": "ok",
            "database": "connected"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/barang", methods=["GET"])
def get_barang():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id,nama,harga FROM barang")

    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify({
        "meta": {
            "api_hostname": socket.gethostname()
        },
        "data": [
            {
                "id": x[0],
                "nama": x[1],
                "harga": x[2]
            } for x in data
        ]
    })

@app.route("/barang", methods=["POST"])
def tambah_barang():
    data = request.get_json()

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO barang (nama,harga) VALUES (%s,%s) RETURNING id",
        (data["nama"], data["harga"])
    )

    new_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "id": new_id,
        "nama": data["nama"],
        "harga": data["harga"]
    })

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)