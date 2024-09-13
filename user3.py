
import socket, threading
import json, sys
import random as Random

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = 'user' + str(Random.randint(1, 10000))

a = 'localhost'
b = 8685
stop_event = threading.Event()

# Establecer un tiempo de espera en el socket
user.settimeout(1)  # Tiempo de espera en segundos para no bloquear indefinidamente

def sendMessage():
    while not stop_event.is_set():
        try:
            msg = input('>>> ')
            message = {
                "user": username,
                "msg": msg,
                "to": "all"
            }
            json_message = json.dumps(message)
            if msg == 'exit':
                print('[*] Conexion cerrada, adios :)')
                stop_event.set()  # Señalamos que se debe detener
                user.close()
                break
            user.send(str(json_message).encode('utf-8'))
        except:
            print('[#] Error al enviar mensaje')
            stop_event.set()  # En caso de error, también detenemos todo
            user.close()
            break
    print('[*] Cerrando bucle de envío...')

def receive():
    while not stop_event.is_set():
        try:
            peticion = user.recv(1024).decode('utf-8')
            message = json.loads(peticion)
            if message['user'] != username:
                print('\n%s: %s' % (message["user"], message['msg']))
        except socket.timeout:
            continue  # Ignoramos el timeout para revisar el estado del evento y continuar
        except:
            print('[#] Error en la conexión')
            stop_event.set()  # Detenemos en caso de error
            user.close()
            break
    print('[*] Cerrando hilo de recepción...')

# Creando el hilo para recepción
recept = threading.Thread(target=receive)

def handler():
    recept.start()  # Inicia el hilo de recepción
    sendMessage()   # Comienza el proceso de enviar mensajes

# Intentamos conectar con el servidor
try:
    user.connect(('localhost', 8685))
except:
    print('[#] Error al conectar')
    sys.exit()

try:
    handler()
except:
    print('[*] Error en el cliente')
finally:
    stop_event.set()  # En cualquier caso, se asegura que el evento se activa
    recept.join()  # Esperamos a que el hilo de recepción termine
    user.close()  # Cerramos el socket si no lo está
    print('[*] Conexión cerrada')
