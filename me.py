import Adafruit_DHT
import paho.mqtt.client as mqtt
import time

# Sensor and GPIO setup
SENSOR = Adafruit_DHT.DHT22  # Use DHT11 for DHT11 sensor
PIN = 4  # GPIO pin connected to the sensor data pin

# MQTT setup
MQTT_BROKER = "test.mosquitto.org"  # Public broker for testing (replace with your broker)
MQTT_PORT = 1883  # Default MQTT port
MQTT_TOPIC = "home/sensors/temperature_humidity"

# MQTT client setup
client = mqtt.Client("RaspberryPi")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def read_and_send_data():
    while True:
        # Read temperature and humidity
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
        if humidity is not None and temperature is not None:
            # Format and print data
            data = {
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2)
            }
            print(f"Publishing data: {data}")

            # Publish data to MQTT broker
            client.publish(MQTT_TOPIC, str(data))
        else:
            print("Failed to get reading. Trying again...")

        # Wait before sending the next data point
        time.sleep(5)

if __name__ == "__main__":
    try:
        read_and_send_data()
    except KeyboardInterrupt:
        print("\nExiting...")
        client.disconnect()
