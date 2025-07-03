from Adafruit_IO import Client, Feed, RequestError

# Use your provided credentials
ADAFRUIT_IO_USERNAME = "varshinicb99"
ADAFRUIT_IO_KEY = "aio_batV15elzJ6knI6nnfHjJ0Mlfe1w"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Ensure feeds exist (create if missing)
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
