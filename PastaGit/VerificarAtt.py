import os
import datetime as dt
import time
import warnings
import Caminhos
warnings.simplefilter("ignore")

# Caminho pastas versao antiga
caminhoSVA_GGE = Caminhos.sva_GGE
caminhoSVA_GERT = Caminhos.sva_GERT
caminhoRevisao_GERT = Caminhos.Revisao_GERT
caminhoRevisao_GGE = Caminhos.Revisao_GGE
caminhoNF_GGE = Caminhos.nf_GGE

# Arquivos pastas
lista_status_SVA_GGE = os.listdir(caminhoSVA_GGE)
lista_status_SVA_GERT = os.listdir(caminhoSVA_GERT)
lista_status_Revisao_GGE = os.listdir(caminhoRevisao_GGE)
lista_status_Revisao_GERT = os.listdir(caminhoRevisao_GERT)
lista_status_NF_GGE = os.listdir(caminhoNF_GGE) # Talvez não necessite ser utilizado

# Compara as pastas
lista_REVS = [elemento for elemento in lista_status_Revisao_GGE if elemento in lista_status_Revisao_GERT]
lista_SVAS = [elemento for elemento in lista_status_SVA_GGE if elemento in lista_status_SVA_GERT]

# Retorna a data atual no formato padrão ISO 8601 
def DataHoje(param = 0) : 
    if param == "dt": # Retorna a data em formato de datetime
        data = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return data
    else: # Retorna data em formato string  
        data = dt.date.today()  
        dataFormatada = data.strftime('%d-%m-%Y')
        return dataFormatada

# Retorna a última alteração da Revisão de Custos
def VerificaAlteracaoRevisao(param = 0) :
    atualizadostr = "01/01/1900" # Deixando uma data inicial para loop de data maior
    atualizado = time.strptime(atualizadostr, '%d/%m/%Y') # Transformando formato string em data
    links = []
    for arquivo in lista_status_Revisao_GGE:
        if "TLB_RelExec" in arquivo:
            link = f"{caminhoRevisao_GGE}/{arquivo}"
            data = pegaredata(link)
            links.append(f"{caminhoRevisao_GGE}/{arquivo}") # Armazenando arquivos com com nomes especificados dentro de um array
            if data > atualizado: # Se o arquivo estiver modificado na data de hoje ele se torna o principal arquivo da lista
                atualizado = data
                linkNovo = link # Link do arquivo mais atualizado
                nomeArquivo  = arquivo # Arquivo mais atualizado
    
        # Quantidade de arquivos status na lista          
        quantidadeArquivo = len(links)
        
    if quantidadeArquivo == 0: # Verifica se tem alguma arquivo de status na pasta, !Necessário para evitar erro de variaveis vazias pós loop!
        er = "Não foi encontado arquivo de status no projeto selecionado!"
        return er
    else:    
        # Somente formato data e hora completo, dificuldade de implementar        
        T_stamp = time.strftime("%d-%m-%Y ás %H:%M:%S", atualizado) # Manipula o formato de time do arquivo em data e hora em formato padrão de texto para o "print"
        T_dmy = time.strftime("%d/%m/%Y", atualizado) # Transforma para um formato de string que a função somentedata aceita como entrada para execução (especificação da biblioteca)
        
        dtime = somentedata(T_dmy)

        if param == "GetHoje":
            return dtime
        else:
            Alteracao = f"O {nomeArquivo} foi modificado pela última vez em {T_stamp}"
            return Alteracao
    
# Retorna o resultado da consulta se o status do projeto está atualizado
def StatusAtualizadoCustos():
    DataCusto = VerificaAlteracaoRevisao("GetHoje")
    Historico = VerificaAlteracaoRevisao()
    data = DataHoje("dt")
    if DataCusto == data:
        print(f"Houve uma atualização hoje do status de Revisão de Sistemas de Custo!\n{Historico}")
    else:
        print(f"Não houve uma atualização no dia de hoje do Revisão de Sistemas de custo!\n{Historico}")

# Função recursiva para capturar datas dos arquivos    
def pegaredata(link):
    ti_m = os.path.getmtime(link)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti)
    
    return t_obj

# Função que transforma uma string dd/mm/yyyy em datetime com objetivo de operações com datas
def somentedata(a):
    data = dt.datetime.strptime(a, "%d/%m/%Y").replace(hour=0, minute=0, second=0, microsecond=0) # Retorna Data(string) em formato de datetime 
    return data
    
###################################
# Sessão do site
###################################

# Função para obter os links/caminhos atualizados dos projetos solicitados
def arquivos_site(param):
    if param == 1: # Revisão
        ppt = ppt_att_site(1)
        pdf = attpdf(1, ppt)
        return ppt, pdf
    elif param == 2: # SVA
        ppt = ppt_att_site(2)
        pdf = attpdf(2, ppt)
        return ppt, pdf
    elif param ==3: # NFCom
        ppt = ppt_att_site(3)  
        pdf = attpdf(3, ppt)
        return ppt, pdf  
    else:
        print("!Parâmetro Incorreto!")
        return

