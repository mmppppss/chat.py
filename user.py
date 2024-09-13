import socket, threading
import json, sys
import random as Random

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = 'user'+str(Random.randint(1, 10000))
'''
a=input("Direccion: ")
b=int(input("Puerto: "))
'''

a='localhost'
b=8685
stop_event = threading.Event()



def sendMessage():
    while not stop_event.is_set():
        try:
            msg=input('>>> ')
            message = {
                "user": username,
                "msg": msg,
                "to": "all"
            }
            json_message = json.dumps(message)
            if(msg=='exit'):
                print('[*] Conexion cerrada, adios :)')
                stop_event.set()
                recept.join()
                user.close()
                break
            user.send(str(json_message).encode('utf-8'))
        except:
            print('[#] Error')
            user.close() 
            stop_event.set()
            break
    print('[*] Cerrando true...')
        
def receive():
    while not stop_event.is_set():
        try:
            peticion = user.recv(1024).decode('utf-8')
            message = json.loads(peticion)
            if(message['user'] != username):
                print('\n%s: %s' %(message["user"], message['msg']))
        except:
            print('[#] Error al Conectar')  
            stop_event.set()
            user.close()
            exit()
    print('[*] Cerrando thread...')

recept = threading.Thread(target=receive)
def handler():
    recept.start()
    sendMessage()

try:
    user.connect(('localhost',8685))
except:    
    print('[#] Error al Conectar')
    exit()
try:
    handler()
except:
    print('[*] Error')
    user.close()
    sys.exit()
    exit()
finally:
    stop_event.set()  # En cualquier caso, se asegura que el evento se activa
    recept.join()  # Esperamos a que el hilo de recepción termine
    user.close()  # Cerramos el socket si no lo está
    print('[*] Conexión cerrada')

