import json
import os

ARQUIVO = "gastos.json"

def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    
    arquivo = open(ARQUIVO, "r")
    conteudo = arquivo.read()
    arquivo.close()
    
    if conteudo == "":
        return []
    
    gastos = json.loads(conteudo)
    return gastos

def salvar(gastos):
    arquivo = open(ARQUIVO, "w")
    json.dump(gastos, arquivo)
    arquivo.close()

def adicionar(gastos):
    print("--- adicionar gasto ---")
    
    nome = input("nome: ")
    valor = input("valor: ")
    categoria = input("categoria: ")
    
    valor = float(valor)
    
    gasto = {}
    gasto["id"] = len(gastos) + 1
    gasto["nome"] = nome
    gasto["valor"] = valor
    gasto["categoria"] = categoria
    
    gastos.append(gasto)
    salvar(gastos)
    
    print("gasto adicionado!")

def listar(gastos):
    print("--- lista de gastos ---")
    
    if len(gastos) == 0:
        print("nenhum gasto ainda")
        return
    
    for gasto in gastos:
        print(gasto["id"], "-", gasto["nome"], "-", gasto["categoria"], "- R$", gasto["valor"])

def total(gastos):
    print("--- total ---")
    
    total = 0
    for gasto in gastos:
        total = total + gasto["valor"]
    
    print("total: R$", total)

def filtrar(gastos):
    print("--- filtrar ---")
    
    categoria = input("qual categoria? ")
    
    encontrados = []
    for gasto in gastos:
        if gasto["categoria"] == categoria:
            encontrados.append(gasto)
    
    if len(encontrados) == 0:
        print("nenhum gasto nessa categoria")
        return
    
    for gasto in encontrados:
        print(gasto["id"], "-", gasto["nome"], "- R$", gasto["valor"])

def remover(gastos):
    print("--- remover gasto ---")
    
    listar(gastos)
    
    id = int(input("qual o id? "))
    
    gasto_pra_remover = None
    for gasto in gastos:
        if gasto["id"] == id:
            gasto_pra_remover = gasto
    
    if gasto_pra_remover == None:
        print("nao achei esse id")
        return
    
    gastos.remove(gasto_pra_remover)
    salvar(gastos)
    print("removido!")

def menu():
    print("================")
    print("controle de gastos")
    print("================")
    print("1 - adicionar")
    print("2 - listar")
    print("3 - total")
    print("4 - filtrar")
    print("5 - remover")
    print("6 - sair")
    print("================")

def main():
    print("bem vindo!")
    
    gastos = carregar()
    
    print(len(gastos), "gastos carregados")
    
    while True:
        menu()
        opcao = input("opcao: ")
        if opcao == "1":
            adicionar(gastos)
        if opcao == "2":
            listar(gastos)
        if opcao == "3":
            total(gastos)
        if opcao == "4":
            filtrar(gastos)
        if opcao == "5":
            remover(gastos)
        if opcao == "6":
            print("tchau!")
            break
main()    
