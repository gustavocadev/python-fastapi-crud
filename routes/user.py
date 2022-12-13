from fastapi import APIRouter, Response
from config.db import connection as conn
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT
# from cryptography.fernet import Fernet

user = APIRouter()


@user.get("/users")
def get_users():
    all_users = conn.execute(users.select()).fetchall()
    return {
        "users": all_users,
    }


@user.post("/users", response_model=User)
def create_user(user: User):
    # Creo una un diccionario con los datos del usuario
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": user.password
    }
    # Guardar usuario en la base de datos
    result = conn.execute(users.insert().values(new_user))

    # Retornar el usuario creado
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get("/users/{id}", response_model=User)
def get_user(id: str):
    # Obtener un solo usuario de la base de datos
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete("/users/{id}")
def delete_user(id: str):
    # Eliminar usuario de la base de datos
    result = conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/users/{id}")
def update_user(id: str, user: User):
    # print("HII!1111111-----")

    # userFound = conn.execute(users.select().where(users.c.id == id)).first()
    # print("HII!2222222222222-----")
    data = {
        "name": user.name,
        "email": user.email,
        "password": user.password
    }
    # if user.password == None:
    #     data["password"] = userFound.password

    # if user.name == None:
    #     data["name"] = userFound.name

    # if user.email == None:
    #     data["email"] = userFound.email
    # print("HII!")
    # print(data)
    conn.execute(users.update().values(
        name=data['name'],
        email=data["email"],
        password=data["password"]
    ).where(users.c.id == id))
    return {
        "message": "User updated successfully",
        "user": conn.execute(users.select().where(users.c.id == id)).first()
    }
