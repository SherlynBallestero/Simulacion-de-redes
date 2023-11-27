import time
import threading
import random

class CableDuplex:
    def __init__(self):
        self.valor_tx = None
        self.valor_rx = None
        self.signal_time = 0.01
        self.puertos_conectados = []

    def transmitir(self, valor):
        self.valor_tx = valor
        time.sleep(self.signal_time)  # Esperar 10 ms antes de transmitir el siguiente bit
        self.valor_tx = None

    def leer(self):
        return self.valor_rx  # lectura del cable

    def conectar_puerto(self, puerto):
        self.puertos_conectados.append(puerto)

    def desconectar_puerto(self, puerto):
        if puerto in self.puertos_conectados:
            self.puertos_conectados.remove(puerto)
class Trama_CapaRed:
    def __init__(self,mac_destino,mac_origen,data):
        self.mac_destino=mac_destino
        self.mac_origen=mac_origen
        self.data=data
class Trama_paqueteIP:
        def __init__(self,ip_destino,ip_origen,cant_Byets,data,ttl=0,protocolo=0):
            self.ip_destino=ip_destino
            self.mac_origen=ip_origen
            self.data=data
            self.cant_Byets=cant_Byets
            self.ttl=ttl
            self.protocolo=protocolo    
        
class Computadora: 
    def __init__(self, nombre, archivo_salida,mac):
        self.nombre = nombre
        self.puerto = nombre + "_1"
        self.cable = None
        self.archivo_salida = archivo_salida
        self.direccion_ip = None
        self.direccion_mascara = None
        self.Subred=None
        if len(mac) != 16:
            print("Error")
        else:
            self.direccion_mac = mac
    def transmite_PaqueteIp(self,ip_destino,data,cant_enviar,ttl=0,protocolo=0):
        trama=Trama_paqueteIP(ip_destino,self.direccion_ip,cant_enviar,ttl,protocolo)
        trama_respuesta=self.Subred.recive_paqueteIp()
        pass        
    def transmitir_cRed(self,ip_destino):
        mac_destino=self.Subred.broadcast
        mac_origen=self.direccion_mac
        data=["ARPQ",ip_destino]
        tramaEspecial=Trama_CapaRed(mac_destino=mac_destino,mac_origen=mac_origen,data=data)
        trama_respuesta=self.Subred.ReciveTrama(tramaEspecial)
        if trama_respuesta is not None:
            print(f"Se envio el mensaje correctamente, la mac destino es {trama_respuesta.mac_origen}")
        
         
                
    def asignar_IP(self,ip,mascara):
        if self.ip is None:
            self.direccion_ip = ip
            self.direccion_mascara=mascara
        else:
            pass      

    def conectar(self, cable):
        if self.cable is not None:
            print("Puerto en uso...")
        else:
            self.cable = cable

    def desconectar(self):
        self.cable = None
    
    def transmitir(self, datos):
            while self.cable.valor_tx is not None:  # Esperar a que el medio esté libre
                pass
            
            hilo_transmitir = threading.Thread(target=self.cable.transmitir, args=(datos))
            hilo_leer = threading.Thread(target=self.cable.leer)
            hilo_transmitir.start()
            hilo_transmitir.join()        

            with open(self.archivo_salida, 'a') as file:
                file.write(f"{time.time() - start_time} {self.nombre} envía {datos} ok\n")
#comprobar que funcione
class Subred:
    def __init__(self,direccion_red,mascara,broadcast):
        self.Computadoras={}#diccionary ip-computadora
        self.direccion_red=direccion_red
        self.mascara=mascara
        self.broadcast=broadcast
        self.cantidadMaximaHosts=self.CantidadMaxima_Hosts()
    def CantidadMaxima_Hosts(self):
        index=0
        mascara=self.mascara.split('.')
        direccion_res=self.direccion_red.split(".")
        
        while(True):
            if mascara[index]==250:
                index=index+1
                if index==4:
                    print('error con el tamanno de la mascara')
            else:
                break
        pivote=4-(index+1)
        cantHosts=((255-direccion_res[index])*pivote)-2
        return cantHosts                    
    
    
    def recive_paqueteIp(self,trama:Trama_paqueteIP):
        pass
    def Recive_trama(self,trama:Trama_CapaRed):
        ip=trama.data[1]
        for key in self.Coputadoras:
              if key==ip:
                  #la computadora responde
                  mac_origen=self.Computadoras[key].direccion_mac
                  mac_destino=trama.mac_origen
                  data=["ARPR",trama.data[1]]
                  trama_respuesta=Trama_CapaRed(mac_destino=mac_destino,mac_origen=mac_origen,data=data)
                  return trama_respuesta
               
    def Agregar_computadoras(self,computadora: Computadora,ip):
        #verificar que el ip coincida ver como controlar eso
        self.Computadoras[ip]=computadora
        computadora.asignar_IP(ip,self.masacara)
    
    #idea: retornar algua direccion random dentro del rango ip de la subred
    #pero que no haya sido asignada antes
    def calcular_direccinDisp(self):
        mascara=self.mascara.split(',')
        direccion=self.direccion_red.split('.')
        direccionAnswer=[]
        broadcast=self.broadcast.split('.')
        while(True):
            for j in range(len(self.mascara)):
                if mascara[j]==255:
                    direccionAnswer[j]=direccion[j]
                    continue
                else:
                    direccionAnswer[j]=random.next(direccion[j]+1,broadcast[j])
            if direccionAnswer.join('.') in self.Computadoras.keys():
                direccionAnswer=[]
            else:
                break
        return direccionAnswer                
            
    def Conectar_computadora(self,Computadora: Computadora):
        #primero ver que esa computadora no este conectada a otra subred
        if len(Computadora)<self.cantidadMaximaHosts:
            if Computadora.direccion_ip !=None:
                return False
            else:
                ip=self.calcular_direccinDisp()
                self.Agregar_computadoras(Computadora,ip)
                return True
        else: 
            return False    
        
       
    def desconectar_Computadora(self,computadora: Computadora):
        ip=computadora.direccion_ip
        if ip !=None:
            computadora.direccion_ip=None
            del self.Computadoras[ip]
        
       
        
        
        
                
            

