# TODO connect to emitter
import time
import tkinter

try:
    from .emitter import Client
except ImportError:
    from emitter import Client

def on_connect():
    print("CONNECTED")
def on_keygen(key):
    print("KEYGEN", key)

# secret key: aPr4nH0j7tzdi-d6nMToQOb95D9roTKg
if __name__=="__main__":
    emitter = Client()

    emitter.connect(host="127.0.0.1", port=8080, secure=False)
    emitter.on_connect = lambda: print("Connected\n\n")
    emitter.subscribe("NgFv_zrSsRznDwjdngZ77wwsP3NEzQeX",
                      "parking/occupancy/",
                      optional_handler=lambda m: print("Message received on handler for parking/occupancy/: " + m.as_string() + "\n\n"))

    emitter.loop_start()

    while True:
        time.sleep(1)

    # emitter.keygen("aPr4nH0j7tzdi-d6nMToQOb95D9roTKg", "channel/", "rwslpex")

    # emitter.on_connect = on_keygen
