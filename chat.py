import socket, threading
import json
#ux
wht='\033[00m'
blk='\033[30m'
red='\033[31m'
grn='\033[32m'
ylw='\033[33m'
blu='\033[34m'
pnk='\033[35m'
#os.system('python -m http.server 8685')


#format json message to array

def conexiones(socket_cliente,index):
    username=red+'['+grn+users[index][1] +red+':'+grn+ str(users[index][2])+red+']'+wht
    while True:
        peticion =(socket_cliente.recv(1024)).decode('utf-8')
        message =json.loads(peticion)
        if(""!=message["msg"]):
            print ('\n%s%s:%s %s' %(message["user"], ylw, wht, message['msg']))
            if(message["to"]=='all'):
                json_message = json.dumps(message)
                for user in users:
                    user[0].send(str(json_message).encode('utf-8'))
        if(message["msg"]=='exit'):
            socket_cliente.close()
            print('[*] Conexion Cerrada, adios :)')
            break
def sendMessage():
    while True:
        if(input('>>>')=='@'):
            print('ok')
        else:
            for user in users:
                user[0].send(input('>>>').encode('utf-8'))

ip = '127.0.0.1'
puerto = 8685
max_conexiones = 5 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


servidor.bind((ip, puerto))
servidor.listen(max_conexiones)
users=[]


def  handler():
    print ("[*] Esperando conexiones en %s:%d" % (ip, puerto))
    while True:
          user, direccion = servidor.accept()
          print("[*] Conexion establecida con %s:%d" % (direccion[0] , direccion[1]))
          users.append([user,direccion[0],direccion[1]])
          message = {
              "user": "server",
              "msg": "[*] Conexion establecida con %s:%d" % (direccion[0] , direccion[1]),
              "to": "all"
          }

          json_message = json.dumps(message)
          user.send(str(json_message).encode('utf-8'))
          new=threading.Thread(target=conexiones, args=(user,len(users)-1))

          adm=threading.Thread(target=sendMessage)
          new.start()
          #adm.start()

try:
    handler()
except KeyboardInterrupt:
    print('\n[*] Cerrando servidor...')
    servidor.close()
