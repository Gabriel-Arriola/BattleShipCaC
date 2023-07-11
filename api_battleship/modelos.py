from app import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.Text, nullable=False)
    tablero = db.relationship('Tablero', backref='user')
    ganador = db.relationship('Ganador', backref='user')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Tablero(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    partida = db.Column(db.Integer, nullable=False)
    barco = db.Column(db.Integer, nullable=False)  # [1, 2, 3, 4]
    coordenada = db.Column(db.String(2), nullable=False)
    estado_barco = db.Column(db.String(1), nullable=False)  # A: afloat // S: sunken
    estado_partida = db.Column(db.String(1), nullable=False)  # O: open // C: closed

    def __init__(self, id_user, partida, barco, coordenada, estado_barco, estado_partida):
        self.id_user = id_user
        self.partida = partida
        self.barco = barco
        self.coordenada = coordenada
        self.estado_barco = estado_barco
        self.estado_partida = estado_partida


class Ganador(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    partida = db.Column(db.Integer, nullable=False)
    disparos = db.Column(db.Integer, nullable=False)

    def __init__(self, id_user, partida, disparos):
        self.id_user = id_user
        self.partida = partida
        self.disparos = disparos


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
