import socket
import threading
import json

wht = '\033[00m'
red = '\033[31m'
grn = '\033[32m'
ylw = '\033[33m'

# Datos del servidor
ip = '127.0.0.1'
puerto = 8685
max_conexiones = 5
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((ip, puerto))
servidor.listen(max_conexiones)

users = []  # Lista de usuarios conectados

def broadcast_message(message):
    """Envía un mensaje a todos los usuarios conectados."""
    json_message = json.dumps(message)
    for user in users:
        try:
            user[0].send(json_message.encode('utf-8'))
        except:
            user[0].close()
            remove_user(user)  # Remover usuarios que no están disponibles

def remove_user(user):
    """Elimina a un usuario de la lista cuando se desconecta."""
    if user in users:
        users.remove(user)
        print(f"[*] Usuario {user[1]}:{user[2]} desconectado y eliminado.")

def conexiones(socket_cliente, index):
    """Maneja la conexión de un cliente y recibe mensajes."""
    username = f'{red}[{grn}{users[index][1]}{red}:{grn}{str(users[index][2])}{red}]{wht}'
    try:
        while True:
            peticion = socket_cliente.recv(1024).decode('utf-8')
            if not peticion:
                break  # Si no se recibe nada, significa que el cliente se desconectó
            message = json.loads(peticion)
            if message["msg"]:
                print(f'\n{message["user"]}{ylw}:{wht} {message["msg"]}')
                if(len(users[index])==3):
                    users[index].append(message["user"])
                else:
                    print("username ya reg ", users[index][3])
                if message["to"] == 'all':
                    broadcast_message(message)
            if message["msg"] == 'exit':
                print(f'[*] {message["user"]} se ha desconectado.')
                break
    except:
        print(f'[!] Error con el usuario {users[index][1]}:{users[index][2]}')
    finally:
        # Cerramos el socket del cliente y lo eliminamos de la lista
        socket_cliente.close()
        remove_user(users[index])

def sendMessage():
    """Permite enviar mensajes desde el servidor a todos los clientes."""
    while True:
        msg = input('>>> ')
        if msg == '@':
            print('ok')
        else:
            message = {
                "user": "server",
                "msg": msg,
                "to": "all"
            }
            broadcast_message(message)

def handler():
    """Maneja la aceptación de nuevas conexiones de clientes."""
    print(f"[*] Esperando conexiones en {ip}:{puerto}")
    while True:
        user_socket, direccion = servidor.accept()
        print(f"[*] Conexión establecida con {direccion[0]}:{direccion[1]}")
        users.append([user_socket, direccion[0], direccion[1]])

        # Enviar mensaje de bienvenida al nuevo cliente
        message = {
            "user": "server",
            "msg": f"[*] Conexión establecida con {direccion[0]}:{direccion[1]}",
            "to": "all"
        }
        user_socket.send(json.dumps(message).encode('utf-8'))

        # Iniciar un hilo para manejar la conexión de cada cliente
        client_thread = threading.Thread(target=conexiones, args=(user_socket, len(users)-1))
        client_thread.start()

# Ejecutar el servidor
try:

    admin_thread = threading.Thread(target=sendMessage)
    admin_thread.start()
    handler()
except KeyboardInterrupt:
    print('\n[*] Cerrando servidor...')
    servidor.close()
