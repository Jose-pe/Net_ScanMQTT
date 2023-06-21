
import network
from umqtt.simple import MQTTClient

def connect_to_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando a la red WiFi...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('Conexión establecida')
    print('Dirección IP:', sta_if.ifconfig()[0])

def get_connected_devices():
    sta_if = network.WLAN(network.STA_IF)
    connected_devices = sta_if.scan()
    return [device[0].decode() for device in connected_devices]


MQTT_BROKER = '192.168.1.66'
MQTT_PORT = 1883
MQTT_TOPIC = 'dispositivos_conectados'

SSID = 'NOMBRE DE RED'
PASSWORD = 'PASSWORD DE LA RED'

connect_to_wifi(SSID, PASSWORD)
devices = get_connected_devices()
device_list = ", ".join(devices)
print('Dispositivos conectados:', device_list)


client = MQTTClient('micropython_client', MQTT_BROKER, port=MQTT_PORT)
client.connect()
client.publish(MQTT_TOPIC, device_list)

client.disconnect()
print('Información enviada por MQTT')
