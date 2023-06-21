import nmap
import time
import json
import socket
import paho.mqtt.client as mqtt

#Configuración de MQTT
mqtt_broker = "192.168.1.66"
mqtt_port = 1883
mqtt_topic = "dispositivos"


def obtener_nombre_dispositivo(ip):
    try:
        nombre = socket.getfqdn(ip)
        return nombre
    except socket.error:
        return ""


def escanear_red():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')
    dispositivos = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            ip = nm[host]['addresses']['ipv4']
            mac = nm[host]['addresses']['mac']
            nombre = obtener_nombre_dispositivo(ip)
            dispositivos.append({"ip": ip, "mac": mac, "nombre": nombre})
    return dispositivos


def publicar_dispositivos(dispositivos):
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port)
    client.publish(mqtt_topic, json.dumps(dispositivos))
    client.disconnect()


while True:
    try:
        dispositivos = escanear_red()
        publicar_dispositivos(dispositivos)
        print("Lista de dispositivos publicada en MQTT.")
    except nmap.PortScannerError as e:
        print("Error al escanear la red:", e)
    except mqtt.MQTTException as e:
        print("Error al publicar en MQTT:", e)
    
    time.sleep(300)  # Espera 3 minutos antes de volver a escanear la red
