import time
import threading

class Cable:
    def __init__(self):
        self.valor = None
        signal_time = 0.01
        self.puertos_conectados = []  
        self.signal_time = signal_time

    def transmitir(self, valor):
        self.valor = valor
        time.sleep(self.signal_time)  # Esperar 10 ms antes de transmitir el siguiente bit
        self.valor = None
        
    def leer(self):
        return self.valor  # lectura del cable
        
    def conectar_puerto(self, puerto):
        self.puertos_conectados.append(puerto)

    def desconectar_puerto(self, puerto):
        if puerto in self.puertos_conectados:
            self.puertos_conectados.remove(puerto)
        
class Computadora:
    def __init__(self, nombre, archivo_salida):
        self.nombre = nombre
        self.puerto = nombre +"_1"
        self.cable = None
        self.archivo_salida = archivo_salida

    def conectar(self, cable):
        if self.cable is not None:
            print("Puerto  en uso...")
        else:
            self.cable = cable
            
    def desconectar(self):
        self.cable = None

    def transmitir(self, dato):
        for bit in dato:
            if self.cable.valor is None :

                hilo_transmitir = threading.Thread(target=self.cable.transmitir, args=(bit))
                hilo_leer = threading.Thread(target=self.cable.leer)
                
                hilo_transmitir.start()
                hilo_leer.start()
                
                lectura = self.cable.leer() # Realizar lectura 
                hilo_transmitir.join()
                hilo_leer.join()
                
                if lectura == bit:
                    with open(self.archivo_salida, 'a') as file:
                        file.write(f"{time.time() - start_time} {self.nombre} send {bit} ok\n")
                else:
                    with open(self.archivo_salida, 'a') as file:
                        file.write(f"{time.time() - start_time} {self.nombre} send {bit} collision\n")
            else:
                self.cable.transmitir(int(self.cable.valor) ^ int(bit))  # XOR entre el valor actual y el bit a transmitir
                lectura = self.cable.leer() # Realizar lectura después de transmitir
                if lectura == bit:
                    with open(self.archivo_salida, 'a') as file:
                        file.write(f"{time.time() - start_time} {self.nombre} send {bit} ok\n")
                else:
                    with open(self.archivo_salida, 'a') as file:
                        file.write(f"{time.time() - start_time} {self.nombre} send {bit} collision\n")

class Hub:
    def __init__(self, nombre, cantidad_puertos, archivo_salida):
        self.nombre = nombre
        self.archivo_salida = archivo_salida
        self.puertos = {}

    def conectar(self, puerto, cable):
        
        if puerto in self.puertos:
            print(f"Puerto {puerto} en uso...")
        else:
            self.puertos[puerto] = cable

    def desconectar(self, puerto):
        self.puertos[puerto] = None

    def transmitir(self, dato, puerto_uso = None):
        for bit in dato:
            
            if puerto_uso != None :
                with open(self.archivo_salida, 'a') as file:
                    file.write(f"{puerto_uso} recibe {bit} ok\n")
            
            for puerto in self.puertos:
                
                if puerto_uso == puerto:
                    continue
                
                cable = self.puertos[puerto]
                if cable is not None and cable.valor == None:
                    
                    hilo_transmitir = threading.Thread(target=cable.transmitir, args=(bit))
                    hilo_leer = threading.Thread(target=cable.leer)
                    
                    hilo_transmitir.start()
                    hilo_leer.start()
                    
                    lectura = cable.leer() # Realizar lectura 
                    hilo_transmitir.join()
                    hilo_leer.join()
                    
                    if lectura == bit:
                        with open(self.archivo_salida, 'a') as file:
                            file.write(f"{time.time() - start_time} {puerto} send {bit} ok\n")
                    else:
                        with open(self.archivo_salida, 'a') as file:
                            file.write(f"{time.time() - start_time} {puerto} send {bit} collision\n")
                            
                else:
                    self.cable.transmitir(int(self.cable.valor) ^ int(bit))  # XOR entre el valor actual y el bit a transmitir
                    lectura = self.cable.valor  # Realizar lectura después de transmitir
                    if lectura == bit:
                        with open(self.archivo_salida, 'a') as file:
                            file.write(f"{time.time() - start_time} {puerto} send {bit} ok\n")
                    else:
                        with open(self.archivo_salida, 'a') as file:
                            file.write(f"{time.time() - start_time} {puerto} send {bit} collision\n")

