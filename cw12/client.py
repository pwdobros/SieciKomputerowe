import socket
import threading
import json
import sys

def receive_messages(client_socket):
    """Wątek odczytujący dane z socketa w tle."""
    try:
        reader = client_socket.makefile('r', encoding='utf-8')
        for line in reader:
            if not line:
                break
            
            try:
                data = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            msg_type = data.get('type')
            
            if msg_type == 'info':
                print(f"\r[SYSTEM] {data.get('message')}\n> ", end="")
            elif msg_type == 'user_list':
                print(f"\r[SYSTEM] {data.get('message')}")
                print(f"[OBECNI UŻYTKOWNICY] {', '.join(data.get('users', []))}\n> ", end="")
            elif msg_type == 'status':
                status = data.get('status')
                user = data.get('username')
                print(f"\r[STATUS] Użytkownik {user} zmienił status na: {status}.\n> ", end="")
            elif msg_type == 'broadcast':
                sender = data.get('sender')
                msg = data.get('message')
                print(f"\r[GLOBAL] <{sender}>: {msg}\n> ", end="")
            elif msg_type == 'private':
                sender = data.get('sender')
                msg = data.get('message')
                print(f"\r[PRYWATNA od {sender}]: {msg}\n> ", end="")
    except Exception as e:
        print(f"\n[BŁĄD] Utracono połączenie: {e}")
    finally:
        print("\n[ROZŁĄCZONO] Naciśnij Enter, aby zakończyć.")
        client_socket.close()

def main():
    if len(sys.argv) < 3:
        print("Użycie: python3 client.py <adres_ip_serwera> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Połączono z serwerem {host}:{port}")
    except Exception as e:
        print(f"Nie udało się połączyć: {e}")
        sys.exit(1)

    # Uruchomienie wątku odbierającego wiadomości (wątek 1: odczyt danych)
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    receive_thread.start()

    print("--- Dostępne komendy ---")
    print("/register <login> <haslo>")
    print("/login <login> <haslo>")
    print("/all <wiadomosc>")
    print("/msg <login_odbiorcy> <wiadomosc>")
    print("/exit")
    print("------------------------")

    # Wątek 2 (główny): pobieranie poleceń od użytkownika
    try:
        while True:
            user_input = input("> ")
            if not user_input.strip():
                continue

            parts = user_input.strip().split(' ', 2)
            command = parts[0].lower()

            if command == '/exit':
                break
            elif command == '/register':
                if len(parts) == 3:
                    msg = {"type": "register", "username": parts[1], "password": parts[2]}
                    client_socket.sendall((json.dumps(msg) + "\n").encode('utf-8'))
                else:
                    print("Użycie: /register <login> <haslo>")
            elif command == '/login':
                if len(parts) == 3:
                    msg = {"type": "login", "username": parts[1], "password": parts[2]}
                    client_socket.sendall((json.dumps(msg) + "\n").encode('utf-8'))
                else:
                    print("Użycie: /login <login> <haslo>")
            elif command == '/all':
                if len(parts) >= 2:
                    message = " ".join(parts[1:])
                    msg = {"type": "broadcast", "message": message}
                    client_socket.sendall((json.dumps(msg) + "\n").encode('utf-8'))
                else:
                    print("Użycie: /all <wiadomosc>")
            elif command == '/msg':
                if len(parts) == 3:
                    msg = {"type": "private", "recipient": parts[1], "message": parts[2]}
                    client_socket.sendall((json.dumps(msg) + "\n").encode('utf-8'))
                else:
                    print("Użycie: /msg <login_odbiorcy> <wiadomosc>")
            else:
                print("Nieznana komenda.")
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
