from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
from MySQLdb import IntegrityError

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_atividade17'

# Inicializa a conexão com o MySQL
mysql = MySQL(app)


# ============================ HOME ============================
@app.route('/')
def index():
    return render_template('index.html')


# ============================ AUTORES ============================
@app.route('/autores')
def listar_autores():
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM autores")
    autores = cursor.fetchall()
    cursor.close()
    return render_template('autores.html', autores=autores)


@app.route('/autores/add', methods=['GET', 'POST'])
def adicionar_autor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        nacionalidade = request.form.get('nacionalidade')
        data_nasc = request.form.get('data_nascimento')
        biografia = request.form.get('biografia')

        if not nome:
            flash("O campo nome é obrigatório!", "danger")
            return redirect(url_for('adicionar_autor'))

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia)
            VALUES (%s, %s, %s, %s)
        """, (nome, nacionalidade, data_nasc, biografia))
        mysql.connection.commit()
        cursor.close()
        flash('Autor adicionado com sucesso!', 'success')
        return redirect(url_for('listar_autores'))

    return render_template('adicionar_autor.html')


@app.route('/autores/editar/<int:id>', methods=['GET', 'POST'])
def editar_autor(id):
    cursor = mysql.connection.cursor(DictCursor)
    if request.method == 'POST':
        nome = request.form.get('nome')
        nacionalidade = request.form.get('nacionalidade')
        data_nasc = request.form.get('data_nascimento')
        biografia = request.form.get('biografia')

        if not nome:
            flash("O campo nome é obrigatório!", "danger")
            return redirect(url_for('editar_autor', id=id))

        cursor.execute("""
            UPDATE autores
            SET Nome_autor=%s, Nacionalidade=%s, Data_nascimento=%s, Biografia=%s
            WHERE ID_autor=%s
        """, (nome, nacionalidade, data_nasc, biografia, id))
        mysql.connection.commit()
        cursor.close()
        flash('Autor atualizado com sucesso!', 'info')
        return redirect(url_for('listar_autores'))

    cursor.execute("SELECT * FROM autores WHERE ID_autor=%s", (id,))
    autor = cursor.fetchone()
    cursor.close()
    return render_template('editar_autor.html', autor=autor)


@app.route('/autores/excluir/<int:id>', methods=['POST'])
def excluir_autor(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM autores WHERE ID_autor=%s", (id,))
        mysql.connection.commit()
        flash('Autor excluído com sucesso!', 'danger')
    except IntegrityError:
        mysql.connection.rollback()
        flash('Não é possível excluir este autor, pois há livros vinculados a ele!', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('listar_autores'))


# ============================ GÊNEROS ============================
@app.route('/generos')
def listar_generos():
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM generos")
    generos = cursor.fetchall()
    cursor.close()
    return render_template('generos.html', generos=generos)


@app.route('/generos/add', methods=['GET', 'POST'])
def adicionar_genero():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash("O campo nome é obrigatório!", "danger")
            return redirect(url_for('adicionar_genero'))

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO generos (Nome_genero) VALUES (%s)", (nome,))
        mysql.connection.commit()
        cursor.close()
        flash('Gênero adicionado com sucesso!', 'success')
        return redirect(url_for('listar_generos'))

    return render_template('adicionar_genero.html')


@app.route('/generos/editar/<int:id>', methods=['GET', 'POST'])
def editar_genero(id):
    cursor = mysql.connection.cursor(DictCursor)
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash("O campo nome é obrigatório!", "danger")
            return redirect(url_for('editar_genero', id=id))

        cursor.execute("UPDATE generos SET Nome_genero=%s WHERE ID_genero=%s", (nome, id))
        mysql.connection.commit()
        cursor.close()
        flash('Gênero atualizado com sucesso!', 'info')
        return redirect(url_for('listar_generos'))

    cursor.execute("SELECT * FROM generos WHERE ID_genero=%s", (id,))
    genero = cursor.fetchone()
    cursor.close()
    return render_template('editar_genero.html', genero=genero)


@app.route('/generos/excluir/<int:id>', methods=['POST'])
def excluir_genero(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM generos WHERE ID_genero=%s", (id,))
        mysql.connection.commit()
        flash('Gênero excluído com sucesso!', 'success')
    except IntegrityError:
        mysql.connection.rollback()
        flash('Não é possível excluir este gênero, pois há livros vinculados a ele!', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('listar_generos'))


# ============================ EDITORAS ============================
@app.route('/editoras')
def listar_editoras():
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM editoras")
    editoras = cursor.fetchall()
    cursor.close()
    return render_template('editoras.html', editoras=editoras)


@app.route('/editoras/add', methods=['GET', 'POST'])
def adicionar_editora():
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        if not nome:
            flash("O campo nome é obrigatório!", "danger")
            return redirect(url_for('adicionar_editora'))

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO editoras (Nome_editora, Endereco_editora) VALUES (%s, %s)", (nome, endereco))
        mysql.connection.commit()
        cursor.close()
        flash('Editora adicionada com sucesso!', 'success')
        return redirect(url_for('listar_editoras'))

    return render_template('adicionar_editora.html')


@app.route('/editoras/editar/<int:id>', methods=['GET', 'POST'])
def editar_editora(id):
    cursor = mysql.connection.cursor(DictCursor)
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        if not nome:
            flash("O campo nome é obrigatório!", "danger")
            return redirect(url_for('editar_editora', id=id))

        cursor.execute("UPDATE editoras SET Nome_editora=%s, Endereco_editora=%s WHERE ID_editora=%s", (nome, endereco, id))
        mysql.connection.commit()
        cursor.close()
        flash('Editora atualizada com sucesso!', 'info')
        return redirect(url_for('listar_editoras'))

    cursor.execute("SELECT * FROM editoras WHERE ID_editora=%s", (id,))
    editora = cursor.fetchone()
    cursor.close()
    return render_template('editar_editora.html', editora=editora)


@app.route('/editoras/excluir/<int:id>', methods=['POST'])
def excluir_editora(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM editoras WHERE ID_editora=%s", (id,))
        mysql.connection.commit()
        flash('Editora excluída com sucesso!', 'success')
    except IntegrityError:
        mysql.connection.rollback()
        flash('Não é possível excluir esta editora se houver livros vinculados a ela!', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('listar_editoras'))


# ============================ LIVROS ============================
@app.route('/livros')
def listar_livros():
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT l.*, a.Nome_autor, g.Nome_genero, e.Nome_editora
        FROM livros l
        LEFT JOIN autores a ON l.Autor_id = a.ID_autor
        LEFT JOIN generos g ON l.Genero_id = g.ID_genero
        LEFT JOIN editoras e ON l.Editora_id = e.ID_editora
    """)
    livros = cursor.fetchall()
    cursor.close()
    return render_template('livros.html', livros=livros)


