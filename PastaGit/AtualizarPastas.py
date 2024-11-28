import os
import time
import shutil
import warnings
import Caminhos
from pathlib import Path
warnings.simplefilter("ignore")

# Caminho pastas versao antiga
caminhoRevisao_GERT = Caminhos.projeto_C_revisao
caminhoRevisao_GGE = Caminhos.projeto_D_revisao

# Arquivos pastas
lista_status_Revisao_GGE = os.listdir(caminhoRevisao_GGE)
lista_status_Revisao_GERT = os.listdir(caminhoRevisao_GERT)

# Compara as pastas
lista_REVS = [elemento for elemento in lista_status_Revisao_GGE if elemento in lista_status_Revisao_GERT]

# Verificar se as pastas estão atualizadas
def VerificaStatus(lista = 0):
    if lista == 1: # Revisão
        ArquivoNovo = nome_att(1) # Nome do arquivo com a data mais recente entre GGE e GERT
        for arquivo in lista_REVS:
            if ArquivoNovo in arquivo:
                print({arquivo})
                print("Os status das pastas de Revisão estão atualizados!")
                organizarStatus('REVGERT')
                organizarStatus('REVGGE')
                organizarStatuspdf('REVGERT')
                organizarStatuspdf('REVGGE')
                return 
            else :
                print({arquivo})
        
        print("Atualizando Revisão de Custos...")        
        CopiarArquivoRevisao()
        print("Atualização concluída")

# Copiar arquivo mais atualizado de Revisao de Custos e sincronizar pastas        
def CopiarArquivoRevisao():
    ArquivoAtualizado = VerificaAlteracao(1)
    if 'GGE' in ArquivoAtualizado:
        organizarStatus('REVGGE')
        copiarOldRevisaoStatus(1)
        shutil.copy2(ArquivoAtualizado, caminhoRevisao_GERT)
        attpdf(1)
    else:
        organizarStatus('REVGERT')
        copiarOldRevisaoStatus(2)
        shutil.copy2(ArquivoAtualizado, caminhoRevisao_GGE)
        attpdf(2)    

# Atualiza arquivos status em PDF
def attpdf(param):
    if param == 1:
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
                    shutil.copy2(pdfAtualizado, caminhoRevisao_GERT)
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
            
            # Copia arquivo PDF mais atualizado para a pasta GERT            
            shutil.copy2(linkPdf, caminhoRevisao_GERT)  
            
            # Loop para colocar pdf desatualizados na pasta old
            for arquivo in listalen:
                if nomearquivopdf in arquivo:
                    continue
                else:
                    oldstatus = Path(f"{caminhoRevisao_GGE}/Old/{arquivo}")
                    origem = f"{caminhoRevisao_GGE}/{arquivo}" 
                    destino = f"{caminhoRevisao_GGE}/Old" 
                    if oldstatus.exists():
                        os.remove(oldstatus)
                        shutil.move(origem, destino)
                    else:
                        shutil.move(origem, destino)  
                
    elif param == 2:
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
                    shutil.copy2(pdfAtualizado, caminhoRevisao_GGE)
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
            
            # Copia arquivo PDF mais atualizado para a pasta GERT            
            shutil.copy2(linkPdf, caminhoRevisao_GGE)
            
            # Loop para colocar pdf desatualizados na pasta old
            for arquivo in listalen:
                if nomearquivopdf in arquivo:
                    continue
                else:
                    oldstatus = Path(f"{caminhoRevisao_GERT}/Old/{arquivo}")
                    origem = f"{caminhoRevisao_GERT}/{arquivo}" 
                    destino = f"{caminhoRevisao_GERT}/Old" 
                    if oldstatus.exists():
                        os.remove(oldstatus)
                        shutil.move(origem, destino)
                    else:
                        shutil.move(origem, destino)  

# Função que retorna o nome do arquivo mais atualizado das pastas GERT E GGE
def nome_att(param):
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
            return nomeArquivoGERT
        elif QtdGERT == 0:
            return nomeArquivoGGE
        else:        
            if atualizadoGGE > atualizadoGERT:
                return  nomeArquivoGGE
            elif atualizadoGGE < atualizadoGERT:
                return nomeArquivoGERT
            else:
                return nomeArquivoGGE
 
# Verificar qual arquivo está mais atualizado entre GGE E GERT               
def VerificaAlteracao(param) :
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
                    nomeArquivo  = arquivo # Arquivo mais atualizado
                     
        for arquivo in lista_status_Revisao_GERT:
            if "TLB_RelExec" in arquivo and ".pptx" in arquivo:
                link = f"{caminhoRevisao_GERT}/{arquivo}"
                data_rev_GERT = DataReturn(link)
                listalenGERT.append(link)
                if data_rev_GERT > atualizadoGERT: # Se o arquivo tiver modificado na data de hoje ele se torna o principal arquivo da lista
                    atualizadoGERT = data_rev_GERT
                    linkNovoGERT = link # Link do arquivo mais atualizado
                    nomeArquivo  = arquivo # Arquivo mais atualizado

        QtdGGE = len(listalenGGE)
        QtdGERT = len(listalenGERT)

        if QtdGGE == 0:
            return linkNovoGERT
        elif QtdGERT == 0:
            return linkNovoGGE
        else:        
            if atualizadoGGE > atualizadoGERT:
                return  linkNovoGGE
            elif atualizadoGGE < atualizadoGERT:
                return linkNovoGERT
            else:
                return "Os arquivos são iguais" # Verificar se é útil, já que se eles são iguais a função não chega a ser chamada
                         
