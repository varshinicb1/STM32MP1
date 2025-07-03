from Adafruit_IO import Client, Feed, RequestError

ADAFRUIT_IO_USERNAME = "varshinicb99"
ADAFRUIT_IO_KEY = "aio_XXYH15mddEj83HFOTw6UZuue7zEF"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Ensure feeds exist
for feed_name in ["temperature", "humidity", "gas", "anomaly"]:
    try:
        aio.feeds(feed_name)
    except RequestError:
        aio.create_feed(Feed(name=feed_name))

def push_to_adafruit(temp, hum, gas, anomaly):
    aio.send('temperature', temp)
    aio.send('humidity', hum)
    aio.send('gas', gas)
    aio.send('anomaly', int(anomaly))
