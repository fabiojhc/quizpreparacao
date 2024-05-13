import json
import os
import random

import google.generativeai as genai

genai.configure(api_key=os.environ['API_KEY_GEMINI'])

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

pontos = {"score":0, "totalQuestoesRealizadas":0,"questoesCertas":0}

def escreverArquivo(texto):
    meu_arquivo = open("historico.txt", "a")
    meu_arquivo.write(texto + "\n")
    meu_arquivo.close()

def isCorreta(opcaoEscolhida, assertivaCorreta):
    return opcaoEscolhida.upper() == assertivaCorreta.upper()

def calcularQuestoes(isCorreta,pontos):
    pontos["totalQuestoesRealizadas"] += 1
    if isCorreta:
        pontos["questoesCertas"] += 1
    pontos["score"] = pontos["questoesCertas"]/pontos["totalQuestoesRealizadas"]

def setarMensagem(isCorreta):
    if (isCorreta):
        mensagem = "Parabéns, acertou."
    else:
        mensagem = "Infelizmente errou."
    return mensagem + " " + questao["explicacao_da_assertiva_correta"] + "\n"
    
def mostrarMensagemTela(mensagem):
    print(mensagem)

def topicoAleatorio(selecao):
    topicoSelecionadoAleatoriamente = random.choice(selecao)
    print (f"O tópico selecionado aleatoriamente foi: {topicoSelecionadoAleatoriamente} \n")
    return topicoSelecionadoAleatoriamente

def mostrarPontuacaoAtual(pontos):
    if (pontos["totalQuestoesRealizadas"]==1):
        print("Você fez 1 questão até o momento.")
    else:
        print(f"Você fez {str(pontos['totalQuestoesRealizadas'])} questões até o momento.")
    if (pontos["questoesCertas"] == 0):
        print("Você ainda não acertou questões")
    elif (pontos["questoesCertas"] == 1):
        print("Você acertou 1 questão")
    else:
        print(f"Você acertou {str(pontos['questoesCertas'])} questões até o momento.")
    
    print(f"Obtendo um score de {str(pontos['score'] * 100)} \n")

def getListaOpcoesQuiz():
    try:
        with open('lista_topico.json', 'r') as arquivo:
            data = json.load(arquivo)
            lista_exames = data["exames"]
            return lista_exames
    except Exception as excecao:
        print("Erro")

def mostrarOpcoesQuiz(lista_exames):
    for exame in lista_exames:
        print(f"{exame['id_exame']} - {exame['nome_exame']}")

def selecionarOpcaoQuiz(lista_exames, opcao):
    try:
        return [dict for dict in lista_exames if dict["id_exame"] == opcao][0]
    except Exception as erro:
        print(f"Erro ao selecionar uma opção de quiz {erro}")

lista_exames = getListaOpcoesQuiz()
mostrarOpcoesQuiz(lista_exames)
opcao = int(input(f"Escolha uma opção de quiz ou digite 0 para sair : "))
selecao = selecionarOpcaoQuiz(lista_exames, opcao)
exame = selecao['nome_exame']
numeroDeQuestoes = 5
chat = model.start_chat(history=[])

while (opcao != 0):
    topico = input("Qual o topico que deseja escolher? Caso prefira, apenas pressione enter para um tópico aleatório ")
    if (topico == ""):
        topico = topicoAleatorio(selecao['lista_topico'])
    
    prompt = "Gere uma lista não repetida de " + str(numeroDeQuestoes) + "lista_questoes, de nome questoes,  no padrão do exame " + exame + " sobre o tópico:  " + topico + "; cada questão deve conter os campos: titulo_da_questao; letra_da_assertiva_correta,  explicacao_da_assertiva_correta  e uma lista com 4 alternativas chamada de lista_de_assertivas, cada assertiva deve conter a letra_da_assertiva e o  texto_da_assertiva; em formato JSON;"
    try:
        print("Favor aguardar um instante, enquanto a requisição ao Gemini é realizada...")
        response = chat.send_message(
        prompt)
        textoJson  = response.text
        textoJson = textoJson.replace("```json","")
        textoJson = textoJson.replace("```", "")
        questoes = json.loads(textoJson)
        for questao in questoes["questoes"]:
            print(questao["titulo_da_questao"])
            escreverArquivo(questao["titulo_da_questao"])
            for assertiva in questao["lista_de_assertivas"]:
                print(assertiva["letra_da_assertiva"], assertiva["texto_da_assertiva"])
                escreverArquivo(assertiva["letra_da_assertiva"] + " - " + assertiva["texto_da_assertiva"])
            
            opcaoAssertiva = input("Qual a letra da alternativa de sua resposta?")

            isQuestaoCorreta = isCorreta(opcaoAssertiva,questao["letra_da_assertiva_correta"])
            calcularQuestoes(isQuestaoCorreta,pontos)
            mensagem = setarMensagem(isQuestaoCorreta)
            escreverArquivo(mensagem)
            mostrarMensagemTela(mensagem)
            mostrarPontuacaoAtual(pontos)

            
    except Exception as excecao:
        print(f"Não foi possível conectar à Inteligência Artificial {excecao}")
    
    except Exception as excecao:
        print(f"Não foi possível conectar à Inteligência Artificial {excecao}")

    opcao = input("Deseja continuar? Digite 'N' para sair ou pressione enter para continuar ")
    if (opcao.upper() == "N"):
        break