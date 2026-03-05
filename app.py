from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "efacec2026"
app.permanent_session_lifetime = timedelta(minutes=5)


def init_db():
    conn = sqlite3.connect('armazem.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS materiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT,
            descricao TEXT,
            localizacao TEXT,
            quantidade INTEGER
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    search = request.args.get('search')
    materiais = []

    if search:
        conn = sqlite3.connect('armazem.db')
        c = conn.cursor()

        c.execute(
            "SELECT * FROM materiais WHERE codigo LIKE ? OR descricao LIKE ?",
            ('%' + search + '%', '%' + search + '%')
        )

        materiais = c.fetchall()
        conn.close()

    return render_template('index.html', materiais=materiais)

    materiais = c.fetchall()
    conn.close()
    return render_template('index.html', materiais=materiais)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == "efacec2026":
            session['logged_in'] = True
            return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')


@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        return redirect('/login')

    codigo = request.form['codigo']
    descricao = request.form['descricao']
    localizacao = request.form['localizacao']
    quantidade = request.form['quantidade']

    conn = sqlite3.connect('armazem.db')
    c = conn.cursor()
    c.execute("INSERT INTO materiais (codigo, descricao, localizacao, quantidade) VALUES (?, ?, ?, ?)",
              (codigo, descricao, localizacao, quantidade))
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):
    if not session.get('logged_in'):
        return redirect('/login')

    conn = sqlite3.connect('armazem.db')
    c = conn.cursor()
    c.execute("SELECT * FROM materiais WHERE id = ?", (id,))
    material = c.fetchone()
    conn.close()
    return render_template('edit.html', material=material)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not session.get('logged_in'):
        return redirect('/login')

    codigo = request.form['codigo']
    descricao = request.form['descricao']
    localizacao = request.form['localizacao']
    quantidade = request.form['quantidade']

    conn = sqlite3.connect('armazem.db')
    c = conn.cursor()
    c.execute("""
        UPDATE materiais
        SET codigo=?, descricao=?, localizacao=?, quantidade=?
        WHERE id=?
    """, (codigo, descricao, localizacao, quantidade, id))
    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)