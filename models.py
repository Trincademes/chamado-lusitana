from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relacionamento com o modelo 'Modelo'
    modelos = db.relationship('Modelo', backref='usuario', lazy=True)
    
class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    hora = db.Column(db.Integer, nullable=False)  # Nova coluna para a hora
    minuto = db.Column(db.Integer, nullable=False)  # Nova coluna para o minuto
    apresentacao = db.Column(db.String(100), nullable=False)
    agendamento = db.Column(db.String(100), nullable=False)
    tipo_operacao = db.Column(db.String(100), nullable=False)
    numero_bs = db.Column(db.String(100), nullable=False)
    numero_nf = db.Column(db.String(100), nullable=False)
    transportadora = db.Column(db.String(100), nullable=False)
    tipo_veiculo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(100), nullable=False)
    placa_cavalo = db.Column(db.String(100), nullable=False)
    placa_carreta = db.Column(db.String(100), nullable=False)
    numero_container = db.Column(db.String(100), nullable=False)
    documentos = db.Column(db.String(500), nullable=True)  # Armazena os nomes dos arquivos como uma string

    # Adicionando o campo para associar ao usuário (foreign key)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relacionamento de volta, se necessário
    # usuario = db.relationship('Usuario', back_populates='modelos')

