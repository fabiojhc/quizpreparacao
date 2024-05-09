# Quizpreparacao (python)
Perguntas e respostas geradas pelo gemini

É apenas uma execução de um comando para se elaborar um quiz com perguntas sobre o aws cloud practitioner com o Gemini.
Para customizar os prompts, é possível alterar os valores das variáveis no código python


1 - Instale o Python -  Passo a Passo no Windows :(https://python.org.br/instalacao-windows/)
2 - Instale o pip - Passo a passo no Windows : (https://pt.stackoverflow.com/questions/239047/como-instalar-o-pip-no-windows-10)
3 - Instale o SKD do Python para o Gemini :(na linha de comando(no gitbash por exemplo) executar: pip install -q -U google-generativeai
4 - Crie uma API Key para o Gemini (https://support.gemini.com/hc/pt-br/articles/360031080191-Como-fa%C3%A7o-para-criar-uma-chave-de-API)
5 - Crie uma variável de ambiente com o nome : API_KEY_GEMINI e sete o valor dela para o valor da Key criada no passo 4.
6 - Execute o arquivo preparacaoaws.py no python (pode ser acionado pela IDE de programação de sua escolha ou por linha de comando, por exemplo pelo gitbash, sendo chamado o comando: python preparacaoaws.py) (lembrando que para o comando funcionar diretamente na linha de comando é necessário criar uma variável de ambiente para o executável do python) 
  (Acesse as configurações avançadas do sistema no Painel de Controle.
  Clique em “Variáveis de Ambiente” e, em seguida, em “Variáveis do Sistema”.
  Na seção “Variáveis do Sistema”, encontre a variável “Path” e clique em “Editar”.
  Adicione o caminho para o diretório “Scripts” da instalação do Python à variável “Path”. Por exemplo, se o Python estiver instalado em “C:\Python\Scripts”, adicione esse caminho à lista de variáveis.) (https://awari.com.br/tutorial-de-python-para-windows/#:~:text=Acesse%20as%20configura%C3%A7%C3%B5es%20avan%C3%A7adas%20do,Python%20%C3%A0%20vari%C3%A1vel%20%E2%80%9CPath%E2%80%9D.)
7 - Para incluir mais tópicos, basta incluir uma nova linha no arquivo lista_topico.txt
