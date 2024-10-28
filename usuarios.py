from cryptography.fernet import Fernet
import sqlite3, login_vulnerable
from data_base import encrypt_data, decrypt_data, desencriptar

def login(username, password):
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        encrypted_password = result[0]
        if decrypt_data(encrypted_password) == password:
            print("Inicio de sesión exitoso.")
            login_vulnerable.registrar_log("Inicio de sesión", username, True)
            return True
        else:
            print("Contraseña incorrecta.")
            login_vulnerable.registrar_log("Intento de inicio de sesión fallido", username, False)
    else:
        print("Usuario no encontrado.")
        login_vulnerable.registrar_log("Intento de inicio de sesión fallido", username, False)

    conn.close()
    return False

def crear_tabla_usuarios():
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            admin BOOLEAN
        )
    ''')

    conn.commit()
    conn.close()


def register_usuario_admin(username, password, admin=False):
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()
    encrypted_password = encrypt_data(password)
    try:
        cursor.execute('''
               INSERT INTO users (username, password, admin) VALUES (?, ?, ?)
           ''', (username, encrypted_password, admin))
        conn.commit()
        print("Usuario registrado con éxito.")
        login_vulnerable.registrar_log("Se creo un nuevo usuaio", username, True)
    except sqlite3.IntegrityError:
        print("El nombre de usuario ya existe.")
        login_vulnerable.registrar_log("Intento de crear nuevo usuario", username, False)

    conn.close()



def acceso_admin():
    username = input("Ingrese su nombre de usuario de administrador: ")
    password = input("Ingrese su contraseña de administrador: ")

    if login(username, password):  # Verificar si el usuario es administrador
        print("Acceso de administrador concedido.")
        while True:
            action = input("¿Desea registrar un nuevo usuario? (s/n): ")
            if action.lower() == 's':
                new_username = input("Ingrese el nuevo nombre de usuario: ")
                new_password = input("Ingrese la nueva contraseña: ")
                register_usuario_admin(new_username, new_password, admin=False)
            elif action.lower() == 'n':
                break
            else:
                print("Opción inválida. Intente nuevamente.")
    else:
        print("Nombre de usuario o contraseña incorrectos.")


def acceso_simulado():
    while True:
        print("\nSeleccione una opción:")
        print("1. Acceso de administrador")
        print("2. Iniciar sesión")
        print("3. Salir")
        choice = input("Opción: ")

        if choice == '1':
            acceso_admin()
        elif choice == '2':
            username = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            if login(username, password):
                desencriptar()
        elif choice == '3':
            break
        else:
            print("Opción inválida, intente nuevamente.")

acceso_simulado()