@app.route('/livros/add', methods=['GET', 'POST'])
def adicionar_livro():
    cursor = mysql.connection.cursor(DictCursor)
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor_id = request.form.get('autor')
        genero_id = request.form.get('genero')
        editora_id = request.form.get('editora')
        resumo = request.form.get('resumo')
        quantidade = request.form.get('quantidade') or 0
        ano_publicacao = request.form.get('ano_publicacao') or None

        if not titulo:
            flash("O campo título é obrigatório!", "danger")
            return redirect(url_for('adicionar_livro'))

        # garantir tipos corretos para quantidade
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            quantidade = 0

        cursor.execute("""
            INSERT INTO livros (Titulo, Autor_id, Genero_id, Editora_id, Resumo, Quantidade_disponivel, Ano_publicacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (titulo, autor_id or None, genero_id or None, editora_id or None, resumo, quantidade, ano_publicacao))
        mysql.connection.commit()
        cursor.close()
        flash('Livro adicionado com sucesso!', 'success')
        return redirect(url_for('listar_livros'))

    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM autores")
    autores = cursor.fetchall()
    cursor.execute("SELECT * FROM generos")
    generos = cursor.fetchall()
    cursor.execute("SELECT * FROM editoras")
    editoras = cursor.fetchall()
    cursor.close()
    return render_template('adicionar_livro.html', autores=autores, generos=generos, editoras=editoras)


@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    cursor = mysql.connection.cursor(DictCursor)
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor_id = request.form.get('autor')
        genero_id = request.form.get('genero')
        editora_id = request.form.get('editora')
        resumo = request.form.get('resumo')
        quantidade = request.form.get('quantidade') or 0
        ano_publicacao = request.form.get('ano_publicacao') or None

        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            quantidade = 0

        cursor.execute("""
            UPDATE livros
            SET Titulo=%s, Autor_id=%s, Genero_id=%s, Editora_id=%s, Resumo=%s, Quantidade_disponivel=%s, Ano_publicacao=%s
            WHERE ID_livro=%s
        """, (titulo, autor_id or None, genero_id or None, editora_id or None, resumo, quantidade, ano_publicacao, id))
        mysql.connection.commit()
        cursor.close()
        flash('Livro atualizado com sucesso!', 'info')
        return redirect(url_for('listar_livros'))

    cursor.execute("SELECT * FROM livros WHERE ID_livro=%s", (id,))
    livro = cursor.fetchone()
    cursor.execute("SELECT * FROM autores")
    autores = cursor.fetchall()
    cursor.execute("SELECT * FROM generos")
    generos = cursor.fetchall()
    cursor.execute("SELECT * FROM editoras")
    editoras = cursor.fetchall()
    cursor.close()
    return render_template('editar_livro.html', livro=livro, autores=autores, generos=generos, editoras=editoras)


@app.route('/livros/excluir/<int:id>', methods=['POST'])
def excluir_livro(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM livros WHERE ID_livro=%s", (id,))
        mysql.connection.commit()
        flash('Livro excluído com sucesso!', 'danger')
    except IntegrityError:
        mysql.connection.rollback()
        flash('Não é possível excluir este livro, pois há empréstimos vinculados a ele!', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('listar_livros'))


# ============================ USUÁRIOS ============================
@app.route('/usuarios')
def listar_usuarios():
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/usuarios/add', methods=['GET', 'POST'])
def adicionar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone') or request.form.get('Numero_telefone') or None
        data_inscricao = request.form.get('data_inscricao')
        multa = request.form.get('multa') or 0

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO usuarios (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, email, telefone, data_inscricao, multa))
        mysql.connection.commit()
        cursor.close()
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))

    return render_template('adicionar_usuario.html')


@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    cursor = mysql.connection.cursor(DictCursor)
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone') or request.form.get('Numero_telefone') or None
        data_inscricao = request.form.get('data_inscricao')
        multa = request.form.get('multa') or 0

        cursor.execute("""
            UPDATE usuarios
            SET Nome_usuario=%s, Email=%s, Numero_telefone=%s, Data_inscricao=%s, Multa_atual=%s
            WHERE ID_usuario=%s
        """, (nome, email, telefone, data_inscricao, multa, id))
        mysql.connection.commit()
        cursor.close()
        flash('Usuário atualizado com sucesso!', 'info')
        return redirect(url_for('listar_usuarios'))

    cursor.execute("SELECT * FROM usuarios WHERE ID_usuario=%s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    return render_template('editar_usuario.html', usuario=usuario)


@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
def excluir_usuario(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE ID_usuario=%s", (id,))
        mysql.connection.commit()
        flash('Usuário excluído com sucesso!', 'danger')
    except IntegrityError:
        mysql.connection.rollback()
        flash('Não é possível excluir este usuário, pois há empréstimos vinculados a ele!', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('listar_usuarios'))


# ============================ EMPRÉSTIMOS ============================
@app.route('/emprestimos')
def listar_emprestimos():
    cursor = mysql.connection.cursor(DictCursor)
    cursor.execute("""
        SELECT ep.*, u.Nome_usuario, l.Titulo
        FROM emprestimos ep
        LEFT JOIN usuarios u ON ep.Usuario_id = u.ID_usuario
        LEFT JOIN livros l ON ep.Livro_id = l.ID_livro
        ORDER BY ep.Data_emprestimo DESC
    """)
    emprestimos = cursor.fetchall()
    cursor.close()
    return render_template('emprestimos.html', emprestimos=emprestimos)


# ============================ ADICIONAR EMPRÉSTIMO ============================
@app.route('/emprestimos/add', methods=['GET', 'POST'])
def adicionar_emprestimo():
    cursor = mysql.connection.cursor(DictCursor)
    if request.method == 'POST':
        usuario_id = request.form.get('usuario')
        livro_id = request.form.get('livro')
        data_emprestimo = request.form.get('data_emprestimo')
        data_prevista = request.form.get('data_prevista')

        # Verifica se o livro está disponível
        cursor.execute("SELECT Quantidade_disponivel FROM livros WHERE ID_livro=%s", (livro_id,))
        livro = cursor.fetchone()
        if not livro or livro['Quantidade_disponivel'] <= 0:
            flash('Livro indisponível para empréstimo!', 'danger')
            cursor.close()
            return redirect(url_for('listar_emprestimos'))

        # Insere o empréstimo
        cursor.execute("""
            INSERT INTO emprestimos (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, Status_emprestimo)
            VALUES (%s, %s, %s, %s, 'pendente')
        """, (usuario_id, livro_id, data_emprestimo, data_prevista))

        # Atualiza a quantidade disponível do livro
        cursor.execute("UPDATE livros SET Quantidade_disponivel = Quantidade_disponivel - 1 WHERE ID_livro=%s", (livro_id,))

        mysql.connection.commit()
        cursor.close()
        flash('Empréstimo realizado com sucesso!', 'success')
        return redirect(url_for('listar_emprestimos'))

    # GET - buscar usuários e livros
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    cursor.close()
    return render_template('adicionar_emprestimo.html', usuarios=usuarios, livros=livros)


@app.route('/emprestimos/devolver/<int:id>', methods=['POST'])
def devolver_emprestimo(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT Livro_id FROM emprestimos WHERE ID_emprestimo=%s", (id,))
    emprestimo = cursor.fetchone()
    cursor.execute("""
        UPDATE emprestimos
        SET Data_devolucao_real = CURDATE(), Status_emprestimo = 'devolvido'
        WHERE ID_emprestimo = %s
    """, (id,))
    mysql.connection.commit()
    cursor.close()
    flash("Livro devolvido com sucesso!", "info")
    return redirect(url_for('listar_emprestimos'))


@app.route('/emprestimos/excluir/<int:id>', methods=['POST'])
def excluir_emprestimo(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM emprestimos WHERE ID_emprestimo = %s", (id,))
        mysql.connection.commit()
        flash('Empréstimo excluído com sucesso!', 'danger')
    except Exception:
        mysql.connection.rollback()
        flash('Erro ao excluir o empréstimo!', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('listar_emprestimos'))

# ================================================================
if __name__ == '__main__':
    app.run(debug=True)
