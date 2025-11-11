from decimal import Decimal
from typing import Optional
from config import get_db_connection

def _to_int_or_none(value) -> Optional[int]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    try:
        return int(s)
    except Exception:
        return None

def _to_decimal_or_none(value) -> Optional[Decimal]:
    if value is None:
        return None
    s = str(value).strip().replace(',', '.')
    if s == "":
        return None
    try:
        return Decimal(s)
    except Exception:
        return None


def get_autores():
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Autores")
        return cur.fetchall()
    finally:
        conn.close()

def insert_autor(nome, nacionalidade, data_nascimento, biografia):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia) VALUES (%s,%s,%s,%s)",
            (nome, nacionalidade or None, data_nascimento or None, biografia or None)
        )
        conn.commit()
    finally:
        conn.close()

def update_autor(id, nome, nacionalidade, data_nascimento, biografia):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """UPDATE Autores SET Nome_autor=%s, Nacionalidade=%s, Data_nascimento=%s, Biografia=%s
               WHERE ID_autor=%s""",
            (nome, nacionalidade or None, data_nascimento or None, biografia or None, id)
        )
        conn.commit()
    finally:
        conn.close()

def delete_autor(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Autores WHERE ID_autor=%s", (id,))
        conn.commit()
    finally:
        conn.close()


def get_generos():
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Generos")
        return cur.fetchall()
    finally:
        conn.close()

def insert_genero(nome):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Generos (Nome_genero) VALUES (%s)", (nome,))
        conn.commit()
    finally:
        conn.close()

def update_genero(id, nome):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE Generos SET Nome_genero=%s WHERE ID_genero=%s", (nome, id))
        conn.commit()
    finally:
        conn.close()

def delete_genero(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Generos WHERE ID_genero=%s", (id,))
        conn.commit()
    finally:
        conn.close()


def get_editoras():
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Editoras")
        return cur.fetchall()
    finally:
        conn.close()

def insert_editora(nome, endereco):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Editoras (Nome_editora, Endereco_editora) VALUES (%s,%s)", (nome, endereco or None))
        conn.commit()
    finally:
        conn.close()

def update_editora(id, nome, endereco):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE Editoras SET Nome_editora=%s, Endereco_editora=%s WHERE ID_editora=%s", (nome, endereco or None, id))
        conn.commit()
    finally:
        conn.close()

def delete_editora(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Editoras WHERE ID_editora=%s", (id,))
        conn.commit()
    finally:
        conn.close()


def get_livros():
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
        SELECT L.*, A.Nome_autor, G.Nome_genero, E.Nome_editora
        FROM Livros L
        LEFT JOIN Autores A ON L.Autor_id=A.ID_autor
        LEFT JOIN Generos G ON L.Genero_id=G.ID_genero
        LEFT JOIN Editoras E ON L.Editora_id=E.ID_editora
    """)
        return cur.fetchall()
    finally:
        conn.close()

def insert_livro(titulo, autor, isbn, ano, genero, editora, qtd, resumo):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO Livros 
        (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (
            titulo,
            _to_int_or_none(autor),
            isbn,
            _to_int_or_none(ano),
            _to_int_or_none(genero),
            _to_int_or_none(editora),
            _to_int_or_none(qtd),
            resumo or None
        ))
        conn.commit()
    finally:
        conn.close()

def update_livro(id, titulo, autor, isbn, ano, genero, editora, qtd, resumo):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""UPDATE Livros SET 
        Titulo=%s, Autor_id=%s, ISBN=%s, Ano_publicacao=%s, Genero_id=%s, Editora_id=%s, Quantidade_disponivel=%s, Resumo=%s
        WHERE ID_livro=%s""",
        (
            titulo,
            _to_int_or_none(autor),
            isbn,
            _to_int_or_none(ano),
            _to_int_or_none(genero),
            _to_int_or_none(editora),
            _to_int_or_none(qtd),
            resumo or None,
            id
        ))
        conn.commit()
    finally:
        conn.close()

def delete_livro(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Livros WHERE ID_livro=%s", (id,))
        conn.commit()
    finally:
        conn.close()


def get_usuarios():
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Usuarios")
        return cur.fetchall()
    finally:
        conn.close()

def insert_usuario(nome, email, telefone, data, multa):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
                   VALUES (%s,%s,%s,%s,%s)""",
                (nome, email or None, telefone or None, data or None, _to_decimal_or_none(multa)))
        conn.commit()
    finally:
        conn.close()

def update_usuario(id, nome, email, telefone, data, multa):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""UPDATE Usuarios SET Nome_usuario=%s, Email=%s, Numero_telefone=%s, Data_inscricao=%s, Multa_atual=%s
                   WHERE ID_usuario=%s""",
                (nome, email or None, telefone or None, data or None, _to_decimal_or_none(multa), id))
        conn.commit()
    finally:
        conn.close()

def delete_usuario(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Usuarios WHERE ID_usuario=%s", (id,))
        conn.commit()
    finally:
        conn.close()


def get_emprestimos():
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
        SELECT E.*, U.Nome_usuario, L.Titulo 
        FROM Emprestimos E
        LEFT JOIN Usuarios U ON E.Usuario_id=U.ID_usuario
        LEFT JOIN Livros L ON E.Livro_id=L.ID_livro
    """)
        return cur.fetchall()
    finally:
        conn.close()

def insert_emprestimo(usuario, livro, d_emp, d_prev, d_real, status):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO Emprestimos 
        (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, Data_devolucao_real, Status_emprestimo)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (_to_int_or_none(usuario), _to_int_or_none(livro), d_emp or None, d_prev or None, d_real or None, status))
        conn.commit()
    finally:
        conn.close()

def update_emprestimo(id, usuario, livro, d_emp, d_prev, d_real, status):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""UPDATE Emprestimos SET Usuario_id=%s, Livro_id=%s, Data_emprestimo=%s, 
        Data_devolucao_prevista=%s, Data_devolucao_real=%s, Status_emprestimo=%s WHERE ID_emprestimo=%s""",
        (_to_int_or_none(usuario), _to_int_or_none(livro), d_emp or None, d_prev or None, d_real or None, status, id))
        conn.commit()
    finally:
        conn.close()

def delete_emprestimo(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Emprestimos WHERE ID_emprestimo=%s", (id,))
        conn.commit()
    finally:
        conn.close()
