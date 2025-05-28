from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chamados.db'
app.config['SECRET_KEY'] = 'chave_secreta'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def brasilia_time():
    tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(tz)

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.DateTime, default=brasilia_time)
    sistema = db.Column(db.String(10), nullable=False)
    user = db.Column(db.String(20), nullable=False)
    num_registro = db.Column(db.Integer, nullable=False)
    numero_nf = db.Column(db.Integer, nullable=False)
    tipo_operacao = db.Column(db.String(20), nullable=False)
    tipo_chamado = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
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
    chamados = Chamado.query.order_by(Chamado.data.desc()).all()
    return render_template('dashboard.html', chamados=chamados)

@app.route('/novo_chamado', methods=['GET', 'POST'])
@login_required
def novo_chamado():
    if request.method == 'POST':
        file = request.files.get('print')
        filename = None
        if file and file.filename:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        chamado = Chamado(
            sistema=request.form['sistema'],
            user=current_user.username,
            num_registro=int(request.form['num_registro']),
            numero_nf=int(request.form['numero_nf']),
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

@app.route('/atualizar_status', methods=['POST'])
@login_required
def atualizar_status():
    chamado_id = request.form.get('id')
    novo_status = request.form.get('status')

    chamado = Chamado.query.get(int(chamado_id))
    if chamado:
        chamado.status = novo_status
        db.session.commit()
        return jsonify({'mensagem': 'Status atualizado com sucesso'})
    return jsonify({'erro': 'Chamado não encontrado'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
