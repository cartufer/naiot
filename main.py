import wifimgr
import _thread
import time
def testThread():
  while True:
    import network
    import slimDNS
    sta_if = network.WLAN(network.STA_IF)
    local_addr = sta_if.ifconfig()[0]
    server = slimDNS.SlimDNSServer(local_addr, "micropython")
    print("starting slimDNS server")
    server.run_forever()


wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK, wifi connected")
#import gc
#gc.collect()
#gc.enable()
#def testThread():#server.run_forever()

_thread.start_new_thread(testThread, ())
#for i in range(1):
_thread.start_new_thread(testThread, ())
print("mdns setup complete")