# Retorna informação de data de alteração do arquivo(data e time)    
def DataReturn(url):
    ti_m = os.path.getmtime(url)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti)

    return t_obj

# Organiza a pasta caso tenha vários ppt em uma só pasta, deixando somente a mais atualizada
def organizarStatus(param):
    if param == 'REVGGE':
        Atualizadoname = nome_att(1)
        for arquivo in lista_status_Revisao_GGE:
            if Atualizadoname in arquivo:
                continue
            else:
                if "TLB_RelExec" in arquivo and ".pptx" in arquivo :
                    origem = f"{caminhoRevisao_GGE}/{arquivo}" 
                    destino = f"{caminhoRevisao_GGE}/Old" 
                    oldstatus = Path(f"{caminhoRevisao_GGE}/Old/{arquivo}")
                    if oldstatus.exists():
                        os.remove(oldstatus)
                        shutil.move(origem, destino)
                    else:
                        shutil.move(origem, destino)
    
    elif param == 'REVGERT':
        Atualizadoname = nome_att(1)
        for arquivo in lista_status_Revisao_GERT:
            if Atualizadoname in arquivo:
                continue
            else:
                if "TLB_RelExec" in arquivo and ".pptx" in arquivo :
                    origem = f"{caminhoRevisao_GERT}/{arquivo}" 
                    destino = f"{caminhoRevisao_GERT}/Old" 
                    oldstatus = Path(f"{caminhoRevisao_GERT}/Old/{arquivo}")
                    if oldstatus.exists():
                        os.remove(oldstatus)
                        shutil.move(origem, destino)
                    else:
                        shutil.move(origem, destino)

# Organiza a pasta caso tenha vários pdf em uma só pasta, deixando somente a mais atualizada, função utilizada somente com pastas atualizadas para evitar duplicação
def organizarStatuspdf(param):
    if param == 'REVGGE':
        listalen = [] 
        for arquivo in lista_status_Revisao_GGE:
            if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                listalen.append(f'{arquivo}')
                
            QtdPdf = len(listalen)
            
        if QtdPdf > 1:
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
                
                # Loop para colocar pdf desatualizados na pasta old
                for arquivo in listalen:
                    if nomearquivopdf in arquivo:
                        continue
                    else:
                        oldstatus = Path(f"{caminhoRevisao_GGE}/Old/{arquivo}")
                        origem = f"{caminhoRevisao_GGE}/{arquivo}" 
                        destino = f"{caminhoRevisao_GGE}/Old" 
                        if oldstatus.exists():
                            os.remove(oldstatus)
                            shutil.move(origem, destino)
                        else:
                            shutil.move(origem, destino)  
        else:
            return
        
    elif param == 'REVGERT':
        listalen = [] 
        for arquivo in lista_status_Revisao_GERT:
            if "TLB_RelExec" in arquivo and ".pdf" in arquivo:
                listalen.append(f'{arquivo}')
                
            QtdPdf = len(listalen)
            
        if QtdPdf > 1:
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
                
                # Loop para colocar pdf desatualizados na pasta old
                for arquivo in listalen:
                    if nomearquivopdf in arquivo:
                        continue
                    else:
                        oldstatus = Path(f"{caminhoRevisao_GERT}/Old/{arquivo}")
                        origem = f"{caminhoRevisao_GERT}/{arquivo}" 
                        destino = f"{caminhoRevisao_GERT}/Old" 
                        if oldstatus.exists():
                            os.remove(oldstatus)
                            shutil.move(origem, destino)
                        else:
                            shutil.move(origem, destino)  
        else:
            return

# Copia os arquivos da pasta desatualizada para a pasta Old _Backup
def copiarOldRevisaoStatus(param):
    if param == 1:
        for arquivo in lista_status_Revisao_GERT:
            if "TLB_RelExec" in arquivo:
                origem = f"{caminhoRevisao_GERT}/{arquivo}" 
                destino = f"{caminhoRevisao_GERT}/Old" 
                oldstatus = Path(f"{caminhoRevisao_GERT}/Old/{arquivo}")
                if oldstatus.exists():
                    os.remove(oldstatus)
                    shutil.move(origem, destino)
                else:
                    shutil.move(origem, destino)
    
    if param == 2:
        for arquivo in lista_status_Revisao_GGE:
            if "TLB_RelExec" in arquivo:
                origem = f"{caminhoRevisao_GGE}/{arquivo}" 
                destino = f"{caminhoRevisao_GGE}/Old" 
                oldstatus = Path(f"{caminhoRevisao_GGE}/Old/{arquivo}")
                if oldstatus.exists():
                    os.remove(oldstatus)
                    shutil.move(origem, destino)
                else:
                    shutil.move(origem, destino)
