import AtualizarPastas as at
import VerificarAtt as vt
import PostarSite as site
import os

# Função para execução dos arquivos e funções python, com entrada e saída de valores
def executor():
            
    while True:
        try:
            opcoes = ("Selecione uma opção válida: \n"
                    "1) Verificar Atualizações Revisão de Custos\n"
                    "2) Atualizar Pastas Status Revisão\n"
                    "3) Publicar Status\n"
                    "4) Encerrar Operação\n")
            case = int(input(f"\n{opcoes}\nDigite a Opção Desejada: "))
            if 1 <= case <= 7:
                os.system("cls")
                conectivo(case)
                input("\nPrecione enter para continuar e retornar ao menu principal ")
                os.system("cls")
            elif case == 8:
                print("Operação encerrada! \nTenha um bom dia!")
                break
            else:
                input("Escolha uma opção válida!\nPrecione enter para continuar ")
                os.system("cls")
        except ValueError:
            input("Informe apenas valores numéricos...\nPrecione enter para continuar ")
            os.system("cls")
      
# Função para Verificação da seleção do meu e chamar as funções da calculadora
def conectivo(opcao):
    match opcao:
        
        case 1:
            os.system('cls')
            vt.StatusAtualizadoCustos()
        case 2:
            os.system('cls')
            at.VerificaStatus(1)
        case 3:
            while True:

                try:
                    print("Selecione uma opção válida: \n"
                    "1) Publicar status Revisão de Custos\n"
                    "2) Cancelar\n")
                    opcao = int(input("Digite a opção desejada: "))

                    if 1:
                        os.system("cls")
                        if opcao == 1:
                            print("Publicando status report...\n")
                            site.postarAtt(1)
                            break
                        elif opcao == 2:
                            break
                            
                    else:
                        input("Escolha uma opção válida!\nPrecione enter para continuar ")
                        os.system("cls")
                except ValueError: # Se for inserido algo diferente de um número
                    input("Informe apenas valores numéricos...\nPrecione enter para continuar ")
                    os.system("cls")

executor()