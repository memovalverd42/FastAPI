import sqlite3
from datetime import datetime

conexion = sqlite3.connect("data.sqlite")

conexion.execute("""INSERT INTO movies (title, year, director, created_at) VALUES (?, ?, ?, ?)""", ("Avatar 2", 2022, "James Cameron", datetime.now()))

conexion.commit()

conexion.close()