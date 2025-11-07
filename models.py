from config import get_db_connection

# ---------------- AUTORES ----------------
def get_autores():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Autores")
    data = cur.fetchall()
    conn.close()
    return data

def insert_autor(nome, nacionalidade, data_nascimento, biografia):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia) VALUES (%s,%s,%s,%s)",
                (nome, nacionalidade, data_nascimento, biografia))
    conn.commit()
    conn.close()

def update_autor(id, nome, nacionalidade, data_nascimento, biografia):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE Autores SET Nome_autor=%s, Nacionalidade=%s, Data_nascimento=%s, Biografia=%s
                   WHERE ID_autor=%s""",
                (nome, nacionalidade, data_nascimento, biografia, id))
    conn.commit()
    conn.close()

def delete_autor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Autores WHERE ID_autor=%s", (id,))
    conn.commit()
    conn.close()


# ---------------- GENEROS ----------------
def get_generos():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Generos")
    data = cur.fetchall()
    conn.close()
    return data

def insert_genero(nome):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Generos (Nome_genero) VALUES (%s)", (nome,))
    conn.commit()
    conn.close()

def update_genero(id, nome):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Generos SET Nome_genero=%s WHERE ID_genero=%s", (nome, id))
    conn.commit()
    conn.close()

def delete_genero(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Generos WHERE ID_genero=%s", (id,))
    conn.commit()
    conn.close()


# ---------------- EDITORAS ----------------
def get_editoras():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Editoras")
    data = cur.fetchall()
    conn.close()
    return data

def insert_editora(nome, endereco):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Editoras (Nome_editora, Endereco_editora) VALUES (%s,%s)", (nome, endereco))
    conn.commit()
    conn.close()

def update_editora(id, nome, endereco):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Editoras SET Nome_editora=%s, Endereco_editora=%s WHERE ID_editora=%s", (nome, endereco, id))
    conn.commit()
    conn.close()

def delete_editora(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Editoras WHERE ID_editora=%s", (id,))
    conn.commit()
    conn.close()


# ---------------- LIVROS ----------------
def get_livros():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT L.*, A.Nome_autor, G.Nome_genero, E.Nome_editora
        FROM Livros L
        LEFT JOIN Autores A ON L.Autor_id=A.ID_autor
        LEFT JOIN Generos G ON L.Genero_id=G.ID_genero
        LEFT JOIN Editoras E ON L.Editora_id=E.ID_editora
    """)
    data = cur.fetchall()
    conn.close()
    return data

def insert_livro(titulo, autor, isbn, ano, genero, editora, qtd, resumo):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO Livros 
        (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (titulo, autor, isbn, ano, genero, editora, qtd, resumo))
    conn.commit()
    conn.close()

def update_livro(id, titulo, autor, isbn, ano, genero, editora, qtd, resumo):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE Livros SET 
        Titulo=%s, Autor_id=%s, ISBN=%s, Ano_publicacao=%s, Genero_id=%s, Editora_id=%s, Quantidade_disponivel=%s, Resumo=%s
        WHERE ID_livro=%s""",
        (titulo, autor, isbn, ano, genero, editora, qtd, resumo, id))
    conn.commit()
    conn.close()

def delete_livro(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Livros WHERE ID_livro=%s", (id,))
    conn.commit()
    conn.close()


# ---------------- USUARIOS ----------------
def get_usuarios():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Usuarios")
    data = cur.fetchall()
    conn.close()
    return data

def insert_usuario(nome, email, telefone, data, multa):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
                   VALUES (%s,%s,%s,%s,%s)""",
                (nome, email, telefone, data, multa))
    conn.commit()
    conn.close()

def update_usuario(id, nome, email, telefone, data, multa):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE Usuarios SET Nome_usuario=%s, Email=%s, Numero_telefone=%s, Data_inscricao=%s, Multa_atual=%s
                   WHERE ID_usuario=%s""",
                (nome, email, telefone, data, multa, id))
    conn.commit()
    conn.close()

def delete_usuario(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Usuarios WHERE ID_usuario=%s", (id,))
    conn.commit()
    conn.close()


# ---------------- EMPRESTIMOS ----------------
def get_emprestimos():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT E.*, U.Nome_usuario, L.Titulo 
        FROM Emprestimos E
        LEFT JOIN Usuarios U ON E.Usuario_id=U.ID_usuario
        LEFT JOIN Livros L ON E.Livro_id=L.ID_livro
    """)
    data = cur.fetchall()
    conn.close()
    return data

def insert_emprestimo(usuario, livro, d_emp, d_prev, d_real, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO Emprestimos 
        (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, Data_devolucao_real, Status_emprestimo)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (usuario, livro, d_emp, d_prev, d_real, status))
    conn.commit()
    conn.close()

def update_emprestimo(id, usuario, livro, d_emp, d_prev, d_real, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE Emprestimos SET Usuario_id=%s, Livro_id=%s, Data_emprestimo=%s, 
        Data_devolucao_prevista=%s, Data_devolucao_real=%s, Status_emprestimo=%s WHERE ID_emprestimo=%s""",
        (usuario, livro, d_emp, d_prev, d_real, status, id))
    conn.commit()
    conn.close()

def delete_emprestimo(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Emprestimos WHERE ID_emprestimo=%s", (id,))
    conn.commit()
    conn.close()
