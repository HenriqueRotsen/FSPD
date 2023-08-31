#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include "spend_time.h"

#define NUM_RESOURCES 8

// Estrutura para armazenar os parâmetros de cada thread
typedef struct{
    pthread_mutex_t resource_mutex[NUM_RESOURCES];
    int tid;
    int free_time;
    int critical_time;
    int num_resources;
    int resources[NUM_RESOURCES];
}ThreadParams;


void init_recursos(ThreadParams *recursos) {
    for (int i = 0; i < NUM_RESOURCES; i++) {
        pthread_mutex_init(&recursos->resource_mutex[i], NULL);
    }
    // Inicialize outros campos da estrutura de recursos
}

void trava_recursos(ThreadParams *recursos, int *resources, int num_resources) {
    for (int i = 0; i < num_resources; i++) {
        pthread_mutex_lock(&recursos->resource_mutex[resources[i]]);
    }
}

void libera_recursos(ThreadParams *recursos, int *resources, int num_resources) {
    for (int i = 0; i < num_resources; i++) {
        pthread_mutex_unlock(&recursos->resource_mutex[resources[i]]);
    }
}

void *thread_function(void *arg) {
    struct ThreadParams *params = (struct ThreadParams *)arg;

    spend_time(params->tid, NULL, params->free_time);
    trava_recursos(&recursos, params->resources, params->num_resources);
    spend_time(params->tid, "C", params->critical_time);
    libera_recursos(&recursos, params->resources, params->num_resources);

    pthread_exit(NULL);
}

int main() {
    init_recursos();
    int tid, free_time, critical_time, num_resources;

    while (scanf("%d %d %d %d", &tid, &free_time, &critical_time, &num_resources) != EOF) {
        struct ThreadParams *params = (struct ThreadParams *)malloc(sizeof(struct ThreadParams));
        params->tid = tid;
        params->free_time = free_time;
        params->critical_time = critical_time;
        params->num_resources = num_resources;

        for (int i = 0; i < num_resources; i++) {
            scanf("%d", &params->resources[i]);
        }

        pthread_t thread;
        pthread_create(&thread, NULL, thread_function, params);
    }

    pthread_exit(NULL);
}
