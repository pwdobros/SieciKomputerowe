#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/types.h>

#define DEFAULT_PORT 80
#define BUFFER_SIZE 4096

int main(int argc, char *argv[]) {
    // Sprawdzenie czy userid != 0 (blokowanie uruchomienia z konta roota)
    if (getuid() == 0) {
        fprintf(stderr, "Błąd: uruchamianie serwera z konta root jest zablokowane.\n");
        return 1;
    }

    int port = DEFAULT_PORT;
    if (argc > 1) {
        port = atoi(argv[1]);
        if (port <= 0 || port > 65535) {
            fprintf(stderr, "Błąd: nieprawidłowy numer portu.\n");
            return 1;
        }
    }

    // 1. socket
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("socket failed");
        return 1;
    }

    // 2. setsockopt
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) == -1) {
        perror("setsockopt failed");
        close(server_fd);
        return 1;
    }

    // 3. bind
    struct sockaddr_in addr;
    memset((char*)&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY); // Dla 127.0.0.1 użyj: htonl(INADDR_LOOPBACK)
    addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        perror("bind failed");
        close(server_fd);
        return 1;
    }

    // 4. listen
    if (listen(server_fd, 5) == -1) {
        perror("listen failed");
        close(server_fd);
        return 1;
    }

    printf("Serwer nasłuchuje na porcie %d...\n", port);

    // 5. accept w pętli (iteracyjna obsługa klientów)
    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr, &client_len);
        if (client_fd == -1) {
            perror("accept failed");
            continue; 
        }

        // 6. recv - blokujące oczekiwanie na przesłanie zapytania przez klienta
        char buffer[BUFFER_SIZE];
        ssize_t bytes_received = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
        if (bytes_received == -1) {
            perror("recv failed");
            close(client_fd);
            continue;
        }
        
        // Zignorowanie sparsowania zapytania i przygotowanie odpowiedzi (uptime)
        FILE *uptime_file = fopen("/proc/uptime", "r");
        if (!uptime_file) {
            perror("fopen /proc/uptime failed");
            close(client_fd);
            continue;
        }
        
        char uptime_str[256];
        if (fgets(uptime_str, sizeof(uptime_str), uptime_file) == NULL) {
            perror("fgets failed");
            fclose(uptime_file);
            close(client_fd);
            continue;
        }
        fclose(uptime_file);
        
        // Wyciągnięcie pierwszej wartości z /proc/uptime (do znaku spacji)
        char *space_pos = strchr(uptime_str, ' ');
        if (space_pos != NULL) {
            *space_pos = '\0';
        }

        const char* http_header_template = 
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/plain; charset=UTF-8\r\n"
            "Connection: close\r\n"
            "Content-Length: %d\r\n"
            "\r\n";
            
        int content_length = strlen(uptime_str);
        char headers[512];
        int header_len = snprintf(headers, sizeof(headers), http_header_template, content_length);
        
        if (header_len < 0 || (size_t)header_len >= sizeof(headers)) {
            fprintf(stderr, "Błąd formatowania nagłówka.\n");
            close(client_fd);
            continue;
        }

        // 7. send - wielokrotnie: najpierw nagłówki
        if (send(client_fd, headers, header_len, 0) == -1) {
            perror("send headers failed");
            close(client_fd);
            continue;
        }
        
        // 7. send - następnie kod odpowiedzi (treść - uptime)
        if (send(client_fd, uptime_str, content_length, 0) == -1) {
            perror("send body failed");
            close(client_fd);
            continue;
        }

        // 8. shutdown(SHUT_WR)
        if (shutdown(client_fd, SHUT_WR) == -1) {
            perror("shutdown failed");
        }

        // 9. close (klienta)
        if (close(client_fd) == -1) {
            perror("close client failed");
        }
    }

    // 10. close (serwera) - w tym programie nieskończona pętla zapobiega dojściu tutaj
    if (close(server_fd) == -1) {
        perror("close server failed");
    }

    return 0;
}