class Trama:
    def __init__(self, mac_destino, mac_origen, tamano, extra, datos):
        self.mac_destino = mac_destino
        self.mac_origen = mac_origen
        self.tamano = tamano
        self.extra = extra
        self.datos = datos[:self.tamano_datos]  # Acotamos los datos al tamaño especificado

class Switch:
    def __init__(self, nombre, cantidad_puertos, archivo_salida):
        self.nombre = nombre
        self.archivo_salida = archivo_salida
        self.puertos = {key: None for key in range(cantidad_puertos)}
        self.tabla_direcciones = {key: None for key in range(cantidad_puertos)}

    def conectar(self, puerto, cable):
        if puerto in self.puertos:
            print(f"Puerto {puerto} en uso...")
        else:
            self.puertos[puerto] = cable

    def desconectar(self, puerto):
        self.puertos[puerto] = None

    def aprender_direccion_mac(self, puerto, direccion_mac):
        self.tabla_direcciones[puerto] = direccion_mac

    def transmitir(self, trama:Trama):

        dispositivo_origen = trama.mac_origen
        dispositivo_destino = trama.mac_destino

        if dispositivo_origen in self.tabla_direcciones and dispositivo_destino in self.tabla_direcciones:
            dispositivo_origen
            
        while self.cable.valor_tx is not None:  # Esperar a que el medio esté libre
                pass
            
        cable = self.puertos[puerto]
        if cable is not None and cable.valor_tx is None:
            hilo_transmitir = threading.Thread(target=cable.transmitir, args=(trama))
            hilo_leer = threading.Thread(target=cable.leer)
            hilo_transmitir.start()
            
            hilo_transmitir.join()
            hilo_leer.join()
            
            with open(self.archivo_salida, 'a') as file:
                file.write(f"{time.time() - start_time} {puerto} envía {datos} ok\n")
            

