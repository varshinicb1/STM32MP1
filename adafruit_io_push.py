from Adafruit_IO import Client, Feed, RequestError

ADAFRUIT_IO_USERNAME = "varshinicb99"
ADAFRUIT_IO_KEY = "aio_dAoB13F0U7Z6wZfP98P6N9zcn8RY"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

for feed_name in ["temperature", "humidity", "gas", "anomaly"]:
    try:
        aio.feeds(feed_name)
    except RequestError:
        try:
            aio.create_feed(Feed(name=feed_name))
        except Exception as e:
            print(f"Adafruit IO: Could not create feed '{feed_name}': {e}")

def push_to_adafruit(temp, hum, gas, anomaly):
    try:
        aio.send('temperature', temp)
        aio.send('humidity', hum)
        aio.send('gas', gas)
        aio.send('anomaly', int(anomaly))
    except Exception as e:
        print(f"Adafruit IO push failed: {e}")
