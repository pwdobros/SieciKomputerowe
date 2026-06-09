# Odpowiedzi do zadania (cw10)

**Pytanie:** Sprawdź, co się stanie gdy zmienisz adres bindowania z `INADDR_ANY` (0.0.0.0) na `INADDR_LOOPBACK` (127.0.0.1). Czy osoba pracująca na komputerze obok może podłączyć się do Twojego serwera?

**Odpowiedź:** 
Gdy zmienimy adres bindowania w wywołaniu funkcji `bind` z `INADDR_ANY` (reprezentującego adres `0.0.0.0`, czyli wszystkie dostępne interfejsy sieciowe komputera) na `INADDR_LOOPBACK` (adres `127.0.0.1`), serwer zacznie nasłuchiwać połączeń wyłącznie na lokalnym interfejsie pętli zwrotnej (loopback).

W rezultacie **osoba pracująca na komputerze obok nie będzie mogła podłączyć się do naszego serwera**. Zmiana ta sprawia, że do serwera mają dostęp wyłącznie procesy uruchomione na tej samej maszynie. Połączenia przychodzące z sieci lokalnej (np. z innej maszyny w sieci LAN) będą odrzucane, ponieważ pakiety te będą kierowane na adres IP zewnętrznego interfejsu (np. z rodziny 192.168.x.x), na którym serwer już nie nasłuchuje.
