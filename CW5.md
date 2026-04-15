### Zadanie 1: Wykaz interfejsów sieciowych i ich statusów
Wyświetlenie uproszczonej listy interfejsów w celu weryfikacji ich stanu (UP/DOWN).

**Polecenie:**
ip -br link

**Wynik:**
```text
lo                UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
enp0s31f6         UP             cc:96:e5:0c:83:57 <BROADCAST,MULTICAST,UP,LOWER_UP> 
virbr0            DOWN           52:54:00:f8:3b:b7 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-b577f0de8e19   DOWN           e6:67:08:fd:96:c7 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-c2c76b48eb27   DOWN           0e:10:0e:ee:ba:39 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-c2d58d5db3bf   DOWN           0a:c1:0d:29:86:5e <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-df67ba73b67b   DOWN           fa:46:af:b9:95:79 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-e270fb02a15f   DOWN           1e:9e:11:a0:92:d0 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-5cc7d5c0a356   UP             be:45:e4:68:53:85 <BROADCAST,MULTICAST,UP,LOWER_UP> 
docker0           UP             0a:e8:eb:a7:52:b0 <BROADCAST,MULTICAST,UP,LOWER_UP> 
br-813593f6b092   DOWN           f2:ac:b1:c1:4a:2e <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-c058572e79d6   UP             aa:41:96:f5:c1:aa <BROADCAST,MULTICAST,UP,LOWER_UP> 
br-d50221502901   DOWN           ce:f6:58:ef:32:72 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-5c4ff0e61303   DOWN           9e:54:a7:cf:c9:79 <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-9b273425498f   DOWN           da:ef:b9:69:17:4a <NO-CARRIER,BROADCAST,MULTICAST,UP> 
br-a01eef478d1f   UP             ce:c6:df:93:f3:c8 <BROADCAST,MULTICAST,UP,LOWER_UP> 
veth17d5bde@if2   UP             f2:cb:d3:9d:5b:29 <BROADCAST,MULTICAST,UP,LOWER_UP> 
vethfb81bc2@if2   UP             1e:62:da:52:c8:7e <BROADCAST,MULTICAST,UP,LOWER_UP> 
vethf60d007@if2   UP             1e:58:28:6d:20:7d <BROADCAST,MULTICAST,UP,LOWER_UP> 
veth913961f@if2   UP             7e:d8:e6:e3:3c:1c <BROADCAST,MULTICAST,UP,LOWER_UP> 
veth246ea98@if2   UP             e6:a2:6e:c8:c6:26 <BROADCAST,MULTICAST,UP,LOWER_UP> 
vethe17a9a5@if2   UP             1a:87:72:69:30:d5 <BROADCAST,MULTICAST,UP,LOWER_UP> 
veth7b7d429@if2   UP             ba:ff:96:46:38:b3 <BROADCAST,MULTICAST,UP,LOWER_UP> 
```
---

### Zadanie 2: Adres fizyczny (MAC) routera domyślnego
Identyfikacja adresu MAC urządzenia pełniącego rolę bramy sieciowej.

**Polecenie:**
arp -a

**Wynik:**
```text
_gateway (192.168.48.1) at d4:76:a0:e4:71:ef [ether] on enp0s31f6
(Wpis dla bramy domyślnej zidentyfikowany po etykiecie _gateway)
```
---

### Zadanie 3: Procedura zmiany adresu MAC
Czynność mająca na celu zmianę identyfikatora sprzętowego karty sieciowej.

**Polecenie:**
```text
sudo ip link set dev eth0 down
sudo ip link set dev eth0 address 00:11:22:33:44:55
sudo ip link set dev eth0 up
```
**Status weryfikacji:**
nie zmienilem

---

### Zadanie 4: Skanowanie dostępności hostów w podsieci (Ping Sweep)
Wykrywanie aktywnych maszyn w lokalnym segmencie sieciowym.

**Polecenie:**
nmap -sn 192.168.48.255/24

**Wynik:**
```text
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-25 11:54 CET
Nmap scan report for 192.168.48.2
Host is up (0.0021s latency).
Nmap scan report for user-Precision-3460 (192.168.48.72)
Host is up (0.000065s latency).
Nmap scan report for 192.168.48.77
Host is up (0.0014s latency).
Nmap scan report for 192.168.48.79
Host is up (0.0011s latency).
Nmap scan report for 192.168.48.81
Host is up (0.0012s latency).
Nmap scan report for 192.168.48.84
Host is up (0.0012s latency).
Nmap scan report for 192.168.48.85
Host is up (0.0011s latency).
Nmap scan report for 192.168.48.87
Host is up (0.00045s latency).
Nmap scan report for 192.168.48.90
Host is up (0.00054s latency).
Nmap done: 256 IP addresses (9 hosts up) scanned in 2.32 seconds
```
---

