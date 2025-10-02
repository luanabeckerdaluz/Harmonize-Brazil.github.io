# Documentação

## Build da documentação

**1)** Para realizar o build, é necessário que alguns pacotes do sphinx estejam instalados. Abaixo, iremos criar um ambiente conda chamado **sphinx** com os pacotes necessários:

```bash
> conda create -c conda-forge \
               --yes \
               --name sphinx \
               python=3.11 \
               sphinx \
               IPython \
               cloud_sptheme \
               sphinx_rtd_theme \
               sphinx-copybutton \
               sphinx-tabs \
               sphinxcontrib \
               sphinx-toolbox \
               sphinxcontrib-bibtex
> conda activate sphinx
> pip install --upgrade sphinx_carousel
```

**2)** Para realizar o build, utilize:

```bash
cd docs
rm -rf build/ && python -m sphinx -b html . build
```

**3)** Por fim, abra o arquivo **build/index.html** no seu navegador.


## Planilhas

| Nome | Local | Proprietário | Responsáveis | Descrição |
| ------ | ------ | ------ | ------ | ------ |
| ConjuntosDados-INPE | Planilha Google | Gilberto (gribeiro.mg) | <p>Abner Anjos</p><p>Fabiana Zioti</p><p>Karine Ferreira</p><p>Lubia Vinhas</p><p>Raphael Costa</p><p>Rennan Marujo</p> | <p>Lista de coleções, cubos e mosaicos consolidados.</p><p>Lista de grades utilizadas pelas coleções.</p> |
| Usuarios PostgreSQL | Planilha Google | Gilberto (gilberto.queiroz) | <p>Abner Anjos</p><p>Daiene Batagioti</p><p>Raphael Costa</p> | <p>Lista de usuários das instâncias de pgAdmin.</p><p>Lista de usuários e roles das instâncias de PostgreSQL</p><p>Controle HBA (Host-based Authentication).</p> |
| BDC-Lab - Usuarios  | Planilha Google | Gilberto (gilberto.queiroz) | <p>Daiene Batagioti</p><p>Luana Becker</p><p>Raphael Costa</p><p>Karine Ferreira</p> | <p>Lista de usuários ativos e inativos.</p><p>Roles e configurações de hardware.<p> |
| Auditoria do Catalogo Dados | Planilha Google | Gilberto (gribeiro.mg) | <p>Raphael Costa</p><p>Rennan Marujo</p><p>Wildson Queiroz</p> | <p>Lista de produtos de dados validados, com datas da validação.</p> |
| organizacao-coids    | Planilha Google | Gilberto (gribeiro.mg) | <p>Raphael Costa</p><p>Diego Gomes</p> | <p>Lista de máquinas virtuais e alocação nos clusters da rede de operação (interna) e DMZ.</p><p>Lista de volumes de dados e políticas de montagem e acesso.</p> |
| Controle-Copia-Dados | Planilha Google | Gilberto (gribeiro.mg) | <p>Jeferson Arcanjo</p><p>Karine Ferreira</p><p>Raphael Costa</p><p>Rennan Marujo</p> | <p>Legado de conjuntos de dados movimentados entre servidores do BDC e para a COIDS.</p> |
| Indice de Dados      | Planilha Google | Gilberto (gribeiro.mg) | <p>Raphael Costa</p> | <p>Lista de localização de alguns dados fragmentados em servidores da DIOTG.</p> |


## Planilhas TODO
| Nome | Local | Proprietário | Responsáveis | Descrição |
| ------ | ------ | ------ | ------ | ------ |
| Configuração ambiente de acesso à COIDS e DIOTG: SSH, túneis, VPN, FireFox e Chrome.  |  |  |  |  |
| Troca de informação criptografada.  |  |  |  |  |
| Configuração de um novo GitLab Runner  |  |  |  |  |
| Monitoramento de VMs (logs, etc) - SysOps: identificação de problemas no Linux e aplicações  |  |  |  |  |
| Roteiros e definições de como produzir uma pipeline no GitLab CI/CD e chave SSH de deployment  |  |  |  |  |
| Roteiro de como portar os produtos L2A gerados via SAFE em SJC para o formato na COIDS com a Big  |  |  |  |  |
| Descrição Geral das Dependências de todo o Sistema Portal  |  |  |  |  |
| Descrição Geral das Dependências de todo o Sistema TerraCollect  |  |  |  |  |
| Documento com listagem de repositórios e árvore de dependências Portal  |  |  |  |  |
| Documento com listagem de repositórios e árvore de dependências TerraCollect  |  |  |  |  |
| Documentação processo TerraCollect API (Criação de Revisão, Execução Host, Execução WS, Execução DB, Setup WS)  |  |  |  |  |
| Documentação processo Sample API (Criação de Revisão, Execução WS, Execução nginx, Setup WS, Setup DB)  |  |  |  |  |
| Documentação processo LCCS API (Execução WS, Execução DB, Setup WS, Setup DB)  |  |  |  |  |
| Documentação processo RWSAS API (Execução WS, Setup WS)  |  |  |  |  |
| Documentação sobre os diferentes ambientes do BDC-Lab (versões de pacotes Python, R, etc.)  |  |  |  |  |
| RFCs: WTSS  |  |  |  |  |

## Diagramas TODO
| Nome | Local | Proprietário | Responsáveis | Descrição |
| ------ | ------ | ------ | ------ | ------ |
| Instancias de serviços e aplicações |  |  |  |  |
| Máquinas e contêineres |  |  |  |  |

## Monitoramento TODO
| Nome | Local | Proprietário | Responsáveis | Descrição |
| ------ | ------ | ------ | ------ | ------ |
| Check-list backup vms, bd, etc. |  |  |  |  |
| Check-list geração dados. |  |  |  |  |
| Check-list volumes de dados. |  |  |  |  |
| Check-list recursos de hardware em uso |  |  |  |  |
| Check-list usuário |  |  |  |  |


## Surveys TODO
| Nome | Local | Proprietário | Responsáveis | Descrição |
| ------ | ------ | ------ | ------ | ------ |
| BDC-Lab: necessidade de novas bibliotecas, as dificuldades de uso, erros frequentes, sugestões de melhoria. |  |  |  |  |
| Dados: descrição está adequada? Tem Alguma informação dúbia? Inspiração no survey da USGS/NASA. |  |  |  |  |
