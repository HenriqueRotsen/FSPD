#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include "spend_time.h"

#define NUM_RESOURCES 8

int resourceArr[NUM_RESOURCES]; // Array que diz se um recurso está travado ou não
pthread_cond_t new_resources;   // Variavel de condição que indica a presença de um novo recurso disponível

pthread_mutex_t mutex; // Declaração do mutex

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

// Definindo uma certa quantidade de threads
Thread threads[1000];

void init_recursos()
{
    for (int i = 0; i < NUM_RESOURCES; i++)
    {
        resourceArr[i] = 0;
    }
}

// Função para travar os recursos
void trava_recursos(int resources[], int num_resources)
{
    // Trava a mutex para apenas uma thread acessar a sessão critica
    pthread_mutex_lock(&mutex);

    // Variável que indica de os recursos estão livres, inicialmente sim (1)
    int free = 1;
    do
    {
        free = 1;
        // Para todos os recursos que ele pede
        for (int i = 0; i < num_resources; i++)
        {
            // Verifica se os recursos estão sendo usados
            if (resourceArr[resources[i]] == 1)
            {
                free = 0;
                break;
            }
        }
        // Se todos os recursos estiverem livres
        if (free == 1)
        {
            // Marque eles como travados
            for (int i = 0; i < num_resources; i++)
            {
                resourceArr[resources[i]] = 1;
            }
        }
        // Senão espere ate que algum seja liberado e tente novamente
        else
        {
            pthread_cond_wait(&new_resources, &mutex);
        }
    } while (!free);

    // Destrava a mutex
    pthread_mutex_unlock(&mutex);
}

/* Função para liberar os recursos
   Nesse caso, não bloqueio a mutex pois nunca deve acontecer de
   2 ou mais threads tentarem destravar o mesmo recurso, logo o
   acesso não é crítico
*/
void libera_recursos()
{
    int i;
    for (i = 0; i < 1000; i++)
    {
        if (threads[i].thread == pthread_self())
        {
            break;
        }
    }

    for (int j = 0; j < threads[i].num_resources; j++)
    {
        resourceArr[threads[i].resources[j]] = 0;
    }

    // Avisa a todos que estiverem esperando que novos recursos estão disponíveis
    pthread_cond_broadcast(&new_resources);
}

void *thread_function(void *arg)
{
    Thread *threads = (Thread *)arg;

    spend_time(threads->tid, NULL, threads->free_time);
    trava_recursos(threads->resources, threads->num_resources);
    spend_time(threads->tid, "C", threads->critical_time);
    libera_recursos();

    pthread_exit(NULL);
}

int main()
{
    init_recursos();
    int tid, free_time, critical_time, num_resources;
    int cont = 0, aux;
    pthread_cond_init(&new_resources, NULL);

    // para cada thread
    while (scanf("%d %d %d", &tid, &free_time, &critical_time) != EOF)
    {
        threads[cont].tid = tid;
        threads[cont].free_time = free_time;
        threads[cont].critical_time = critical_time;
        threads[cont].num_resources = 0;

        // printf("%d %d %d\n", threads[cont].tid, threads[cont].free_time, threads[cont].critical_time);

        // ler os recursos
        char linha[100];   // Assumindo um tamanho máximo de 1000 caracteres por linha
        char *ptr = linha; // Ponteiro para percorrer a linha
        int num, k = 0;

        // Ler uma linha inteira
        fgets(linha, sizeof(linha), stdin);

        // Ignora qualquer espaço em branco
        ptr += strspn(ptr, " \t");

        // Usar sscanf para extrair os números
        while (sscanf(ptr, " %d", &num) == 1)
        {
            threads[cont].resources[k] = num;
            threads[cont].num_resources++;
            k++;

            // Avançar para o próximo número na linha
            ptr += strspn(ptr, "0123456789") + 1;
        }
        pthread_create(&threads[cont].thread, NULL, thread_function, (void *)&threads[cont]);
        cont++;
    }

    for (int i = 0; i < cont; i++)
    {
        pthread_join(threads[i].thread, NULL);
    }
}