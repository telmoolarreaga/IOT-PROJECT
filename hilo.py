import time
import threading
import RPi.GPIO as GPIO
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from influxdb_client import InfluxDBClient, Point

# --- CONFIGURACIÓN DE PINES ---
BUTTON_1_PIN = 25
BUTTON_2_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- SENSORES ---
light_1 = GroveLightSensor(0)
light_2 = GroveLightSensor(2)
ultra_1 = GroveUltrasonicRanger(16)
ultra_2 = GroveUltrasonicRanger(18)

# --- INFLUXDB ---
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"
token = "iKM4DU0L0H5XYJB3NNj_WRALv2VjS1f6P4caRzeUzFMDaVjwBu5WgNB4oVCEeTIwIc6uAobuF9BMID_4JdmLIQ=="
org = "deusto"
bucket = "mesas"
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api()

# --- FUNCIONES ---
def estado_mesa(luz, distancia, boton):
    activos = sum([luz, distancia, boton])
    return activos >= 2

def leer_sensores(mesa_id, luz_sensor, ultra_sensor, boton_pin):
    while True:
        luz_activo = luz_sensor.light > 600
        dist = ultra_sensor.get_distance()
        distancia_activo = 30 <= dist <= 80
        boton_activo = GPIO.input(boton_pin) == 0

        ocupada = estado_mesa(luz_activo, distancia_activo, boton_activo)
        print(f"[Mesa {mesa_id}] Ocupada: {ocupada}")

        # --- Enviar a InfluxDB ---
        point = Point("ocupacion_mesa").tag("mesa", str(mesa_id)).field("estado", ocupada)
        write_api.write(bucket=bucket, record=point)

        time.sleep(1)  # leer cada 1 segundo

# --- CREAR HILOS ---
hilos = [
    threading.Thread(target=leer_sensores, args=(1, light_1, ultra_1, BUTTON_1_PIN), daemon=True),
    threading.Thread(target=leer_sensores, args=(2, light_2, ultra_2, BUTTON_2_PIN), daemon=True)
]

for h in hilos:
    h.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado")
finally:
    GPIO.cleanup()
