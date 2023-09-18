#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include "spend_time.h"

#define NUM_RESOURCES 8

int resourceArr[NUM_RESOURCES]; //Array que diz se um recurso está travado ou não
pthread_cond_t new_resources;

pthread_mutex_t mutex; //Declaração do mutex

// Estrutura para armazenar os parâmetros de cada thread
typedef struct
{
    pthread_t thread;
    int tid;
    int free_time;
    int critical_time;
    int num_resources;
    int resources[NUM_RESOURCES];
} Thread;

Thread threads[1000];

void init_recursos()
{
    for (int i = 0; i < NUM_RESOURCES; i++)
    {
        resourceArr[i] = 0;
    }
}

void trava_recursos(int resources[], int num_resources)
{
    pthread_mutex_lock(&mutex);
    int free = 1;
    do{
        free = 1;
        for (int i = 0; i < num_resources; i++)
        {
            if (resourceArr[resources[i]] == 1)
            {
                free = 0;
                break;
            }
        }
        if (free == 1)
        {
            for (int i = 0; i < num_resources; i++)
            {
                resourceArr[resources[i]] = 1;
            }
        }
        else
        {
            pthread_cond_wait(&new_resources, &mutex);
        }
    }
    while(!free);
    pthread_mutex_unlock(&mutex);
}

void libera_recursos(int *resources, int num_resources)
{
    for (int i = 0; i < num_resources; i++)
    {
        resourceArr[resources[i]] = 0;
    }
    pthread_cond_broadcast(&new_resources);
}

void *thread_function(void *arg)
{
    Thread *threads = (Thread *)arg;

    spend_time(threads->tid, NULL, threads->free_time);
    trava_recursos(threads->resources, threads->num_resources);
    spend_time(threads->tid, "C", threads->critical_time);
    libera_recursos(threads->resources, threads->num_resources);

    pthread_exit(NULL);
}

int main()
{
    init_recursos();
    int tid, free_time, critical_time, num_resources;
    int cont = 0, aux;
    pthread_cond_init(&new_resources, NULL);

    // para cada thread
    for (int i = 0; i<4; i++)
    {
        scanf("%d %d %d", &tid, &free_time, &critical_time);
        threads[i].tid = tid;
        threads[i].free_time = free_time;
        threads[i].critical_time = critical_time;
        threads[i].num_resources = 0;

        //printf("%d %d %d\n", threads[i].tid, threads[i].free_time, threads[i].critical_time);
        
        // ler os recursos
        char linha[100]; // Assumindo um tamanho máximo de 1000 caracteres por linha
        char *ptr = linha; // Ponteiro para percorrer a linha
        int num, k=0;

        // Ler uma linha inteira
        fgets(linha, sizeof(linha), stdin); 

        // Ignora qualquer espaço em branco
        ptr += strspn(ptr, " \t");
        
        // Usar sscanf para extrair os números
        while (sscanf(ptr, " %d", &num) == 1) 
        {
            threads[i].resources[k] = num;
            threads[i].num_resources++;
            k++;

            // Avançar para o próximo número na linha
            ptr += strspn(ptr, "0123456789") + 1;
        }
        cont++;
        pthread_create(&threads[i].thread, NULL, thread_function, (void *)&threads[i]);
    }

    for (int i = 0; i < cont; i++)
    {
        pthread_join(threads[i].thread, NULL);
    }
}