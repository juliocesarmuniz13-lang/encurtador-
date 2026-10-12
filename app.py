import sqlite3
import random
import string
from flask import Flask, request, redirect, render_template, abort

app = Flask(__name__)
DB = "links.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela():
    with get_db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS links ("
            "codigo TEXT PRIMARY KEY, url TEXT NOT NULL)"
        )


def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(tamanho))


@app.route("/", methods=["GET", "POST"])
def index():
    link_curto = None
    if request.method == "POST":
        url = request.form["url"].strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        codigo = gerar_codigo()
        with get_db() as conn:
            conn.execute("INSERT INTO links (codigo, url) VALUES (?, ?)", (codigo, url))
        link_curto = request.host_url + codigo

    return render_template("index.html", link_curto=link_curto)


@app.route("/<codigo>")
def redirecionar(codigo):
    with get_db() as conn:
        linha = conn.execute(
            "SELECT url FROM links WHERE codigo = ?", (codigo,)
        ).fetchone()
    if linha is None:
        abort(404)
    return redirect(linha["url"])


criar_tabela()

if __name__ == "__main__":
    app.run()
