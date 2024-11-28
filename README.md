# Python-Sharepoint-Integration
Solução Python X sharepoint utilizando biblioteca Office365-REST-Python-Client

# Projeto de Sincronização e Publicação no SharePoint

Este projeto foi desenvolvido durante um estágio de 1 ano na **Telebras** para gerenciar e automatizar a atualização, organização e publicação de arquivos em um contexto corporativo.

## Requisitos

O projeto necessita da biblioteca `Office365-REST-Python-Client` versão 2.5.13. Instale-a com o comando:

```bash
pip install Office365-REST-Python-Client
```

## Arquivos do Projeto

- **`AtualizarPastas.py`**  
  Atualiza os arquivos do projeto nas pastas do sistema. Arquivos mais recentes ficam destacados no diretório principal, enquanto os antigos são movidos para uma pasta de backup organizada.

- **`VerificarAtt.py`**  
  Verifica atualizações no projeto, identificando arquivos novos ou modificados.

- **`Caminhos.py`**  
  Define os caminhos do sistema, incluindo diretórios locais e URLs do SharePoint.

- **`PostarSite.py`**  
  Publica os arquivos atualizados no site corporativo no SharePoint.

- **`Executor.py`**  
  Orquestra a execução de todos os scripts do projeto.

## Contexto do Projeto

Foi utilizado como exemplo um **projeto de Revisão de Sistema de Custos** que conta com dois diretórios:  

1. **Principal (GGE):** Onde os arquivos mais recentes e organizados são armazenados.  
2. **Backup (GERT):** Mantido sincronizado com o diretório principal para segurança e redundância.  

A publicação de atualizações no **SharePoint** ocorre por meio de arquivos de **status report**, que informam a equipe sobre mudanças no projeto.
