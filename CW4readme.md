### Krok 1: Zdefiniowanie głównej sieci

Wybrałem prywatną pulę **`10.0.0.0/22`**. 
Co to oznacza w praktyce?
* Maska `/22` zostawia nam 10 bitów na hosty (32 - 22 = 10).
* Ilość wszystkich adresów w tej sieci to 2^10 = 1024.
* Zakres adresów to od `10.0.0.0` do `10.0.3.255`.

---

### Krok 2: Obliczenie rzeczywistego zapotrzebowania

Zgodnie z poleceniem, nie mogłem przydzielić adresów "na styk". Musiałem zastosować wzór: `(obecne zapotrzebowanie * 1.5) + 1 host na router`. 

Na przykład dla **Zarządu (25 urządzeń)**:
* 25 * 1.5 = 37.5 (ponieważ nie można mieć połowy adresu, musimy to zaokrąglić do 38)
* 38 + 1 (router) = **39** wymaganych adresów.

Tę samą matematykę zastosowałem dla każdego działu.

---

### Krok 3: Sortowanie od największej podsieci do najmniejszej

To absolutnie **kluczowa zasada**. Gdybyśmy zaczęli od małych podsieci, pocięlibyśmy przestrzeń adresową na małe kawałki ("szwajcarski ser") i później duża podsieć by się nie zmieściła w jednym spójnym bloku. 

Ułożyłem działy malejąco po wymaganym zapotrzebowaniu (z uwzględnieniem over-provisioningu):
1. **Serwery:** 301 
2. **Stacje robocze:** 151
3. **IoT:** 91
4. **Zarząd:** 39
5. **Goście:** 24

---

### Krok 4: Dobór odpowiednich masek

W sieciach komputery zawsze zajmują bloki o wielkości potęgi liczby 2 (2, 4, 8, 16, 32, 64, 128, 256, 512 itd.). Musiałem znaleźć najmniejszą potęgę dwójki, która pomieści nasze zapotrzebowanie + 2 obowiązkowe adresy (jeden na adres sieci, jeden na adres broadcast).

* **Serwery (potrzeba 301):** Blok 256 to za mało. Następny to **512** (czyli 2^9). Skoro hosty zajmują 9 bitów, maska to 32 - 9 = **`/23`**.
* **Stacje (potrzeba 151):** Blok 128 to za mało. Następny to **256** (2^8). Maska to 32 - 8 = **`/24`**.
* **IoT (potrzeba 91):** Blok 64 to za mało. Następny to **128** (2^7). Maska to 32 - 7 = **`/25`**.
* **Zarząd (potrzeba 39):** Blok 32 to za mało. Następny to **64** (2^6). Maska to 32 - 6 = **`/26`**.
* **Goście (potrzeba 24):** Zmieści się w bloku **32** (2^5). Maska to 32 - 5 = **`/27`**.

---

### Krok 5: Odcinanie kawałków

Zaczynamy od początku naszej głównej sieci (`10.0.0.0`) i dodajemy do niej kolejne wyliczone bloki:

1. **Serwery (blok 512 adresów):** Zaczynamy od `10.0.0.0`. Dodanie 512 adresów oznacza zajęcie całej podsieci `10.0.0.x` (256) i `10.0.1.x` (256). 
   * Podsieć kończy się na broadcaście `10.0.1.255`.
2. **Stacje robocze (blok 256 adresów):**
   Zaczynamy dokładnie tam, gdzie skończyliśmy, czyli od następnego wolnego adresu: `10.0.2.0`. Dodajemy 256, więc zajmujemy całe `10.0.2.x`.
   * Broadcast to `10.0.2.255`.
3. **IoT (blok 128 adresów):**
   Następny wolny to `10.0.3.0`. Dodajemy 128. 
   * Broadcast to `10.0.3.127`.
4. **Zarząd (blok 64 adresy):**
   Następny wolny to `10.0.3.128`. Dodajemy 64. 
   * Broadcast to `10.0.3.191`.
5. **Goście (blok 32 adresy):**
   Następny wolny to `10.0.3.192`. Dodajemy 32. 
   * Broadcast to `10.0.3.223`.

---

### Krok 6: Wyliczenie niewykorzystanych adresów

Nasza podsieć dla Gości skończyła się na adresie `10.0.3.223`. Następny wolny adres to `10.0.3.224`. 
Nasza wielka główna sieć `/22` kończyła się na `10.0.3.255`.

Odejmując od siebie te wartości (lub licząc w potęgach), łatwo zauważyć, że został nam dokładnie jeden wolny blok 32 adresów (od `.224` do `.255`), co odpowiada jednej pustej sieci z maską **`/27`**. Została ona oznaczona jako *niewykorzystana*.
