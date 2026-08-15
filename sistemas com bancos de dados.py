import sqlite3

def conectar_banco():
    """Cria a conexão com o banco de dados SQLite local."""
    conn = sqlite3.connect("sistema_estoque.db")
    cursor = conn.cursor()
    # Criação da tabela com comandos SQL nativos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conn.commit()
    return conn

def cadastrar_produto(conn):
    print("\n--- Cadastrar Produto ---")
    nome = input("Nome do produto: ")
    preco = float(input("Preço (R$): "))
    quantidade = int(input("Quantidade em estoque: "))

    cursor = conn.cursor()
    # Uso de Query Parametrizada para evitar SQL Injection
    cursor.execute(
        "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
        (nome, preco, quantidade)
    )
    conn.commit()
    print("✅ Produto cadastrado com sucesso!")

def listar_produtos(conn):
    print("\n--- Lista de Produtos ---")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print(f"{'ID':<5} | {'Nome':<20} | {'Preço (R$)':<10} | {'Estoque':<8}")
    print("-" * 50)
    for p in produtos:
        print(f"{p[0]:<5} | {p[1]:<20} | R$ {p[2]:<8.2f} | {p[3]:<8}")

def atualizar_produto(conn):
    listar_produtos(conn)
    print("\n--- Atualizar Produto ---")
    id_prod = int(input("Digite o ID do produto que deseja atualizar: "))
    novo_preco = float(input("Novo preço (R$): "))
    nova_qtd = int(input("Nova quantidade: "))

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produtos SET preco = ?, quantidade = ? WHERE id = ?",
        (novo_preco, nova_qtd, id_prod)
    )
    conn.commit()
    print("✅ Produto atualizado com sucesso!")

def deletar_produto(conn):
    listar_produtos(conn)
    print("\n--- Excluir Produto ---")
    id_prod = int(input("Digite o ID do produto que deseja excluir: "))

    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_prod,))
    conn.commit()
    print("❌ Produto excluído com sucesso!")

def main():
    conn = conectar_banco()

    while True:
        print("\n=================================")
        print("  SISTEMA DE ESTOQUE (SQL + PYTHON)")
        print("=================================")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Excluir Produto")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_produto(conn)
        elif opcao == '2':
            listar_produtos(conn)
        elif opcao == '3':
            atualizar_produto(conn)
        elif opcao == '4':
            deletar_produto(conn)
        elif opcao == '5':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

    conn.close()

if __name__ == "__main__":
    main()