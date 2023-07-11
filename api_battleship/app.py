from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Proyecto-BattleShip-Codo-A-Codo'
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Arriolagabriel:Ga155954008@Arriolagabriel.mysql.pythonanywhere-services.com/Arriolagabriel$battleship'
    #'mysql+pymysql://root:mysql@localhost/battleship'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


from controladores import *


if __name__ == '__main__':
    app.run(debug=True)
