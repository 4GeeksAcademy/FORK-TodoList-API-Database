from flask_sqlalchemy import SQLAlchemy
from enum import Enum

# Esta vez usaremos sql Alchemy + Flask 
# para simplificar la creacion de tablas (bd.xxxxxx en vez de importar Integer, Text, Column ETC)
# Fijate que cosas se tienen que importar
db = SQLAlchemy()

# Esto es un num y asi se usa
# Proposito? Una tabla con datos que van a ser estaticos basicamente
class Genders(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'other'

class User(db.Model):
    # Omitimos el tablename 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False, unique=True)
    # Enum
    gender = db.Column(db.Enum(Genders), nullable=False)

    todos = db.relationship('Todos', back_populates='user', cascade="all, delete") # Cascade En caso de querer borrar usuario y sus tareas a la vez Usa la Cascade...

    # Recuerda que jsonify acepta diccionarios, no objetos asi que convierte a objeto con ayuda de los self
    def serializable(self):
        return {
            "id": self.id,
            "name": self.name,
            # Ordenado desde el Frontend Opcion 1
            "todos" : sorted(
                [item.serializable for item in self.todos], key=lambda todo : todo["id"] 
            )

            # Ordenado desde el Frontend Opcion 2
            # "todos" : sorted(
            #     list(map(lambda item : item.serializable), self.todos), key=lambda todo : todo["id"]
            # )

            # Sin ordenar desde el frotend
            # "todos": list(map(lambda unit: unit.serializable(), self.todos) )
        }

    def serializable_users(self):
        return {
            "id" : self.id,
            "name" : self.name
        }



                          
class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(99), nullable=True)
    is_done = db.Column(db.Boolean(), nullable=True)


    # Necesario para pasar a json la tabla todos desde user (Relacion uno a muchos) 
    def serializable(self):
        return {
            "id": self.id,
            "label": self.label,
            "is_done": self.is_done
        }

    # Recuerda que solo va a conectar la tarea todos con el user solo si es compatible con este ID !
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='todos')
    


# Comandos para correr el proyecto-

# pipenv shell 
# pipenv run start 

# Ahora necesitamos este ORM y pasarselo a la base de datos real con los comandos... 

# pipenv shell 
# pipenv run init 
# Y me crea la carpeta migrations
 
# Luego corre el comando: pipenv run migrate
# Hasta aqui prepara las migraciones 

# Aun falta el comando y ahora sigue entrar manualmente a la basedatos y crear la database...
# Comando: psql -h localhost -U gitpod postgres 

# Luego creas la base de datos: create database todos;

# Ahora si, vuelve a darle: pipenv run migrate y listo ahora 
# se prepara por segunda vez pero ya con la base de data creada + su nombre 

# Ahora por ultimo para guardar las tablas del ORM en la base de datos: \
# pipen run upgrade

# Ahora vuelve a entrar: psql -h localhost -U gitpod postgres 
# y posicionate en la base de datos: \c example
# Ahora para ver las tablas de esa base de datos: \dt 

# Luego si quieres ver todo el contenido, como los registros: select * from <nombre de basedatos>















# Y SE BORRO...

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }