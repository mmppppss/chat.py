
import socket
import threading
import json
import sys
import random as Random

class ChatClient:
    def __init__(self, host='100.25.250.69', port=8685):
        self.username = 'user' + str(Random.randint(1, 10000))
        self.host = host
        self.port = port
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user.settimeout(1)  # Tiempo de espera para evitar bloqueos en recv()
        self.stop_event = threading.Event()
        self.recept_thread = threading.Thread(target=self.receive)

    def connect(self):
        """Conectar al servidor de chat."""
        try:
            self.user.connect((self.host, self.port))
            print(f'[*] Conectado como {self.username}')
        except Exception as e:
            print(f'[!] Error al conectar: {e}')
            sys.exit()

    def send_message(self):
        """Manejo del envío de mensajes del usuario."""
        while not self.stop_event.is_set():
            try:
                msg = input('>>> ')
                message = {
                    "user": self.username,
                    "msg": msg,
                    "to": "all"
                }
                json_message = json.dumps(message)
                if msg == 'exit':
                    print('[*] Conexion cerrada, adios :)')
                    self.stop_event.set()
                    self.user.close()
                    break
                self.user.send(json_message.encode('utf-8'))
            except Exception as e:
                print(f'[!] Error al enviar mensaje: {e}')
                self.stop_event.set()
                self.user.close()
                break
        print('[*] Cerrando bucle de envío...')

    def receive(self):
        """Manejo de la recepción de mensajes."""
        while not self.stop_event.is_set():
            try:
                peticion = self.user.recv(1024).decode('utf-8')
                if not peticion:  # Conexión cerrada por el servidor
                    print('[!] Conexión cerrada por el servidor.')
                    self.stop_event.set()
                    break
                message = json.loads(peticion)
                if message['user'] != self.username:
                    print(f'\n{message["user"]}: {message["msg"]}')
            except socket.timeout:
                continue  # Continuamos el bucle en caso de timeout
            except Exception as e:
                print(f'[!] Error en la recepción de mensajes: {e}')
                self.stop_event.set()
                self.user.close()
                break
        print('[*] Cerrando hilo de recepción...')

    def start(self):
        """Iniciar el cliente y los hilos de comunicación."""
        self.recept_thread.start()
        self.send_message()
        self.recept_thread.join()  # Esperamos que el hilo de recepción termine
        self.user.close()
        print('[*] Conexión cerrada')

# Ejecución del cliente
if __name__ == "__main__":
    client = ChatClient()
    try:
        client.connect()
        client.start()
    except KeyboardInterrupt:
        print('[*] Interrupción manual, cerrando cliente...')
        client.stop_event.set()
        client.recept_thread.join()
        client.user.close()
