import json
import os

# CONFIGURAÇÕES

ARQUIVO_GASTOS = "gastos.json"

def carregar_gastos():
    """
    Carrega os gastos salvos no arquivo JSON.
    Se o arquivo não existir ou estiver vazio/corrompido, retorna uma lista vazia.
    """
    if os.path.exists(ARQUIVO_GASTOS):
        with open(ARQUIVO_GASTOS, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()  # ✅ Lê o conteúdo primeiro

            if not conteudo:  # ✅ Verifica se está vazio
                print("⚠️  Arquivo encontrado, mas está vazio. Começando do zero!")
                return []

            try:
                return json.loads(conteudo)  # ✅ Tenta decodificar o JSON
            except json.JSONDecodeError:     # ✅ Captura JSON corrompido/inválido
                print("⚠️  Arquivo corrompido! Criando novo arquivo...")
                return []

    return []


def salvar_gastos(gastos):
    """
    Salva a lista de gastos no arquivo JSON.
    """
    with open(ARQUIVO_GASTOS, "w", encoding="utf-8") as arquivo:
        json.dump(gastos, arquivo, indent=4, ensure_ascii=False)

def adicionar_gasto(gastos):
    """
    Solicita os dados do gasto ao usuário e adiciona na lista.
    Salva automaticamente no arquivo após adicionar.
    """
    print("\n➕  ADICIONAR NOVO GASTO")
    print("-" * 30)

    # Coleta o nome do gasto
    nome = input("Nome do gasto: ").strip()
    if not nome:
        print("❌ O nome não pode estar vazio!")
        return

    # Coleta e valida o valor
    try:
        valor = float(input("Valor (R$): ").replace(",", "."))
        if valor <= 0:
            print("❌ O valor deve ser maior que zero!")
            return
    except ValueError:
        print("❌ Valor inválido! Digite um número (ex: 25.90)")
        return

    # Coleta a categoria
    categoria = input("Categoria (ex: Alimentação, Transporte, Lazer): ").strip()
    if not categoria:
        print("❌ A categoria não pode estar vazia!")
        return

    # Cria o dicionário do gasto
    novo_gasto = {
        "id": len(gastos) + 1,
        "nome": nome,
        "valor": valor,
        "categoria": categoria.capitalize()
    }

    # Adiciona na lista e salva no arquivo
    gastos.append(novo_gasto)
    salvar_gastos(gastos)

    print(f"\n✅ Gasto '{nome}' de R$ {valor:.2f} adicionado com sucesso!")


def listar_gastos(gastos):
    """
    Exibe todos os gastos cadastrados de forma organizada.
    """
    print("\n📋  LISTA DE GASTOS")
    print("-" * 50)

    if not gastos:
        print("Nenhum gasto cadastrado ainda.")
        return

    # Cabeçalho da tabela
    print(f"{'ID':<5} {'Nome':<20} {'Categoria':<15} {'Valor':>10}")
    print("-" * 50)

    # Exibe cada gasto
    for gasto in gastos:
        print(
            f"{gasto['id']:<5} "
            f"{gasto['nome']:<20} "
            f"{gasto['categoria']:<15} "
            f"R$ {gasto['valor']:>8.2f}"
        )

    print("-" * 50)
    print(f"{'Total de registros:':<35} {len(gastos)}")


def mostrar_total(gastos):
    """
    Calcula e exibe o valor total de todos os gastos.
    """
    print("\n💰  TOTAL GASTO")
    print("-" * 30)

    if not gastos:
        print("Nenhum gasto cadastrado ainda.")
        return

    total = sum(gasto["valor"] for gasto in gastos)

    print(f"Total de gastos: R$ {total:.2f}")
    print(f"Quantidade de itens: {len(gastos)}")


def filtrar_por_categoria(gastos):
    """
    Filtra e exibe os gastos de uma categoria específica.
    """
    print("\n🔍  FILTRAR POR CATEGORIA")
    print("-" * 30)

    if not gastos:
        print("Nenhum gasto cadastrado ainda.")
        return

    # Lista as categorias disponíveis (sem repetição)
    categorias = list(set(gasto["categoria"] for gasto in gastos))
    print("Categorias disponíveis:")
    for i, categoria in enumerate(categorias, start=1):
        print(f"  {i}. {categoria}")

    # Solicita a categoria para filtrar
    categoria_buscada = input("\nDigite a categoria desejada: ").strip().capitalize()

    # Filtra os gastos
    gastos_filtrados = [
        gasto for gasto in gastos
        if gasto["categoria"] == categoria_buscada
    ]

    if not gastos_filtrados:
        print(f"❌ Nenhum gasto encontrado na categoria '{categoria_buscada}'.")
        return

    # Exibe os gastos filtrados
    print(f"\n📂  Gastos na categoria: {categoria_buscada}")
    print("-" * 50)
    print(f"{'ID':<5} {'Nome':<20} {'Categoria':<15} {'Valor':>10}")
    print("-" * 50)

    for gasto in gastos_filtrados:
        print(
            f"{gasto['id']:<5} "
            f"{gasto['nome']:<20} "
            f"{gasto['categoria']:<15} "
            f"R$ {gasto['valor']:>8.2f}"
        )

    total_categoria = sum(gasto["valor"] for gasto in gastos_filtrados)
    print("-" * 50)
    print(f"Total em '{categoria_buscada}': R$ {total_categoria:.2f}")


def remover_gasto(gastos):
    """
    Remove um gasto da lista pelo ID.
    Salva automaticamente após remover.
    """
    print("\n🗑️   REMOVER GASTO")
    print("-" * 30)

    if not gastos:
        print("Nenhum gasto cadastrado ainda.")
        return

    # Mostra os gastos antes de remover
    listar_gastos(gastos)

    # Solicita o ID para remover
    try:
        id_remover = int(input("\nDigite o ID do gasto que deseja remover: "))
    except ValueError:
        print("❌ ID inválido! Digite um número inteiro.")
        return

    # Procura o gasto pelo ID
    gasto_encontrado = None
    for gasto in gastos:
        if gasto["id"] == id_remover:
            gasto_encontrado = gasto
            break

    if not gasto_encontrado:
        print(f"❌ Nenhum gasto encontrado com o ID {id_remover}.")
        return

    # Confirma a remoção
    confirmacao = input(
        f"Tem certeza que deseja remover '{gasto_encontrado['nome']}'? (s/n): "
    ).strip().lower()

    if confirmacao == "s":
        gastos.remove(gasto_encontrado)
        salvar_gastos(gastos)
        print(f"✅ Gasto '{gasto_encontrado['nome']}' removido com sucesso!")
    else:
        print("❌ Remoção cancelada.")

def exibir_menu():
    """
    Exibe o menu de opções no terminal.
    """
    print("\n" + "=" * 40)
    print("   💸  CONTROLE DE GASTOS  💸")
    print("=" * 40)
    print("  1. ➕  Adicionar gasto")
    print("  2. 📋  Listar todos os gastos")
    print("  3. 💰  Ver total gasto")
    print("  4. 🔍  Filtrar por categoria")
    print("  5. 🗑️   Remover um gasto")
    print("  6. 🚪  Sair")
    print("=" * 40)


def main():
    """
    Função principal que controla o fluxo do programa.
    """
    print("\n🚀 Bem-vindo ao Sistema de Controle de Gastos!")

    # Carrega os dados salvos ao iniciar
    gastos = carregar_gastos()

    if gastos:
        print(f"📂 {len(gastos)} gasto(s) carregado(s) do arquivo.")
    else:
        print("📂 Nenhum dado encontrado. Começando do zero!")

    # Loop principal do menu
    while True:
        exibir_menu()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_gasto(gastos)

        elif opcao == "2":
            listar_gastos(gastos)

        elif opcao == "3":
            mostrar_total(gastos)

        elif opcao == "4":
            filtrar_por_categoria(gastos)

        elif opcao == "5":
            remover_gasto(gastos)

        elif opcao == "6":
            print("\n👋 Até logo! Seus dados foram salvos.")
            break

        else:
            print("❌ Opção inválida! Digite um número de 1 a 6.")

if __name__ == "__main__":
    main()