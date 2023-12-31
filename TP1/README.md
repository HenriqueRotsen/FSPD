Primeiro exercício de programação: travas múltiplas atômicas (trabalho individual) 2023-2

Exercício individual

Prazo de entrega: confira o moodle, no link de entrega
Introdução

Neste trabalho vamos implementar um sistema de sincronização entre threads que controlará o acesso a diversas travas de forma simultânea, em um modelo trava tudo ou nada.

Objetivo

Como veremos nas próximas aulas, um recurso importante em sistemas distribuídos é ser capaz de requisitar e obter de uma só vez todos os recursos que precisam de exclusão mútua em sistemas distribuídos. isto é, se uma thread precisa de três recursos para continuar com exclusão mútua, ou ela consegue os três de uma vez, ou fica esperando até que os três fiquem disponíveis para ela. Até então, sua execução fica suspensa, como quando se tenta travar uma variável de exclusão mútua que já esteja travada.

Seu objetivo será criar um programa em C, com Pthreads, que deve criar um certo número de threads e um conjunto de 8 recursos. Seu mecanismo de sincronização, ao ser chamado, permitirá que uma thread indique quais dos 8 recursos ela necessita obter; aquela thread só poderá prosseguir quando conseguir ter acesso a todos os recursos escolhidos simultaneamente. Enquanto isso não ocorrer, nenhum daqueles recursos ficará bloqueado por aquele pedido, isto é, a operação de obter qualquer número de recursos é atômica: enquanto todos os recursos pedidos não estiverem disponíveis, nenhum dos recursos é bloqueado; quando todos estiverem disponíveis, a chamada de travamento retorna com todos os recursos solicitadas bloqueados.

O princípio de operação

Durante a execução o programa criará diversas threads, segundo os dados de entrada (mais sobre isso a seguir). Cada thread deverá primeiro passar algum tempo (potencialmente zero) executando um trabalho "simples" (sem sincronização) e depois deverá obter um certo conjunto de recursos e passar outro tempo em um trabalho "crítico" para o qual necessita a posse dos recursos. Depois que o tempo de trabalho terminar, a thread libera todos os recursos que estavam sob seu controle e termina. 
Sobre esses recursos, você deverá definir as operações:

    void init_recursos(void) - inicializa a estrutura de dados que você definir para representar os recursos;
    void trava_recursos(recursos) - uma thread pede para reservar um conjunto de recursos, representados da forma que seu programa preferir;
    void libera_recursos(void) - uma thread que já reservou alguns recursos sinaliza que completou seu trabalho crítico, liberando os recursos.

Uma thread que pede para travar um recurso que já esteja sendo usado por outra deve esperar até que aquele recurso e todos os outros que ela requisitou estejam disponíveis. Quando um recurso se tornar disponível ele pode ser assinalado para qualquer thread que esteja esperando por ele, desde que tal thread tenha todos os recursos que solicitou. Se mais de uma thread pode completar seu conjunto de recursos quando um recurso específico fica disponível, qualquer uma delas pode prosseguir, enquanto a outra deve continuar esperando.

Se um recurso disponível faz parte do conjunto requisitado por uma thread que tem que esperar por outros recursos já travados por outras threads, aquele recurso não é pré-alocado. Por exemplo, se em um certo momento só o recurso 1 está travado por uma thread e uma segunda thread requisita os recursos 1 e 2, essa thread tem que esperar; se antes do recurso 1 ser liberado, uma terceira thread tenta travar apenas o recurso 2, ela pode prosseguir, pois o recurso continua liberado; nesse caso, a segunda thread teria agora que esperar pela liberação dos dois recursos para continuar.

Normalmente, threads em um sistema passam a maior parte do seu tempo realizando alguma tarefa mais longa, como uma manipulação de uma estrutura de dados complexa, ou um cálculo com vários operadores. Para simplificar e generalizar essa passagem do tempo, os arquivos  spend_time.h e spend_time.c são fornecidos. A função spend_time replica a passagem do tempo que computações mais complexas causariam. A função internamente gera um registro da passagem do tempo, que será usado pelo processo de avaliação automática. Para isso, a função recebe como parâmetros o identificador da thread, uma string de informação e o tempo, em décimos de segundos, que ela deve ocupar. Se a string existe (não é NULL), a função gera uma linha de log na saída padrão (stdout).

Considerando o comportamento esperado de cada thread, o corpo das mesmas deve ser descrito basicamente pelo seguinte (pseudo)código:

// No início da thread, ela deve receber como parâmetros seu tid, os tempos livre e crítico
//    e os recursos que ela necessita para completar seu trabalho
// Em segunda, ela deve executar as operações:
  spend_time(tid,NULL,tlivre);
  trava_recursos(recursos);     // a forma de representar os recursos é uma decisão do desenvolvedor
  spend_time(tid,"C",tcritico);
  libera_recursos();            // note que cada thread deve ser ter sua lista de recursos registrada em algum lugar
  pthread_exit(); 

Exceto pelo detalhamento do tipo de dados recursos, as linhas acima devem ser mantidas sem outras alterações no código final.
Entrada do problema

o programa deverá ler da entrada padrão (stdin) a descrição de cada thread que deverão ser criadas, uma por linha, até o fim da entrada padrão (EOF). Cada linha será composta por inteiros separados por espaços, sendo o primeiro o indentificador da thread (na faixa 1..1000), dois inteiros indicando, em décimos de segundo, os tempos livre e crítico, respectivamente, e a lista de recursos que a thread deve travar (1 a 8 números, de 0 a 7). Cada thread requistará pelo menos um recurso.

