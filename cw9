# Utworzenie interfejsu mostka
sudo ip link add name br0 type bridge

# Dodanie fizycznych interfejsów do mostka
sudo ip link set eth0 master br0
sudo ip link set eth1 master br0



# Podniesienie interfejsów
sudo ip link set dev br0 up
sudo ip link set dev eth0 up
sudo ip link set dev eth1 up

sudo systemctl stop NetworkManager
sudo ip addr flush dev eth0
sudo ip addr flush dev eth1

# Pobranie adresu IP dla mostka (jeśli w sieci jest DHCP)
sudo dhcpcd br0


dnsmasq.conf

# Interfejs, na którym nasłuchuje DNS
interface=br0

# Ustawienie OpenDNS jako serwerów nadrzędnych (Upstream)
server=208.67.222.222
server=208.67.220.220

# Statyczne rekordy dla komputerów w pracowni
address=/k1.lan/192.168.48.71
address=/k2.lan/192.168.48.72
# ... dodaj resztę aż do k20 ...
address=/k20.lan/192.168.48.90

# Blokada domeny tiktok.com (zwraca 0.0.0.0)
address=/tiktok.com/0.0.0.0

# Włączenie logowania zapytań
log-queries
log-facility=/tmp/dns.log

# Wielkość cache (domyślnie 150, można zwiększyć)
cache-size=1000
