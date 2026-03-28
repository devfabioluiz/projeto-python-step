
from typing import Optional

from fastapi import FastAPI
import sqlite3

# IMPORTANTE: executa a criação do banco/tabela
import app.database.db

app = FastAPI()

def get_connection():
    return sqlite3.connect("database.db")

@app.get("/")
def home():
    return {"msg": "API rodando"}

@app.get("/usuarios")
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()

    conn.close()
    return dados

@app.get("/usuarios/{id}")
def obter_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    dados = cursor.fetchall()

    conn.close()
    return dados

@app.post("/usuarios")
def criar_usuario(nome: str, idade: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nome, idade) VALUES (?, ?)",
        (nome, idade)
    )

    conn.commit()
    conn.close()

    return {"msg": "Usuário criado"}

@app.delete("/usuarios/{id}")
def deletar_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"msg": "Usuário deletado"}

@app.put("/usuarios/{id}")
def atualizar_usuario(id: int, nome: str, idade: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?",
        (nome, idade, id)
    )

    conn.commit()
    conn.close()

    return {"msg": "Usuário atualizado"}

@app.post("/produtos")
def criar_produto(nome: str, categoria: str, preco: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO produtos (nome, categoria, preco) VALUES (?, ?, ?)",
        (nome, categoria, preco)
    )

    conn.commit()
    conn.close()

    return {"msg": "Produto criado"}

@app.get("/produtos")
def listar_produtos(
    categoria: str,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None
):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM produtos WHERE 1=1"
    params = []

    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)

    if preco_min:
        query += " AND preco >= ?"
        params.append(preco_min)

    if preco_max:
        query += " AND preco <= ?"
        params.append(preco_max)

    cursor.execute(query, tuple(params))
    dados = cursor.fetchall()

    conn.close()
    return dados