import pandas as pd 
import json

with open("bancoDeDados.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.read_json("bancoDeDados.json")

loginAdm = data["bancoDeDados"]["login"]["adm"]
loginJogadora = data["bancoDeDados"]["login"]["jogadoras"]
time = data["bancoDeDados"]["time"]
jogos = data["bancoDeDados"]["jogos"]

loginAdmfeito = False
verificacaoCadastro = False
loginJogadorafeito = False

verificacao = input("Ja tem conta(responda com S/n): ")

# Sistema de login
def login() :
    for i in range(4):
        try: 
            if verificacao.lower() == "s" : 
                tipoConta = input('vai entrar como jogadora ou como admin: ')
                # login para jogadoras
                if tipoConta == 'jogadora': 
                    nomeJogador = input('digite seu nome de usuario: ').strip()
                    senhaJogador = input('digite sua senha: ')
                    if [nomeJogador,senhaJogador] in loginJogadora.values() :
                        print(f'seja bem vinda {nomeJogador}')
                        global loginJogadorafeito
                        loginJogadorafeito = True
                        break
                    elif i > 0 and i < 3: 
                        print('alguma coisa deu errado tente novamente!')
                    # recuperação de senha
                    elif i == 3 :
                        recuperacaoSenha = input('voce esqueceu a senha?(S/n) ')
                        if recuperacaoSenha.lower() == 's':
                            identificacao = input('digite seu nome: ')
                            confimacao = input('digite seu cpf:')
                            if identificacao in loginJogadora.keys() and confimacao == loginJogadora[identificacao][2][0]:
                                novaSenha = input('digite sua senha nova: ')
                                loginJogadora[identificacao][1] = novaSenha
                            else:
                                print('CPF incorreto ou voce nao tem conta.')
                    elif i == 4 :
                        print('numero maximo de tentativas, tente novamente mais tarde')     

                #login caso for administrador
                if tipoConta == 'admin':
                    for i in range(4):
                        nomeAdm = input('digite seu nome de usuario: ').strip()
                        senhaAdm = input('digite sua senha: ')
                        if [nomeAdm, senhaAdm] in loginAdm.values():
                            print(f'Seja bem vinda {nomeAdm}')
                            global loginAdmfeito
                            loginAdmfeito = True
                            return verificacaoAdm()
                        elif i == 3:
                            print('Passou do numero maximo de tentativas, tente mais tarde.')
                            break
                        if nomeAdm not in loginAdm or senhaAdm in loginAdm and i < 3:
                            print('nome de usuario ou senha errados, tente novamente.')
            # cadastro de jogadoras
            elif verificacao.lower() == 'n' :
                visitante = input('voce quer criar uma conta(S/n): ')
                if visitante.lower() == 's':
                    while verificacaoCadastro == False :
                        cadastroCpf = int(input('digite seu CPF(sem espaços): '))
                        cadastroNome = input('crie um nome de usuario: ')
                        cadastroIdade = int(input('digite quantos anos voce tem(digite apenas o numero): '))
                        cadastroSenha = input('crie sua senha (pelo menos 4 caracteres): ')
                        #validação de CPF, idade e senha dentro dos padroes de segurança da minha cabeça
                        if len(cadastroCpf) < 11 or cadastroIdade < 18 or len(cadastroSenha) < 4 :
                            print('algo deu errado no seu cadastro, tente novamente.')
                        elif cadastroNome in loginJogadora.keys(): 
                            print('o seu nome de usuario ja esta sendo usado.')
                        else :
                            loginJogadora[cadastroNome] = ([cadastroNome, cadastroSenha],[cadastroCpf,cadastroNome,cadastroIdade])
                            verificacaoCadastro = True
                else :
                    break       
        except IOError as e: 
            print(f'deu erro por conta disso: {e}')

# pagina exclusiva para admins
def verificacaoAdm():
    if loginAdmfeito == True:
        return menu()

#menu dos admins
def menu() :
    opcoes = {
        'camp': input('quer criar um campeonato? '),
        'cadastro times' : input('cadastrar times para um jogo? '),
        'remover times' : input("remover algum time? "),
        'atualizar times': input("atualizar algum time? "),
        'ver times': input("ver quais times tem em alguma copa? "),
        'botaoSair': input('coloque "sair" se quiser sair e "nao" para nao sair: ')
    }
    if opcoes['camp'] == 's' and loginAdmfeito == True: 
        cadastroCamp()
    if opcoes['cadastro times'] == 's' and loginAdmfeito == True:
        times()
    if opcoes['botaoSair'] == 's' and loginAdmfeito == True:
        sair()

# função de cadastro de campeonato, apenas para administradores
def cadastroCamp(): 
    confirma = input('confirme que você quer criar um campeonato(responda com S/n): ')
    if confirma.lower() == 's' : 
        nome = input('digite o nome do campeonato: ')
        #define nome, data, horario e local do campeonato
        data = input('digite o dia e o mês do evento(exemplo: 22/02/25): ')
        horario = input('digite o horario do campeonato: ')
        local = input('digite o local do campeonato: ')
        jogos[nome] = [data,horario,local]
        print('Jogo criado com sucesso!')
        voltarMenu = input('voce quer voltar ao menu(S/n)? ')
    if voltarMenu.lower() == 's': 
        menu()
    else :
        print('ok, ate logo!')

#cadastro de times para um campeonato
def times(): 
    #o campeonato ja precisa existir
    nomeDocamp = input('coloque o nome do campeonato aqui: ')
    nomeTime = input('digite o nome do time: ')
    time[nomeTime] = []
    time[nomeTime].append(nomeTime)
    jogadoras = []
    for i in range(3):
        jogadora = input(f'digite o nome da jogadora {i + 1}: ')
        jogadoras.append(jogadora)
    time[nomeTime].append(jogadoras)
    jogos[nomeDocamp] += time[nomeTime]
    print(jogos)
    print("time cadastrado com sucesso!")
    voltarMenu = input('voce quer voltar ao menu(S/n)? ')
    if voltarMenu.lower() == 's' :
        menu()
    else :
        print('ok, ate logo!')
    
def sair():
    pass

login()
 
jg = pd.DataFrame(jogos)
print(jg)