### Zadanie 5: Skanowanie podsieci pod kątem usługi SSH (port 22)
Wyszukiwanie maszyn z otwartym portem komunikacyjnym 22.

**Polecenie:**
nmap -p 22 --open 192.168.48.0/24

**Wynik:**
```text
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-25 11:56 CET
Nmap scan report for 192.168.48.2
Host is up (0.00093s latency).
PORT   STATE SERVICE
22/tcp open  ssh
... (wyniki powtarzalne dla hostów .72, .77, .79, .81, .84, .85, .87, .90)
Nmap done: 256 IP addresses (9 hosts up) scanned in 2.32 seconds
```
---

### Zadanie 6: Analiza wszystkich portów interfejsu loopback
Sprawdzenie lokalnie uruchomionych usług na interfejsie zwrotnym.

**Polecenie:**
nmap -p- 127.0.0.1

**Wynik:**
```text
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-03-25 11:51 CET
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000039s latency).
Not shown: 65525 closed tcp ports (conn-refused)
PORT      STATE SERVICE
22/tcp    open  ssh
631/tcp   open  ipp
3000/tcp  open  ppp
3308/tcp  open  tns-server
5040/tcp  open  unknown
5432/tcp  open  postgresql
5433/tcp  open  pyrrho
8082/tcp  open  blackice-alerts
11434/tcp open  unknown
27017/tcp open  mongod
```
---

### Zadanie 7: Identyfikacja portów, procesów i nazw programów
Szczegółowa lista nasłuchujących połączeń TCP/UDP.

**Polecenie:**
sudo netstat -tulnp

**Wynik (wybrane wpisy):**
```text
Proto Recv-Q Send-Q Local Address           State       PID/Program name    
tcp        0      0 0.0.0.0:3000            LISTEN      4809/docker-proxy   
tcp        0      0 127.0.0.1:5432          LISTEN      2596/postgres       
tcp        0      0 127.0.0.53:53           LISTEN      1175/systemd-resolv 
tcp        0      0 0.0.0.0:22              LISTEN      1/init              
tcp        0      0 127.0.0.1:11434         LISTEN      3039/ollama         
tcp        0      0 127.0.0.1:27017         LISTEN      3552/mongod         
```
---

### Zadanie 8: Wyświetlenie trasy domyślnej
Weryfikacja głównej ścieżki wyjścia pakietów z systemu.

**Polecenie:**
ip route | grep default

**Wynik:**
default via 192.168.48.1 dev enp0s31f6 proto dhcp src 192.168.48.72 metric 100 

---

### Zadanie 9: Śledzenie trasy pakietów do serwera zewnętrznego
Analiza przeskoków (hops) na drodze do domeny kosmatka.pl.

**Polecenie:**
traceroute kosmatka.pl

**Wynik:**
traceroute to kosmatka.pl (217.28.148.190), 30 hops max
 1  * * *
 ...
 30  * * *
(Brak odpowiedzi sugeruje filtrowanie ruchu diagnostycznego przez zaporę sieciową).

---

### Zadanie 10: Adresacja serwerów DNS w systemie
Sprawdzenie pliku konfiguracyjnego resolvera.

**Polecenie:**
cat /etc/resolv.conf

**Wynik:**
```text
nameserver 127.0.0.53
options edns0 trust-ad
search .
```
---

### Zadanie 11: Statyczne wpisy w pliku hosts
Weryfikacja lokalnej bazy mapowania nazw na adresy IP.

**Polecenie:**
cat /etc/hosts

**Wynik:**
```text
127.0.0.1 localhost
127.0.1.1 user-Precision-3460
::1     ip6-localhost ip6-loopback
```
---

### Zadanie 12: Zapytanie o rekordy MX przez zewnętrzny serwer DNS
Wykorzystanie serwera 8.8.8.8 do odpytania o rekordy pocztowe domeny.

**Polecenie:**
dig MX kosmatka.pl @8.8.8.8 +short

**Wynik:**
```text
10 mx2.privateemail.com.
10 mx1.privateemail.com.
```
---

### Zadanie 13: Sprawdzenie adresu IPv6 dla domeny google.pl
Zapytanie o rekord AAAA.

**Polecenie:**
dig AAAA google.pl +short

**Wynik:**
2a00:1450:4025:807::5e

---

### Zadanie 14: Informacje o domenie kosmatka.pl (WHOIS)
Sprawdzenie dat ważności i rejestracji domeny.

**Polecenie:**
whois kosmatka.pl

**Wynik:**
```text
created:                        2022.12.02 12:27:10
last modified:                  2022.12.02 12:33:53
renewal date:                   2032.12.02 12:27:10
```
---

### Zadanie 15: Lokalizacja listy usuniętych domen .pl
Wskazanie adresu URL oficjalnego rejestru NASK.

**Adres URL:** https://dns.pl/lista_domen_usunietych
