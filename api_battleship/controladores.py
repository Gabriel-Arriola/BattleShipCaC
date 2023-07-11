from flask import Flask, jsonify, session, request
from app import app, ma, db, bcrypt
from modelos import *
from tablero import crea_tablero_usuario


class TableroSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_user', 'partida', 'barco', 'coordenada', 'estado_barco', 'estado_partida')


class GanadoresSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'partida', 'disparos')


tablero_schema = TableroSchema(many=True)
ganadores_schema = GanadoresSchema(many=True)


@app.route('/')
def hola():  # put application's code here
    return jsonify({"response": "HOLAAA!!!"})


@app.route('/ping')
def ping_pong():  # put application's code here
    return jsonify({"response": "PONG!!!"})


@app.route("/register", methods=["POST"])
def signup():
    name = request.get_json()["params"]["username"] or request.json["username"]
    email = request.get_json()["params"]["email"] or request.json["email"]
    password = request.get_json()["params"]["password"] or request.json["password"]

    user_name_exists = User.query.filter_by(name=name).first() is not None
    user_email_exists = User.query.filter_by(email=email).first() is not None

    if user_name_exists:
        return jsonify({"error": "Nombre de usuario ya registrado"}), 409

    if user_email_exists:
        return jsonify({"error": "Email ya registrado"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.id

    return jsonify({
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    })


@app.route("/login", methods=["POST"])
def login_user():
    #my_json = request.get_json()
    #print("3", my_json["params"]["username"])

    name = request.get_json()["params"]["username"] or request.json["username"]
    password = request.get_json()["params"]["password"] or request.json["uspassworder_id"]
    user = User.query.filter_by(name=name).first()
    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    session["user_id"] = user.id

    return jsonify({
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    })

@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop('user_id', None)

    return jsonify({"session": "LOGGED OUT"})


@app.route("/tablero/usuario", methods=["POST"])
def crear_tablero_usuario():

    session_id = request.get_json()["params"]["user_id"] or request.json["user_id"]
    tablero_usuario = crea_tablero_usuario(10, 10)
    max_partida = db.session.execute(db.text('select max(partida) from tablero'))
    sig_partida = [row[0] for row in max_partida][0]
    if sig_partida is None:
        sig_partida = 1
    else:
        sig_partida = sig_partida + 1

    for barco in range(1, 5):
        for f in range(10):
            for c in range(10):
                if tablero_usuario[f, c] == str(barco):
                    new_tablero = Tablero(id_user=session_id, partida=sig_partida, barco=barco, coordenada=str(f)+str(c), estado_barco='A', estado_partida='O')
                    db.session.add(new_tablero)
                    db.session.commit()
    tabla_barcos = tablero_schema.dump(Tablero.query.filter_by(partida=sig_partida))
    return jsonify({"partida": new_tablero.partida,
                    "user_id": session_id,
                    "barcos": "20",
                    "tabla": tabla_barcos})


@app.route("/tablero/", methods=["GET"])
def ver_tablero_usuario():
    #my_json = request.args.keys()
    partida = request.args.get("partida") or request.json["partida"]
    tabla_barcos = tablero_schema.dump(Tablero.query.filter_by(partida=partida))
    return jsonify({"partida": partida,
                    "tabla_barcos": tabla_barcos})


@app.route("/ranking/", methods=["GET"])
def ver_ranking():
    sql = "SELECT user.name, user.email, ganador.partida, ganador.disparos FROM ganador, user WHERE ganador.id_user = user.id ORDER BY ganador.disparos"
    res = db.session.execute(db.text(sql))
    ranking = ganadores_schema.dump(res)
    return jsonify({"ranking": ranking})


@app.route("/tablero/borrar", methods=["DELETE"])
def eliminar_tablero():
    partida = request.json["partida"]
    Tablero.query.filter_by(partida=partida).delete()
    db.session.commit()
    return jsonify({"Resultado": "OK"})


@app.route("/tablero/disparo", methods=["PUT"])
def disparo():
    #my_json = request.get_json()
   # print(my_json)

    cant_barcos = int(request.get_json()["params"]["barcos"]) or int(request.json["barcos"])
    disparos = int(request.get_json()["params"]["disparos"]) or int(request.json["disparos"])
    id_user = request.get_json()["params"]["user_id"] or request.json["user_id"]
    partida = request.get_json()["params"]["partida"] or request.json["partida"]
    coordenada = request.get_json()["params"]["coordenada"] or request.json["coordenada"]
    barco = db.session.execute(db.text(f'select * from tablero where id_user = {id_user} and partida = {partida}'))
    barco_id = []
    barco_coord = []
    barco_estado = []
    for row in barco:
        barco_id.append(row.id)
        barco_coord.append(row.coordenada)
        barco_estado.append(row.estado_barco)

    if "A" in barco_estado:
        disparos = disparos + 1
        if coordenada in barco_coord and barco_estado[barco_coord.index(coordenada)] == "A":
            golpe = "hit"
            tablero = Tablero.query.get(barco_id[barco_coord.index(coordenada)])
            tablero.estado_barco = "S"
            db.session.commit()
            cant_barcos = cant_barcos - 1
            if cant_barcos >= 1:
                estado_juego = "Playing"
            else:
                estado_juego = "Finished"
                db.session.execute(db.text(f'update tablero set estado_partida = "C" where partida = {partida}'))
                db.session.commit()
                new_ganador = Ganador(id_user=id_user, partida=partida, disparos=disparos)
                db.session.add(new_ganador)
                db.session.commit()
        elif coordenada in barco_coord and barco_estado[barco_coord.index(coordenada)] == "S":
            golpe = "hitted"
            estado_juego = "Playing"
        else:
            golpe = "miss"
            estado_juego = "Playing"
    else:
        golpe = "Finished"
        estado_juego = "Finished"
    return jsonify({"user_id": id_user,
                    "golpe": golpe,
                    "estado": estado_juego,
                    "barcos": cant_barcos,
                    "disparos": disparos})
