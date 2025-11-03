import pandas as pd
import os

# Caminhos dos arquivos CSV
CAMINHO_JOGADORAS = "jogadoras.csv"
CAMINHO_ADMS = "admins.csv"
CAMINHO_JOGOS = "jogos.csv"

# Carregar dados ou criar caso não exista
def carregar_csv(caminho, colunas):
    if os.path.exists(caminho):
        df = pd.read_csv(caminho, index_col=0)
        # Garantir que todas as colunas existam
        for col in colunas:
            if col not in df.columns:
                df[col] = ""
        return df
    else:
        return pd.DataFrame(columns=colunas)

# Inicializando dados
df_jogadoras = carregar_csv(CAMINHO_JOGADORAS, ["nome", "senha", "cpf", "idade"])
df_admins = carregar_csv(CAMINHO_ADMS, ["nome", "senha"])
df_jogos = carregar_csv(CAMINHO_JOGOS, ["campeonato", "data", "horario", "local", "times", "placar"])

# Exemplo de admins iniciais
if df_admins.empty:
    df_admins = pd.DataFrame([["adm","senha"], ["vitor","160507"]], columns=["nome","senha"])
    df_admins.to_csv(CAMINHO_ADMS)

# Função de login de jogadora
def login_jogadora():
    nome = input("Nome da jogadora: ").strip()
    senha = input("Senha: ").strip()
    jogador = df_jogadoras[(df_jogadoras['nome'] == nome) & (df_jogadoras['senha'] == senha)]
    if not jogador.empty:
        print(f"Seja bem-vinda {nome}")
        return True
    else:
        print("❌ Usuário ou senha incorretos.")
        return False

# Função de login de administrador
def login_admin():
    nome = input("Usuário ADM: ").strip()
    senha = input("Senha: ").strip()
    admin = df_admins[(df_admins['nome'] == nome) & (df_admins['senha'] == senha)]
    if not admin.empty:
        print(f"Seja bem-vinda {nome}")
        menu_admin()
        return True
    else:
        print("❌ Usuário ou senha incorretos.")
        return False

# Função de cadastro de jogadora
def cadastrar_jogadora():
    global df_jogadoras
    nome = input("Crie um nome de usuário: ").strip()
    if nome in df_jogadoras['nome'].values:
        print("Nome de usuário já existe!")
        return
    senha = input("Crie uma senha (min. 4 caracteres): ").strip()
    if len(senha) < 4:
        print("Senha muito curta!")
        return
    cpf = input("Digite seu CPF: ").strip()
    idade = int(input("Digite sua idade: "))
    if idade < 18:
        print("Você precisa ter 18 anos ou mais!")
        return
    # Adiciona jogadora
    df_jogadoras.loc[len(df_jogadoras)] = [nome, senha, cpf, idade]
    df_jogadoras.to_csv(CAMINHO_JOGADORAS, index=False)
    print("Cadastro realizado com sucesso!")

# Menu do administrador
def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1 - Criar campeonato")
        print("2 - Cadastrar times")
        print("3 - Lançar placar de jogo")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            criar_campeonato()
        elif opcao == "2":
            cadastrar_times()
        elif opcao == "3":
            lancar_placar()
        elif opcao == "4":
            break
        else:
            print("Opção inválida!")

# Função criar campeonato
def criar_campeonato():
    global df_jogos
    nome = input("Nome do campeonato: ").strip()
    data = input("Data (DD/MM/AAAA): ").strip()
    horario = input("Horário: ").strip()
    local = input("Local: ").strip()
    # Adiciona linha com todas as colunas
    df_jogos.loc[len(df_jogos)] = [nome, data, horario, local, "", ""]
    df_jogos.to_csv(CAMINHO_JOGOS, index=False)
    print("Campeonato criado!")

# Função cadastrar times
def cadastrar_times():
    global df_jogos
    campeonato = input("Nome do campeonato: ").strip()
    if campeonato not in df_jogos['campeonato'].values:
        print("Campeonato não encontrado!")
        return
    times = input("Digite os nomes dos times (separados por vírgula): ")
    df_jogos.loc[df_jogos['campeonato'] == campeonato, 'times'] = times
    df_jogos.to_csv(CAMINHO_JOGOS, index=False)
    print("Times cadastrados!")

# Função lançar placar (simples)
def lancar_placar():
    global df_jogos
    campeonato = input("Nome do campeonato: ").strip()
    if campeonato not in df_jogos['campeonato'].values:
        print("Campeonato não encontrado!")
        return
    placar = input("Digite o placar (ex: 2x1): ").strip()
    df_jogos.loc[df_jogos['campeonato'] == campeonato, 'placar'] = placar
    df_jogos.to_csv(CAMINHO_JOGOS, index=False)
    print("Placar lançado!")

# Menu principal
def menu_principal():
    while True:
        print("\n=== SISTEMA DE FUTEBOL FEMININO ===")
        print("1 - Login jogadora")
        print("2 - Login administradora")
        print("3 - Cadastrar jogadora")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            login_jogadora()
        elif opcao == "2":
            login_admin()
        elif opcao == "3":
            cadastrar_jogadora()
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

# Inicia programa
menu_principal()
