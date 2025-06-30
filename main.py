import sqlite3
from fastapi import FastAPI, Depends
from pydantic import BaseModel


class Estudiante(BaseModel):
    nombre: str
    apellido: str


def connect():
    connection = sqlite3.connect("test.db")
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def creacionTabla():
    connect = sqlite3.connect("test.db")
    connect.execute(
        "CREATE TABLE IF NOT EXISTS estudiantes (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT)"
    )
    connect.commit()
    connect.close()


creacionTabla()

app = FastAPI()


@app.get("/")
def raiz(db: sqlite3.Connection = Depends(connect)):
    # obtener info de db
    res = db.execute("SELECT id, nombre, apellido FROM estudiantes").fetchall()
    return [dict(item) for item in res]
    # return {datos}


@app.post("/agregar_estudiante")
def postEstudiante(estudiante: Estudiante, db: sqlite3.Connection = Depends(connect)):
    if estudiante:
        db.execute(
            "INSERT INTO estudiantes (nombre, apellido) VALUES (?,?)",
            (estudiante.nombre, estudiante.apellido),
        )
        db.commit()
        return {"msg": "Estudiante agregado"}
    else:
        return {"msg": "Faltan datos"}


@app.put("/modificar_estudiante/{id}")
def putEstudiante(
    id: int, estudiante: Estudiante, db: sqlite3.Connection = Depends(connect)
):
    cursor = db.cursor()
    if estudiante:
        cursor.execute(
            "UPDATE estudiantes SET nombre = ?, apellido = ? WHERE id = ?",
            (estudiante.nombre, estudiante.apellido, id),
        )
        db.commit()
        return {"msg": "El estudiante fue modificado"}
    else:
        return {"msg": "Faltaron datos"}


@app.delete("/eliminar_estudiante/{id}")
def deleteEstudiante(id: int, db: sqlite3.Connection = Depends(connect)):
    db.execute("DELETE from estudiantes WHERE id = ?", (id,))
    db.commit()
    return {"msg": "Estudiante eliminado"}
