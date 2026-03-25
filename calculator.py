import sys

def ip_na_liczbe(ip_str):
    """Zamienia adres IP w formacie tekstowym na 32-bitową liczbę całkowitą."""
    oktety = [int(o) for o in ip_str.split('.')]
    return (oktety[0] << 24) + (oktety[1] << 16) + (oktety[2] << 8) + oktety[3]

def liczba_na_ip(liczba_ip):
    """Zamienia liczbę całkowitą z powrotem na format tekstowy IP (A.B.C.D)."""
    return ".".join(str((liczba_ip >> i) & 0xFF) for i in (24, 16, 8, 0))

def formatuj_binarnie(liczba_ip):
    """Zwraca postać binarną adresu IP z kropkami między oktetami."""
    binarny = f"{liczba_ip:032b}"
    return ".".join([binarny[i:i+8] for i in range(0, 32, 8)])

def kalkulator_cidr(wejscie):
    try:
        # Rozdzielenie adresu od maski
        adres_str, maska_str = wejscie.split('/')
        prefix = int(maska_str)

        if not (0 <= prefix <= 32):
            raise ValueError("Maska musi być z zakresu 0-32.")

        # Podstawowe obliczenia bitowe
        ip_int = ip_na_liczbe(adres_str)
        maska_bitowa = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        
        adres_sieci = ip_int & maska_bitowa
        adres_broadcast = adres_sieci | (~maska_bitowa & 0xFFFFFFFF)
        
        # Obliczanie liczby hostów i zakresu
        if prefix == 32:
            liczba_hostow = 1
            pierwszy_host = ostatni_host = adres_sieci
        elif prefix == 31:
            liczba_hostow = 2
            pierwszy_host = adres_sieci
            ostatni_host = adres_broadcast
        else:
            liczba_hostow = (adres_broadcast - adres_sieci) - 1
            pierwszy_host = adres_sieci + 1
            ostatni_host = adres_broadcast - 1

        # Wyświetlanie wyników
        print(f"--- Wyniki dla {wejscie} ---")
        
        dane = [
            ("Adres sieci", adres_sieci),
            (f"Maska (/{prefix})", maska_bitowa),
            ("Pierwszy host", pierwszy_host),
            ("Ostatni host", ostatni_host),
            ("Broadcast", adres_broadcast),
        ]

        for opis, wartosc in dane:
            print(f"{opis}:")
            print(f"  Dziesiętnie: {liczba_na_ip(wartosc)}")
            print(f"  Binarnie:    {formatuj_binarnie(wartosc)}")
        
        print(f"\nLiczba użytecznych hostów: {liczba_hostow}")

    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python kalkulator.py <adres_ip/maska>")
        print("Przykład: python kalkulator.py 192.168.1.10/24")
    else:
        kalkulator_cidr(sys.argv[1])
