# Zestawienie Analizy Ruchu Sieciowego

### Adres MAC i IP serwera oraz numer portu TCP, do którego łączy się klient:
Ethernet II, Src: 7a:9b:67:94:85:b5 (7a:9b:67:94:85:b5), Dst: 52:34:7f:f0:12:d0 (52:34:7f:f0:12:d0)

---

### Treść wszystkich danych przesyłanych od klienta do serwera (tcp.pcap) w formacie ASCII:
8b2c2652b46b20cf0b984439ec3e54a6543a2cb3
x
Y100
Q0
M0
Z0
T87500
A0
F-1
W0
D0
G01
A3
G11
F0
W55000
Z1
X

---

### Zawartość najdłuższego pakietu przesłanego z serwera do klienta (HEX + ASCII dump):
0000   7a 9b 67 94 85 b5 52 34 7f f0 12 d0 08 00 45 00
0010   00 77 94 68 40 00 40 06 91 0c 0a 00 01 03 0a 00
0020   00 0a 1c cd b8 c4 71 b1 ae 40 bf 9c b3 9f 80 18
0030   01 fe 93 92 00 00 01 01 08 0a dd 15 f5 34 29 2f
0040   10 fa 4d 30 0a 54 36 34 30 30 30 2c 31 30 0a 5a
0050   30 0a 53 6d 2d 30 2e 37 35 2c 39 35 2c 2d 31 0a
0060   54 38 37 35 30 30 2c 31 30 0a 41 30 0a 57 30 0a
0070   44 30 0a 47 30 31 0a 53 6d 32 2e 38 32 2c 31 30
0080   30 2c 2d 31 0a

---

### Filtr na wszystkie ramki (frame), które zawierają w sobie string ASCII “ok” (case insensitive):
12  0.208390    10.0.1.3    10.0.0.10   TCP 109 7373 → 47300 [PSH, ACK] Seq=23 Ack=44 Win=65280 Len=43 TSval=3709203605 TSecr=690950314

---

### Filtr na pakiet IP z adresu źródłowego 10.0.1.3 i długości payloadu TCP o wartości 13:
21  0.408587    10.0.1.3    10.0.0.10   TCP 79  7373 → 47300 [PSH, ACK] Seq=141 Ack=82 Win=65280 Len=13 TSval=3709203828 TSecr=690950491

---

### Filtr na pakiety ARP Reply lub Ping Reply:
1620    13.969802081    Dell_0c:83:57   Fortinet_e4:71:ef   ARP 42  192.168.48.72 is at cc:96:e5:0c:83:57

---

### Payload protokołu DNS (bez niższych warstw) z zapytaniem kosmatka.pl w postaci zdekodowanego drzewa:
Domain Name System (response)
    Transaction ID: 0x4a59
    Flags: 0x8180 Standard query response, No error
    Questions: 1
    Answer RRs: 0
    Authority RRs: 1
    Additional RRs: 1
    Queries
        kosmatka.pl: type HTTPS, class IN
    Authoritative nameservers
        kosmatka.pl: type SOA, class IN, mname ns1.he.net
    Additional records
        <Root>: type OPT
    [Request In: 1765]
    [Time: 0.000907485 seconds]

---

### Zapytanie HTTP do serwera http://mm.kosmatka.pl/ oraz odpowiedź (tylko nagłówki) w formacie ASCII:
GET / HTTP/1.1
Host: mm.kosmatka.pl
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Connection: keep-alive

---

### Sposób zapisu obrazka http://mm.kosmatka.pl/favicon.png z Wireshark oraz jego treść w formacie base64:

iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=

---

### Polecenie tcpdump do nasłuchu pakietów na interfejsie karty sieciowej wraz z zapisem do pliku output.pcap:
sudo tcpdump -i eth0 -w output.pcap
