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

def topicoAleatorio():
    try:
        with open('lista_topico.txt', 'r') as lista:
            linhas = lista.readlines()
            random_integer = random.randint(1, len(linhas))
        topicoSelecionadoAleatoriamente = linhas[random_integer-1].replace("\n","")
        print ("O tópico selecionado aleatoriamente foi: " + topicoSelecionadoAleatoriamente + "\n")
        return topicoSelecionadoAleatoriamente
    except Exception as excecao:
        print("Houve um erro durante a tentativa de leitura do arquivo lista_topico.txt")
        print("Retornando consulta sobre o tópico Geral")
        return "Geral"

def mostrarPontuacaoAtual(pontos):
    if (pontos["totalQuestoesRealizadas"]==1):
        print("Você fez 1 questão até o momento.")
    else:
        print("Você fez " + str(pontos["totalQuestoesRealizadas"]) + " questões até o momento.")
    if (pontos["questoesCertas"] == 0):
        print("Você ainda não acertou questões")
    elif (pontos["questoesCertas"] == 1):
        print("Você acertou 1 questão")
    else:
        print("Você acertou " + str(pontos["questoesCertas"]) + " questões até o momento.")
    
    print("Obtendo um score de " + str(pontos["score"] * 100) + "%\n")

opcao = input("Deseja fazer uma questão no padrão do exame aws?Digite 'N' para sair ou pressione enter para continuar ")
numeroDeQuestoes = 5
nova = ""


while (opcao.upper() != "N"):
    topico = input("Qual o topico que deseja escolher? Caso prefira, apenas pressione enter para um tópico aleatório ")
    if (topico == ""):
        topico = topicoAleatorio()
    
    prompt = "Gere uma " + nova + " lista de " + str(numeroDeQuestoes) + "questões no padrão do exame aws clf-02 sobre o tópico:  " + topico + "; cada questão deve conter os campos: titulo_da_questao; letra_da_assertiva_correta,  explicacao_da_assertiva_correta  e uma lista com 4 alternativas chamada de lista_de_assertivas, cada assertiva deve conter a letra_da_assertiva e o  texto_da_assertiva; em formato JSON;"
    try:
        print("Favor aguardar um instante, enquanto a requisição ao Gemini é realizada...")
        response = chat.send_message(
        prompt)
        nova = "nova"
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
        print("Não foi possível conectar à Inteligência Artificial")

    opcao = input("Deseja continuar? Digite 'N' para sair ou pressione enter para continuar ")
    if (opcao.upper() == "N"):
        break