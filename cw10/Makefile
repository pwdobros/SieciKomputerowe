CC=gcc
CFLAGS=-Wall -Wextra -O2

all: server

server: server.c
	$(CC) $(CFLAGS) -o server server.c

clean:
	rm -f server

help:
	@echo "Aby uruchomić serwer na porcie niższym niż 1024 bez konta root,"
	@echo "nadaj mu uprawnienia:"
	@echo "sudo setcap 'cap_net_bind_service=+ep' server"