Cada thread deve ser criada assim que a linha com sua descrição seja lida. Não é permitido esperar pela leitura de todas as linhas da entrada para iniciar a execução. Como mencionado anteriormente, a entrada termina com o fim do arquivo. Para simplificar o código, pode-se assumir que no máximo 1000 threads serão criadas e todas terão identificadores diferentes.

A leitura deve ser feita da entrada padrão usando scanf ou uma solução equivalente. O programa não deve receber nenhum parâmetro da linha de comando e não deve abrir nenhum arquivo explicitamente (basta usar a entrada padrão). Certifique-se de entender o comportamento de scanf ao ler um marcador de fim de arquivo e como gerar esse marcador se estiver executando o programa diretamente da linha de comando, sem redirecionamento.

O formato da entrada será garantido sem erros (não é preciso incluir código para verificar se os valores seguem a especificação). 

Um exemplo de arquivo de entrada será apresentado ao final desta página.

Detalhamento da implementação

Seu programa deve observar os seguintes pontos, que devem ser bem documentados por comentários no código fonte:

Representação do conjunto de recursos: seu código deve definir uma abstração de sincronização como um tipo abstrato de dados que represente o conjunto de recursos disponíveis (em um total de 8) (p.ex, um vetor) e o mesmo pode ser mantido como um variável global.

Sincronização adotada: em síntese, o objetivo principal deste exercício, do ponto de vista da disciplina, é a criação e controle de um grupo de threads, que deverão acessar os recursos de forma sincronizada, segundo a regra apresentada. Essa sincronização deve ser implementada usando variáveis de exclusão mútua e de condição (uma solução com semáforos nesse caso seria mais complexa e será penalizada se for usada).

Uso controlado de travas: existem diversas soluções possíveis para esse problema. Entretanto, a sua solução só deve manter variáveis de exclusão mútua travadas dentro das funções de travamente e liberação - isto é, toda mutex travada dentro de uma função deve ser destravada antes do retorno daquela função. Soluções que não obedeçam esse requisito serão penalizadas.

Sobre a execução do programa:

Como mencionado, seu programa deve ler da entrada padrão e escrever na saída padrão. Ele não deve receber parâmetros de linha de comando. Não é preciso testar por erros na entrada, mas seu programa deve funcionar com qualquer combinação válida.

A única saída esperada para seu programa será gerada pelos comandos printf dentro da função spend_time. Caso você inclua mensagens de depuração ou outras informações que sejam exibidas durante a execução, certifique-se de removê-las da saída na execução da versão final.

O código deve usar apenas C padrão (não C++), sem bibliotecas além das consideradas padrão. O paralelismo de threads deve ser implementado usando POSIX threads (Pthreads) apenas.

O material desenvolvido por você deve executar sem erros nas máquinas linux do laboratório de graduação. A correção será feita naquelas máquinas e programas que não compilarem, não seguirem as determinações quanto ao formato da entrada e da saída, ou apresentarem erros durante a execução, serão desconsiderados.
O que deve ser entregue:

Você deve entregar apenas um arquivo, de nome ep1_main.c, contendo todo o código necessário, que inclua spend_time.h. Os arquivos spend_time.[ch] não podem ser alterados e não devem ser incluídos na entrega (eles serão de qualquer forma substituídos pelos originais antes da correção). Novamente, o material desenvolvido por você deve executar sem erros nas máquinas linux do laboratório de graduação.

Não é necessário apresentar um relatório em PDF, mas seu código deve ser bem comentado. Em particular, as estruturas de dados utilizadas para representar recursos solicitados e travados e o princípio de funcionamento das funções de reserva e liberação de recursos devem ser claramente descritas. Essa clareza dos comentários será considerada na avaliação.

Preste atenção nos prazos: entregas com atraso serão aceitas por um ou dois dias, mas serão penalizadas.
Sugestões de depuração

Faz parte do exercício desenvolver os casos de teste para o mesmo. Não serão fornecidos arquivos de teste além da entrada descrita a seguir. Vocês devem criar os seus próprios arquivos e podem compartilhá-los no fórum do exercício. Por outro lado, obviamente não é permitido discutir o princípio de sincronização da solução.
Dúvidas?

Usem o fórum criado especialmente para esse exercício de programação para enviar suas dúvidas. Não é permitido publicar código no fórum! Se você tem uma dúvida que envolve explicitamente um trecho de código, envie mensagem por e-mail diretamente para o professor.
Exemplo de entrada:

Segundo o formato definido, as linhas a seguir definem 4 threads

-------------
11 5 10 7 6
12 0 10 6
13 17 7 0 1 2 3 4 5 6 7 
14 15 8 0
-------------

Não executei o programa ainda, mas a saída para essa entrada (lida por redirecionamento da entrada para um arquivo contendo as quatro linhas), em uma máquina que não esteja sobrecarregada, deve ser a como a lista a seguir.  O tempo total de execução deveria ser da casa de 3 segundos. Mudanças nesse tempo total podem indicar erros na sincronização (mas pequenas variações são possíveis).

-------------
  0:12:C [10
  5:11:E
 10:12:C ]
 10:11:C [10
 15:14:E
 15:14:C [8
 17:13:E
 23:14:C ]
 23:13:C [7
 30:13:C ]
------------

(No momento, essa saída foi gerada manualmente, sem a execução do programa - isto é, podem haver erros.)