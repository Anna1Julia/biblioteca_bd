from flask import Flask, render_template, request, redirect, url_for
import models

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/autores')
def autores():
    autores = models.get_autores()
    return render_template('autores.html', autores=autores)

@app.route('/autores/add', methods=['POST'])
def add_autor():
    models.insert_autor(
        request.form['nome'],
        request.form['nacionalidade'],
        request.form['data_nascimento'],
        request.form['biografia']
    )
    return redirect(url_for('autores'))

@app.route('/autores/edit/<int:id>', methods=['POST'])
def edit_autor(id):
    models.update_autor(
        id,
        request.form['nome'],
        request.form['nacionalidade'],
        request.form['data_nascimento'],
        request.form['biografia']
    )
    return redirect(url_for('autores'))

@app.route('/autores/delete/<int:id>')
def delete_autor(id):
    models.delete_autor(id)
    return redirect(url_for('autores'))

@app.route('/generos')
def generos():
    generos = models.get_generos()
    return render_template('generos.html', generos=generos)

@app.route('/generos/add', methods=['POST'])
def add_genero():
    models.insert_genero(request.form['nome'])
    return redirect(url_for('generos'))

@app.route('/generos/edit/<int:id>', methods=['POST'])
def edit_genero(id):
    models.update_genero(id, request.form['nome'])
    return redirect(url_for('generos'))

@app.route('/generos/delete/<int:id>')
def delete_genero(id):
    models.delete_genero(id)
    return redirect(url_for('generos'))

@app.route('/editoras')
def editoras():
    editoras = models.get_editoras()
    return render_template('editoras.html', editoras=editoras)

@app.route('/editoras/add', methods=['POST'])
def add_editora():
    models.insert_editora(request.form['nome'], request.form['endereco'])
    return redirect(url_for('editoras'))

@app.route('/editoras/edit/<int:id>', methods=['POST'])
def edit_editora(id):
    models.update_editora(id, request.form['nome'], request.form['endereco'])
    return redirect(url_for('editoras'))

@app.route('/editoras/delete/<int:id>')
def delete_editora(id):
    models.delete_editora(id)
    return redirect(url_for('editoras'))

@app.route('/livros')
def livros():
    livros = models.get_livros()
    autores = models.get_autores()
    generos = models.get_generos()
    editoras = models.get_editoras()
    return render_template('livros.html', livros=livros, autores=autores, generos=generos, editoras=editoras)

@app.route('/livros/add', methods=['POST'])
def add_livro():
    models.insert_livro(
        request.form['titulo'],
        request.form['autor'],
        request.form['isbn'],
        request.form['ano'],
        request.form['genero'],
        request.form['editora'],
        request.form['quantidade'],
        request.form['resumo']
    )
    return redirect(url_for('livros'))

@app.route('/livros/edit/<int:id>', methods=['POST'])
def edit_livro(id):
    models.update_livro(
        id,
        request.form['titulo'],
        request.form['autor'],
        request.form['isbn'],
        request.form['ano'],
        request.form['genero'],
        request.form['editora'],
        request.form['quantidade'],
        request.form['resumo']
    )
    return redirect(url_for('livros'))

@app.route('/livros/delete/<int:id>')
def delete_livro(id):
    models.delete_livro(id)
    return redirect(url_for('livros'))

@app.route('/usuarios')
def usuarios():
    usuarios = models.get_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/add', methods=['POST'])
def add_usuario():
    models.insert_usuario(
        request.form['nome'],
        request.form['email'],
        request.form['telefone'],
        request.form['data_inscricao'],
        request.form['multa']
    )
    return redirect(url_for('usuarios'))

@app.route('/usuarios/edit/<int:id>', methods=['POST'])
def edit_usuario(id):
    models.update_usuario(
        id,
        request.form['nome'],
        request.form['email'],
        request.form['telefone'],
        request.form['data_inscricao'],
        request.form['multa']
    )
    return redirect(url_for('usuarios'))

@app.route('/usuarios/delete/<int:id>')
def delete_usuario(id):
    models.delete_usuario(id)
    return redirect(url_for('usuarios'))

@app.route('/emprestimos')
def emprestimos():
    emprestimos = models.get_emprestimos()
    usuarios = models.get_usuarios()
    livros = models.get_livros()
    return render_template('emprestimos.html', emprestimos=emprestimos, usuarios=usuarios, livros=livros)

@app.route('/emprestimos/add', methods=['POST'])
def add_emprestimo():
    models.insert_emprestimo(
        request.form['usuario'],
        request.form['livro'],
        request.form['data_emprestimo'],
        request.form['data_prevista'],
        request.form['data_real'],
        request.form['status']
    )
    return redirect(url_for('emprestimos'))

@app.route('/emprestimos/edit/<int:id>', methods=['POST'])
def edit_emprestimo(id):
    models.update_emprestimo(
        id,
        request.form['usuario'],
        request.form['livro'],
        request.form['data_emprestimo'],
        request.form['data_prevista'],
        request.form['data_real'],
        request.form['status']
    )
    return redirect(url_for('emprestimos'))

@app.route('/emprestimos/delete/<int:id>')
def delete_emprestimo(id):
    models.delete_emprestimo(id)
    return redirect(url_for('emprestimos'))


if __name__ == '__main__':
    app.run(debug=True)
