from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

API_URL = os.getenv("API_URL", "http://api:8080")

@app.route("/")
def index():
    try:
        response = requests.get(f"{API_URL}/barang")
        data = response.json().get("data", [])
    except:
        data = []

    return render_template("index.html", barang=data)

@app.route("/tambah", methods=["POST"])
def tambah():
    nama = request.form["nama"]
    harga = request.form["harga"]

    requests.post(
        f"{API_URL}/barang",
        json={
            "nama": nama,
            "harga": int(harga)
        }
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  