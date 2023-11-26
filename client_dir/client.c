#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

#define CONFIG_FILE_NAME "config.txt"
#define LOG_FILE_NAME "client_log.log"
#define RUNTIME 20

void handle_config(char (*serv_ip)[32], int *serv_port) {
    char buffer_port[8];
    FILE *fp;
    
    fp = fopen(CONFIG_FILE_NAME, "r");
    if (!fp) {
        printf("Error: %s was not created!\n", CONFIG_FILE_NAME);
        exit(1);
    }

    fgets(*serv_ip, 32, fp);
    fgets(buffer_port, 8, fp);
    *serv_port = atoi(buffer_port);
}

void get_time(char (*buffer)[32]) {
    time_t timer = time(NULL);
    strftime(*buffer, 26, "%a %b %Y, %H:%M:%S", localtime(&timer));
}

void log_connection(FILE *log_file, char serv_ip[32]) {
    char time[32];
    get_time(&time);

    fprintf(log_file, "%s: Connected to %s", time, serv_ip);
}

void log_disconnection(FILE *log_file, char serv_ip[32]) {
    char time[32];
    get_time(&time);

    fprintf(log_file, "%s: Disconnected from %s", time, serv_ip);
}

void log_send(FILE *log_file, char *msg) {
    char time[32];
    get_time(&time);

    fprintf(log_file, "%s: %s\n", time, msg);
}

void log_recv(FILE *log_file, char *msg) {
    char time[32];
    get_time(&time);

    fprintf(log_file, "%s: server: %s\n", time, msg);
}

void timer(int sec) {
    clock_t wait;
    wait = clock() + sec * CLOCKS_PER_SEC;
    while (clock() < wait) ;
}

int main() {
    FILE *log_file;
    char server_ip[32];
    int server_port; 
    int sockfd, len;
    int result;
    struct sockaddr_in address;

    handle_config(&server_ip, &server_port);
    
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = inet_addr(server_ip);
    address.sin_port = htons(server_port);

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    len = sizeof(address);
    
    log_file = fopen(LOG_FILE_NAME, "w");
    if (!log_file) {
        printf("Error: %s was not created!\n", LOG_FILE_NAME);
        exit(1);
    }
    
    result = connect(sockfd, (struct sockaddr *)&address, len);
    if (result == -1) {
        perror("Error: client 1");
        exit(1);
    }
    log_connection(log_file, server_ip);
    timer(RUNTIME);

    char message[] = "Савенков И.В., М3О-419Бк-20.";
    write(sockfd, message, sizeof(message) - 1);
    log_send(log_file, message);

    char buffer[1024];
    ssize_t bytesRead = read(sockfd, buffer, sizeof(buffer) - 1);
    if (bytesRead > 0) {
        buffer[bytesRead] = '\0';

        timer(RUNTIME);
        log_recv(log_file, buffer);
    }

    close(sockfd);
    log_disconnection(log_file, server_ip);

    fclose(log_file);

    exit(0);
}