class Red:
    def __init__(self):
        self.cable = CableDuplex()
        self.computadoras = {}
        self.hubs = {}
        self.switch = None
        self.puertos_conectados = {}

    def crear_computadora(self, host, archivo_salida,mac, tiempo: int):
        time.sleep(int(tiempo))
        nombre,_ = host.split('_')
        computadora = Computadora(nombre, archivo_salida,mac)
        self.computadoras[nombre] = computadora

    def crear_hub(self, nombre, cantidad_puertos, archivo_salida, tiempo: int):
        time.sleep(int(tiempo))
        hub = Hub(nombre, cantidad_puertos, archivo_salida)
        self.hubs[nombre] = hub

    def crear_switch(self, nombre, cantidad_puertos, archivo_salida, tiempo: int):
        time.sleep(int(tiempo))
        switch = Switch(nombre, cantidad_puertos, archivo_salida)
        self.switch = switch

    def conectar_dispositivos(self, puerto1, puerto2, tiempo: int):
        time.sleep(int(tiempo))
        self.cable = CableDuplex()
        self.cable.conectar_puerto(puerto1)
        self.cable.conectar_puerto(puerto2)
        dispositivo1, _ = puerto1.split('_')
        dispositivo2, _ = puerto2.split('_')
        

        if dispositivo1 in self.computadoras and dispositivo2 in self.computadoras:
            self.computadoras[dispositivo1].conectar(self.cable)
            self.computadoras[dispositivo2].conectar(self.cable)
        elif dispositivo1 in self.computadoras and dispositivo2 in self.hubs:
            self.computadoras[dispositivo1].conectar(self.cable)
            self.hubs[dispositivo2].conectar(puerto1, self.cable)
        elif dispositivo1 in self.hubs and dispositivo2 in self.computadoras:
            self.computadoras[dispositivo2].conectar(self.cable)
            self.hubs[dispositivo1].conectar(puerto1, self.cable)
        elif dispositivo1 in self.hubs and dispositivo2 in self.hubs:
            self.hubs[dispositivo1].conectar(puerto1, self.cable)
            self.hubs[dispositivo2].conectar(puerto2, self.cable)
        elif dispositivo1 in self.computadoras and dispositivo2 == self.switch.nombre:
            self.switch.conectar(puerto2,self.cable)
            self.computadoras[dispositivo1].conectar( self.cable)

    def enviar_datos(self, puerto_origen, puerto_destino, datos, tiempo):
        time.sleep(int(tiempo))
        dispositivo_origen, _ = puerto_origen.split('_')
        dispositivo_destino, _ = puerto_destino.split('_')

        if dispositivo_origen in self.computadoras and dispositivo_destino in self.computadoras:
            self.computadoras[dispositivo_origen].transmitir(datos)
        elif dispositivo_origen in self.computadoras and dispositivo_destino in self.hubs:
            self.computadoras[dispositivo_origen].transmitir(datos)
            self.hubs[dispositivo_destino].transmitir(datos, puerto_destino)
        elif dispositivo_origen in self.hubs:
            self.hubs[dispositivo_origen].transmitir(datos)
        elif dispositivo_origen in self.computadoras and dispositivo_destino == self.switch.nombre:
            self.computadoras[dispositivo_origen].transmitir(datos)
        else:
            pass

    def desconectar_puerto(self, puerto, tiempo):        
        time.sleep(int(tiempo))
        dispositivo, _ = puerto.split('_')

        if dispositivo in self.computadoras:
            self.computadoras[dispositivo].desconectar()
        elif dispositivo in self.hubs:
            self.hubs[dispositivo].desconectar(puerto)

    def ejecutar_script(self, archivo):
        self.cable.__init__()  # Inicializar el cable
        with open(archivo, 'r') as file:
            for linea in file:
                tiempo, *instruccion = linea.strip().split()
                instruccion = ' '.join(instruccion)
                
                if instruccion.startswith('create hub'):
                    _, _, nombre, cantidad_puertos = instruccion.split()
                    archivo_salida = f"{nombre}.txt"
                    hilo_crear_hub = threading.Thread(target=self.crear_hub, args=(nombre, int(cantidad_puertos), archivo_salida, tiempo))
                    hilo_crear_hub.start()
                    
                #elif instruccion.startswith('create host'):
                #    _, _, nombre = instruccion.split()
                #    archivo_salida = f"{nombre}.txt"
                #    hilo_crear_computadora = threading.Thread(target=self.crear_computadora, args=(nombre, archivo_salida, tiempo))
                #    hilo_crear_computadora.start()
                    
                elif instruccion.startswith('create switch'):
                    _, _, nombre, cantidad_puertos = instruccion.split()
                    archivo_salida = f"{nombre}.txt"
                    self.crear_switch(nombre, int(cantidad_puertos), archivo_salida, tiempo)
                    #hilo_crear_switch = threading.Thread(target=self.crear_switch, args=(nombre, int(cantidad_puertos), archivo_salida, tiempo))
                    #hilo_crear_switch.start()
                    
                elif instruccion.startswith('connect'):
                    _, puerto1, puerto2 = instruccion.split()
                    
                    hilo_conectar_dispositivos = threading.Thread(target=self.conectar_dispositivos, args=(puerto1, puerto2, tiempo))
                    #hilo_conectar_dispositivos.start()
                    self.conectar_dispositivos(puerto1, puerto2, tiempo)
                    self.puertos_conectados[puerto1] = puerto2
                    self.puertos_conectados[puerto2] = puerto1
                    
                elif instruccion.startswith('mac'):
                    _, host, direccion_mac = instruccion.split()
                    archivo_salida = f"{nombre}.txt"
                    self.crear_computadora(host, archivo_salida,direccion_mac,0)
                    #    hilo_crear_computadora = threading.Thread(target=self.crear_computadora, args=(host, archivo_salida,direccion_mac,0))
                    #    hilo_crear_computadora.start()
                    self.switch.aprender_direccion_mac(host, direccion_mac)
                    
                elif instruccion.startswith('send_frame'):
                    _, host, mac_destino, datos = instruccion.split()
                    trama = Trama(mac_destino, self.computadoras[host].direccion_mac, len(datos) // 2, "00", datos)
                    self.enviar_datos(host + "_1", self.puertos_conectados[host + "_1"], trama, tiempo)
                    
  
                elif instruccion.startswith('disconnect'):
                    _, puerto = instruccion.split()
                    hilo_desconectar_puerto = threading.Thread(target=self.desconectar_puerto, args=(puerto, tiempo))
                    hilo_desconectar_puerto.start()

        hilo_crear_hub.join()
        hilo_crear_computadora.join()
        hilo_crear_switch.join()
        hilo_conectar_dispositivos.join()
        hilo_desconectar_puerto.join()



# Ejemplo de uso
red = Red()
start_time = time.time()  # Variable global para almacenar el tiempo de inicio del programa
red.ejecutar_script('script.txt')
elapsed_time = time.time() - start_time  # Calcular el tiempo transcurrido desde el inicio del programa hasta el final
print("Tiempo transcurrido:", elapsed_time, "segundos")