# Função que retorna o nome do arquivo mais atualizado das pastas GERT E GGE
def ppt_att_site(param):
    if param == 1:    
        atualizadostr = "01/01/1900" # Deixando uma data inicial para loop de data maior
        atualizadoGGE = time.strptime(atualizadostr, '%d/%m/%Y') # Transformando formato string em data
        atualizadoGERT = time.strptime(atualizadostr, '%d/%m/%Y') # Transformando formato string em data
        listalenGGE = []
        listalenGERT = []
        
        for arquivo in lista_status_Revisao_GGE:
            if "TLB_RelExec" in arquivo and ".pptx" in arquivo:
                link = f"{caminhoRevisao_GGE}/{arquivo}"
                data_rev_GGE = DataReturn(link)
                listalenGGE.append(link)
                if data_rev_GGE > atualizadoGGE: # Se o arquivo tiver modificado na data de hoje ele se torna o principal arquivo da lista
                    atualizadoGGE = data_rev_GGE
                    linkNovoGGE = link # Link do arquivo mais atualizado
                    nomeArquivoGGE  = arquivo # Arquivo mais atualizado
                     
        for arquivo in lista_status_Revisao_GERT:
            if "TLB_RelExec" in arquivo and ".pptx" in arquivo:
                link = f"{caminhoRevisao_GERT}/{arquivo}"
                data_rev_GERT = DataReturn(link)
                listalenGERT.append(link)
                if data_rev_GERT > atualizadoGERT: # Se o arquivo tiver modificado na data de hoje ele se torna o principal arquivo da lista
                    atualizadoGERT = data_rev_GERT
                    linkNovoGERT = link # Link do arquivo mais atualizado
                    nomeArquivoGERT  = arquivo # Arquivo mais atualizado

        QtdGGE = len(listalenGGE)
        QtdGERT = len(listalenGERT)

        if QtdGGE == 0 and QtdGERT == 0:
            print("Não existe arquivos de status ppt nas pastas")
            return
        elif QtdGGE == 0:
            return linkNovoGERT
        elif QtdGERT == 0:
            return linkNovoGGE
        else:        
            if atualizadoGGE > atualizadoGERT:
                return  linkNovoGGE
            elif atualizadoGGE < atualizadoGERT:
                return linkNovoGERT
            else:
                return linkNovoGGE

# Atualiza arquivos status em PDF
def attpdf(param, gerencia):
    if param == 1:
        if "GGE" in gerencia:
            listalen = [] 
            for arquivo in lista_status_Revisao_GGE:
                if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                    listalen.append(f'{arquivo}')
                    
                QtdPdf = len(listalen)
                
            if QtdPdf == 0:
                print('Não há arquivo PDF para ser atualizado')
                return
            elif QtdPdf == 1:
                for arquivo in lista_status_Revisao_GGE:
                    if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                        pdfAtualizado = f"{caminhoRevisao_GGE}/{arquivo}"
                        linkPdf = pdfAtualizado
                        return linkPdf
            elif QtdPdf > 1:
                atualizadostr = "01/01/1900" # Deixando uma data inicial para loop de data maior
                atualizado = time.strptime(atualizadostr, '%d/%m/%Y') # Transformando formato string em data
                
                for arquivo in lista_status_Revisao_GGE:
                    if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                        pdf = f"{caminhoRevisao_GGE}/{arquivo}"
                        DataPdf = DataReturn(pdf)
                        if DataPdf > atualizado: # Se o arquivo tiver modificado na data de hoje ele se torna o principal arquivo da lista
                            atualizado = DataPdf
                            linkPdf = pdf # Link do arquivo mais atualizado
                            nomearquivopdf = arquivo
                
                return linkPdf
                
        elif "GERT" in gerencia:
            listalen = [] 
            for arquivo in lista_status_Revisao_GERT:
                if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                    listalen.append(f'{arquivo}')
                    
                QtdPdf = len(listalen)
                
            if QtdPdf == 0:
                print('Não há arquivo PDF para ser atualizado')
                return
            elif QtdPdf == 1:
                for arquivo in lista_status_Revisao_GERT:
                    if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                        pdfAtualizado = f"{caminhoRevisao_GERT}/{arquivo}"
                        linkPdf = pdfAtualizado
                        return linkPdf
            elif QtdPdf > 1:
                atualizadostr = "01/01/1900" # Deixando uma data inicial para loop de data maior
                atualizado = time.strptime(atualizadostr, '%d/%m/%Y') # Transformando formato string em data
                
                for arquivo in lista_status_Revisao_GERT:
                    if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                        pdf = f"{caminhoRevisao_GERT}/{arquivo}"
                        DataPdf = DataReturn(pdf)
                        if DataPdf > atualizado: # Se o arquivo tiver modificado na data de hoje ele se torna o principal arquivo da lista
                            atualizado = DataPdf
                            linkPdf = pdf # Link do arquivo mais atualizado
                            nomearquivopdf = arquivo
                 
                return linkPdf

# Retorna informação de data de alteração do arquivo(data e time)    
def DataReturn(url):
    ti_m = os.path.getmtime(url)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti)

    return t_obj