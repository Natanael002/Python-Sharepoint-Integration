from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
from office365.sharepoint.webs.web import Web
from office365.sharepoint.files.move_operations import MoveOperations
import Caminhos
import VerificarAtt as vatt
import os

# Configurações do SharePoint
test_url = Caminhos.test_url
sva_url = Caminhos.sva_url
revisao_url =Caminhos.revisao_url
nf_url = Caminhos.nf_url

# client_id = "seu_client_id" Versão azure, paga, porém mais segura
# client_secret = "seu_client_secret"

# Email e senha do usuário "Proprietário" 
username = "email@gmail.com.br"
password = "12345678"

# # Autenticação no SharePoint +Azure
# credentials = ClientCredential(client_id, client_secret)
# ctx = ClientContext(sharepoint_url).with_credentials(credentials)

# Função que dispara os comandos para atualização do site
def postarAtt(projeto):
    
    if projeto == 1: # Revisao
        
        # Autenticação no SharePoint Tradicional 
        ctx = ClientContext(revisao_url).with_credentials(UserCredential(username, password))
        
        # Caminho completo da pasta e subpasta no SharePoint
        document_library = Caminhos.document_library_revisao
        subfolder_path = Caminhos.subfolder_path_revisao
        target_folder_url = f"{document_library}/{subfolder_path}"
        
        # Obter Arquivos na nuvem 
        ppt, pdf = vatt.arquivos_site(1)
        file_name_ppt = os.path.basename(ppt)
        file_name_pdf = os.path.basename(pdf)
        
        # Upload do arquivo PPT
        if exist_file(target_folder_url, file_name_ppt, ctx) == True:
            print(f"O arquivo {file_name_ppt} já esta no site!")
        else: 
            status_old(ctx, target_folder_url, file_name_ppt)
            target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
            with open(ppt, 'rb') as content_file:
                file_content = content_file.read()
            target_file = target_folder.upload_file(file_name_ppt, file_content).execute_query()

        # Upload do arquivo PDF, True = o arquivo ja esta no site
        if exist_file(target_folder_url, file_name_pdf, ctx) == True:
            print(f"O arquivo {file_name_pdf} já esta no site!")
        else: 
            status_old(ctx, target_folder_url, file_name_ppt) # O primeiro status ja limpa toda a pasta
            target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
            with open(pdf, 'rb') as content_file:
                file_content = content_file.read()
            target_file = target_folder.upload_file(file_name_pdf, file_content).execute_query()
            
        
        # Gerar o link do arquivo
        file_url = f"{revisao_url}/{document_library}/{subfolder_path}/{file_name_ppt}"
        file_url2 = f"{revisao_url}/{document_library}/{subfolder_path}/{file_name_pdf}"

        print(f"Link do PPT {file_url}\nLink do PDF {file_url2}")
        
# Função para verificar se já existe o arquivo no site, testar implementação de ver qual é mais atualizado
def exist_file(caminho, file, ctx):
    file_url = f"{caminho}/{file}"
    file = try_get_file(ctx.web, file_url)
    if file is None:
        return False
    else: # caso exista o arquivo com o mesmo nome 
        return True
        
# Função que move arquivos antigos para a pasta old
def mover_old(ctx, file, caminho):
        file_from = ctx.web.get_file_by_server_relative_path(file)
        folder_to = ctx.web.get_folder_by_server_relative_url(f"{caminho}/old")
        file_to = file_from.move_to_using_path(
        folder_to, MoveOperations.overwrite
        ).execute_query()
        print("'{0}' movido para pasta Old".format(file_from, folder_to))
        
# Função para jogar arquivos antigos para a pasta old
def status_old(ctx, folder, nameatt):
    arquivos = []
    root_folder = ctx.web.get_folder_by_server_relative_path(folder)
    files = root_folder.get_files(False).execute_query() # Se 'get_files' estiver como True, também vai verificar as subpastas
    
    nameattExt = os.path.splitext(nameatt)[0]  # Remove a extensão do arquivo
    
    for f in files:
        arquivos.append(f'{f.serverRelativeUrl}') # Adicionando o arquivo com o caminho relativo para a lista
        # print(f.serverRelativeUrl) Para pegar o caminho relativo do arquivo no site
    
    for status in arquivos:
        semExt = os.path.splitext(os.path.basename(status))[0] # Tirar extensão e caminho porquê só necessita o nome do arquivo
        if "TLB_RelExec" in semExt and semExt != nameattExt: # Verificar possibilidade de se o nome do arquivo ja estiver no site msm depois de postada ele nao ser movido
            mover_old(ctx, status, folder)
        else:
            continue
        
# Função que procura o arquivo e retorna resultado
def try_get_file(web, url):
    # type: (Web, str) -> Optional[File]
    try:
        return web.get_file_by_server_relative_url(url).get().execute_query()
    except ClientRequestException as e:
        if e.response.status_code == 404:
            return None
        else:
            raise ValueError(e.response.text)
