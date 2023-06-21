import network
import ubinascii
import machine
import time
from umqtt.simple import MQTTClient

# Configura los parámetros de tu red WiFi
SSID = "NOMBRE DE RED"
PASSWORD = "CONTRASEÑA DE RED"

# Configura los parámetros de tu broker MQTT
MQTT_BROKER = "192.168.1.66"
MQTT_PORT = 1883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
MQTT_TOPIC = "dispositivos_conectados"

def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando a la red WiFi....')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Conexión WiFi establecida:', sta_if.ifconfig())

def on_message(topic, message):
    pass  # No se realiza ninguna acción en este caso

def obtener_dispositivos_conectados():
    dispositivos = []
    sta_if = network.WLAN(network.STA_IF)
    for cliente in sta_if.scan():
        dispositivos.append(cliente[0].decode())
    return dispositivos

def publicar_dispositivos_conectados(dispositivos):
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    client.connect()
    client.publish(MQTT_TOPIC, ', '.join(dispositivos))
    client.disconnect()

def main():
    conectar_wifi()
    dispositivos_conectados = obtener_dispositivos_conectados()
    publicar_dispositivos_conectados(dispositivos_conectados)
    print('Lista de dispositivos conectados enviada por MQTT:', dispositivos_conectados)

if __name__ == '__main__':
    main()

