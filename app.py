import mysql.connector
import hashlib
from waitress import serve
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)  # cria uma instância do app
app.config['SECRET_KEY'] = 'chave-secreta'

cnx = mysql.connector.connect(user='root', password='aluno@rsc', host='127.0.0.1', database='seg_info')
cursor = cnx.cursor()

global is_active
is_active = False

@app.route("/")  # no end point /
def index():  # chama o método hello
    return (render_template('index.html'))  # método retorna "hello world"

@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password_sha = hashlib.sha256(request.form.get('password').encode("utf-8")).hexdigest()
    cursor.execute('SELECT * FROM users WHERE email = %s and password = %s',(email, password_sha,))
    user = cursor.fetchone()
    if user:
        global is_active
        is_active = True
        return redirect(url_for('perfil'))
    else:
        flash('Por favor verifique seu login.')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    global is_active
    is_active = False
    return redirect(url_for('index'))

@app.route("/perfil")
def perfil():
    global is_active
    if is_active:
        return(render_template('perfil.html'))
    else:
        return redirect(url_for('index'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password_md5 = hashlib.sha256(request.form.get('password').encode("utf-8")).hexdigest()
    cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (name, email, password_md5,))
    cnx.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":  # rodando o python app.py
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    serve(app, host='0.0.0.0', port=5000)
