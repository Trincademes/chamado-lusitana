from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chamados.db'
app.config['SECRET_KEY'] = 'chave_secreta'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    sistema = db.Column(db.String(10))
    user = db.Column(db.String(20))
    num_registro = db.Column(db.Integer)
    numero_nf = db.Column(db.Integer)
    tipo_operacao = db.Column(db.String(20))
    tipo_chamado = db.Column(db.String(20))
    descricao = db.Column(db.Text)
    print_path = db.Column(db.String(500))
    status = db.Column(db.String(10), default='ABERTO')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = Usuario(username=request.form['username'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/dashboard')
@login_required
def dashboard():
    chamados = Chamado.query.all()
    return render_template('dashboard.html', chamados=chamados)

@app.route('/novo_chamado', methods=['GET', 'POST'])
@login_required
def novo_chamado():
    if request.method == 'POST':
        file = request.files['print']
        filename = None
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        chamado = Chamado(
            sistema=request.form['sistema'],
            user=current_user.username,
            num_registro=request.form['num_registro'],
            numero_nf=request.form['numero_nf'],
            tipo_operacao=request.form['tipo_operacao'],
            tipo_chamado=request.form['tipo_chamado'],
            descricao=request.form['descricao'],
            print_path=filename
        )
        db.session.add(chamado)
        db.session.commit()
        flash('Chamado criado com sucesso!')
        return redirect(url_for('dashboard'))
    return render_template('novo_chamado.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
