import sqlite3
import data_base

def crear_tabla_logs():
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            action TEXT,
            username TEXT,
            success BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

def crear_tabla_usuarios():
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

def registrar_log(action, username, success):
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (action, username, success)
        VALUES (?, ?, ?)
    ''', (action, username, success))
    conn.commit()
    conn.close()




def login_vulnerable(username, password):
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()

    # Consulta vulnerable a inyección SQL
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    result = cursor.fetchone()

    if result:
        print("Inicio de sesión exitoso.")
        registrar_log("Inicio de sesión", username, True)
        return True
    else:
        print("Usuario o contraseña incorrectos.")
        registrar_log("Intento de inicio de sesión fallido", username, False)

    conn.close()
    return False




def acceso_simulado():
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    if login_vulnerable(username, password):
        ver_registros = input("¿Deseas ver los registros de pacientes? (s/n): ")
        if ver_registros.lower() == 's':
            pass
            data_base.desencriptar()

#testuser' OR '1'='1


# acceso_simulado()

