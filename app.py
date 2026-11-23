import os
import sqlite3
from contextlib import closing
from flask import Flask, jsonify, request


def get_db():
    conn = sqlite3.connect(os.environ.get("DB_PATH", "items.db"))
    conn.row_factory = sqlite3.Row
    return conn


def create_app():
    app = Flask(__name__)
    with closing(get_db()) as db:
        db.execute("CREATE TABLE IF NOT EXISTS items ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "name TEXT NOT NULL, quantity INTEGER NOT NULL)")
        db.commit()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/items")
    def list_items():
        with closing(get_db()) as db:
            rows = db.execute("SELECT id, name, quantity FROM items").fetchall()
        return jsonify([dict(r) for r in rows])

    @app.post("/items")
    def add_item():
        data = request.get_json(silent=True) or {}
        name, quantity = data.get("name"), data.get("quantity")
        if not isinstance(name, str) or not 1 <= len(name) <= 100:
            return {"error": "name invalide"}, 400
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:
            return {"error": "quantity invalide"}, 400
        with closing(get_db()) as db:
            cur = db.execute("INSERT INTO items (name, quantity) VALUES (?, ?)",
                             (name, quantity))
            db.commit()
        return {"id": cur.lastrowid, "name": name, "quantity": quantity}, 201

    return app