class Red:
    def __init__(self):
        self.cable = Cable()
        self.computadoras = {}
        self.hubs = {}
        self.puertos_conectados = {}

    def crear_computadora(self, nombre, archivo_salida,tiempo: int):
        time.sleep(int(tiempo))
        computadora = Computadora(nombre, archivo_salida)
        self.computadoras[nombre] = computadora

    def crear_hub(self, nombre, cantidad_puertos, archivo_salida,tiempo: int):
        time.sleep(int(tiempo))
        hub = Hub(nombre, cantidad_puertos, archivo_salida)
        self.hubs[nombre] = hub
         

    def conectar_dispositivos(self, puerto1, puerto2,tiempo:int):
        time.sleep(int(tiempo))
        
        self.cable = Cable()
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
            self.hubs[dispositivo1].conectar(puerto1,self.cable)
            self.hubs[dispositivo2].conectar(puerto2,self.cable)

    def enviar_datos(self, puerto_origen, puerto_destino, datos, tiempo):
        
        time.sleep(int(tiempo))
        dispositivo_origen,_ = puerto_origen.split('_')
        dispositivo_destino,_ = puerto_destino.split('_')
        
        if dispositivo_origen in self.computadoras and dispositivo_destino in self.computadoras:
            self.computadoras[dispositivo_origen].transmitir(datos)
            
                
        elif dispositivo_origen in self.computadoras and dispositivo_destino in self.hubs:
            #El dispositivo le envia datos al hub
            self.computadoras[dispositivo_origen].transmitir(datos)
            
            #El hub reenvia los datos a los dispositivos conectados
            self.hubs[dispositivo_destino].transmitir(datos,puerto_destino)
        
                                   
        elif dispositivo_origen in self.hubs :
            self.hubs[dispositivo_origen].transmitir(datos)
            
        else:
            pass

    def desconectar_puerto(self, puerto,tiempo):        
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
                    #self.crear_hub(nombre, int(cantidad_puertos), archivo_salida,tiempo)
                    
                    hilo_crear_hub = threading.Thread(target=self.crear_hub, args=(nombre, int(cantidad_puertos), archivo_salida,tiempo))
                    hilo_crear_hub.start()

                    
                elif instruccion.startswith('create host'):
                    _, _, nombre = instruccion.split()
                    archivo_salida = f"{nombre}.txt"
                    #self.crear_computadora(nombre, archivo_salida,tiempo)
                    hilo_crear_computadora = threading.Thread(target=self.crear_computadora, args=(nombre, archivo_salida,tiempo))
                    hilo_crear_computadora.start()
                    
               
                elif instruccion.startswith('connect'):
                    _, puerto1, puerto2 = instruccion.split()                        
                    #self.conectar_dispositivos(puerto1, puerto2)
                    hilo_conectar_dispositivos = threading.Thread(target=self.conectar_dispositivos, args=(puerto1, puerto2,tiempo))
                    hilo_conectar_dispositivos.start()
                    self.puertos_conectados[puerto1] = puerto2
                    self.puertos_conectados[puerto2] = puerto1
                    
               

                elif instruccion.startswith('send'):
                    _, dispositivo,puerto, datos = instruccion.split()
                    #self.enviar_datos(puerto,self.puertos_conectados[puerto], datos)
                    hilo_enviar_datos = threading.Thread(target=self.enviar_datos, args=(puerto,self.puertos_conectados[puerto], datos,tiempo))
                    hilo_enviar_datos.start()
                    
                elif instruccion.startswith('disconnect'):
                    _, puerto = instruccion.split()
                    #self.desconectar_puerto(puerto)
                    hilo_desconectar_puerto = threading.Thread(target=self.desconectar_puerto, args=(puerto,tiempo))
                    hilo_desconectar_puerto.start()
                
        hilo_crear_hub.join()
        hilo_crear_hub.join()
        hilo_conectar_dispositivos.join()
        hilo_enviar_datos.join()
        hilo_desconectar_puerto.join()

# Ejemplo de uso
red = Red()
start_time = time.time()# Variable global para almacenar el tiempo de inicio del programa
red.ejecutar_script('script1.txt')

elapsed_time = time.time() - start_time # Calcular el tiempo transcurrido desde el inicio del programa hasta el final
print("Tiempo transcurrido:", elapsed_time, "segundos")