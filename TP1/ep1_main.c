#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include "spend_time.h"

#define NUM_RESOURCES 8

int resourceArr[NUM_RESOURCES]; //Array que diz se um recurso está travado ou não

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
    pthread_mutex_unlock(&mutex);
}

void libera_recursos(int *resources, int num_resources)
{
    for (int i = 0; i < num_resources; i++)
    {
        resourceArr[resources[i]] = 0;
    }
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

    // para cada thread
    for (int i = 0;; i++)
    {
        scanf("%d %d %d", &tid, &free_time, &critical_time);
        threads[i].tid = tid;
        threads[i].free_time = free_time;
        threads[i].critical_time = critical_time;
        threads[i].num_resources = 0;

        printf("%d %d %d\n", threads[i].tid, threads[i].free_time, threads[i].critical_time);
        
        // ler os recursos
        char linha[1000]; // Assumindo um tamanho máximo de 1000 caracteres por linha
        int num;

        // Ler uma linha inteira
        fgets(linha, sizeof(linha), stdin);

        // Usar sscanf para extrair os números
        while (sscanf(linha, "%d", &num) == 1) {
            // Faça alguma coisa com o número, por exemplo, imprima-o
            printf("Você digitou: %d\n", num);

            // Avançar para o próximo número na linha
            linha += strspn(linha, "0123456789") + 1;
        }
        
        for (int j=0;j<NUM_RESOURCES; j++)
        {
            printf("%d ", threads[i].resources[j]);
        }
        printf("\n");
        
        //pthread_create(&threads[i].thread, NULL, thread_function, (void *)&threads[i]);
        cont++;
    }

    for (int i = 0; i < cont; i++)
    {
        //pthread_join(threads[i].thread, NULL);
    }
}