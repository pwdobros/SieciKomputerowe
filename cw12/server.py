import socket
import threading
import json
import sys

HOST = '0.0.0.0'
PORT = 12345

# Struktury danych w pamięci RAM
registered_users = {} # username -> password
online_users = {}     # username -> obiekt socket
lock = threading.Lock()

def broadcast_message(message_dict, exclude_username=None):
    """Przesyła wiadomość do wszystkich aktualnie połączonych użytkowników."""
    with lock:
        msg_str = json.dumps(message_dict) + "\n"
        for user, sock in online_users.items():
            if user != exclude_username:
                try:
                    sock.sendall(msg_str.encode('utf-8'))
                except Exception:
                    pass

def handle_client(client_socket, addr):
    print(f"[NOWE POŁĄCZENIE] Klient {addr} podłączył się.")
    current_username = None

    try:
        # Odczyt linia po linii (upraszcza przetwarzanie JSONa)
        reader = client_socket.makefile('r', encoding='utf-8')
        for line in reader:
            if not line:
                break
            
            try:
                data = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            msg_type = data.get('type')

            if msg_type == 'register':
                username = data.get('username')
                password = data.get('password')
                
                with lock: # Zabezpieczenie dostępu muteksem
                    if username in registered_users:
                        resp = {"type": "info", "success": False, "message": "Użytkownik o takiej nazwie już istnieje."}
                    else:
                        registered_users[username] = password
                        resp = {"type": "info", "success": True, "message": "Zarejestrowano pomyślnie. Możesz się teraz zalogować."}
                
                client_socket.sendall((json.dumps(resp) + "\n").encode('utf-8'))

            elif msg_type == 'login':
                username = data.get('username')
                password = data.get('password')
                
                with lock: # Zabezpieczenie dostępu muteksem
                    if username not in registered_users or registered_users[username] != password:
                        resp = {"type": "info", "success": False, "message": "Błędne dane logowania."}
                        client_socket.sendall((json.dumps(resp) + "\n").encode('utf-8'))
                    elif username in online_users:
                        resp = {"type": "info", "success": False, "message": "Użytkownik jest już zalogowany."}
                        client_socket.sendall((json.dumps(resp) + "\n").encode('utf-8'))
                    else:
                        current_username = username
                        online_users[username] = client_socket
                        
                        # Przesłanie listy obecnych użytkowników
                        user_list = list(online_users.keys())
                        resp = {"type": "user_list", "success": True, "users": user_list, "message": "Zalogowano pomyślnie."}
                        client_socket.sendall((json.dumps(resp) + "\n").encode('utf-8'))
                
                # Wysłanie notyfikacji o podłączeniu do reszty użytkowników (poza blokadą, wewnątrz używa muteksu)
                if current_username:
                    broadcast_message({"type": "status", "username": current_username, "status": "połączony"}, exclude_username=current_username)

            elif msg_type == 'broadcast' and current_username:
                message = data.get('message')
                msg_dict = {"type": "broadcast", "sender": current_username, "message": message}
                broadcast_message(msg_dict)

            elif msg_type == 'private' and current_username:
                recipient = data.get('recipient')
                message = data.get('message')
                
                with lock: # Odczyt obecności wymaga muteksu
                    recipient_sock = online_users.get(recipient)
                
                if recipient_sock:
                    msg_dict = {"type": "private", "sender": current_username, "message": message}
                    try:
                        recipient_sock.sendall((json.dumps(msg_dict) + "\n").encode('utf-8'))
                    except Exception:
                        pass
                else:
                    resp = {"type": "info", "success": False, "message": f"Użytkownik {recipient} nie jest online."}
                    client_socket.sendall((json.dumps(resp) + "\n").encode('utf-8'))

    except Exception as e:
        print(f"[BŁĄD] {addr}: {e}")
    finally:
        # Obsługa rozłączenia
        if current_username:
            with lock:
                if current_username in online_users:
                    del online_users[current_username]
            broadcast_message({"type": "status", "username": current_username, "status": "rozłączony"})
            print(f"[ROZŁĄCZONO] Użytkownik {current_username} wyszedł.")
        else:
            print(f"[ROZŁĄCZONO] Niezalogowany klient {addr} wyszedł.")
        
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        
    server.bind((HOST, port))
    server.listen()
    print(f"[START] Serwer nasłuchuje na porcie {port}")

    try:
        while True:
            client_socket, addr = server.accept()
            # Każdy klient jest obsługiwany w oddzielnym wątku
            thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
            thread.start()
            print(f"[AKTYWNE WĄTKI KLIENTÓW] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[ZAMYKANIE] Serwer kończy działanie.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
