
STAC
====

Este guia explica como configurar e implantar o serviço STAC em uma máquina virtual. O STAC é um serviço que gerencia e serve coleções de dados geoespaciais. As instruções a seguir irão guiá-lo pelo processo, desde a configuração inicial até a verificação final do serviço.


Verificando a Configuração de Auto-Mount
----------------------------------------

Primeiro, precisamos verificar o arquivo de configuração do sistema que cuida do auto-mount (montagem automática) dos discos. Esse arquivo define como e onde os discos ou partições são montados no sistema.

Acesse o arquivo de configuração do auto-mount:
+++++++++++++++++++++++++++++++++++++++++++++++

Execute o comando abaixo para visualizar o conteúdo do arquivo bdc.discos, que está localizado em /etc/auto.master.d/:

.. code-block:: bash

    cat /etc/auto.master.d/bdc.discos


Verifique se as configurações estão corretas e se os discos necessários estão sendo montados automaticamente.


Configuração do STAC
--------------------

Acessando o Usuário bigdocker
+++++++++++++++++++++++++++++

Para acessar o ambiente onde o STAC será configurado, você precisa trocar para o usuário bigdocker utilizando o seguinte comando:

.. code-block:: bash

    sudo su - bigdocker

O comando **sudo su - bigdocker** faz com que você consiga executar comandos com as permissões desse usuário.


Navegando para o Diretório de Containers
++++++++++++++++++++++++++++++++++++++++

Utilize o comando abaixo para navegar até o diretório onde o arquivo de configuração do Docker (docker-compose.yml) e o arquivo de ambiente (.env) serão armazenados. Caso o diretório ainda não exista, você pode criá-lo:

.. code-block:: bash

    cd containers/bdc-stac


Configurando os Arquivos docker-compose.yml e .env
++++++++++++++++++++++++++++++++++++++++++++++++++

- Crie os arquivos de configuração:
    Se os arquivos docker-compose.yml e .env ainda não existirem, você pode criá-los com o comando vim. Você pode usar modelos de arquivos de outra máquina virtual como base:

    .. code-block:: bash

        vim docker-compose.yml
        vim .env

- Atualize as configurações de cada arquivo para atender as necessidades do serviço.


Definindo Permissões e Verificando Credenciais
++++++++++++++++++++++++++++++++++++++++++++++

- Defina as permissões do arquivo .env:
    O arquivo .env contém informações sensíveis, como credenciais. Para protegê-lo, ajuste as permissões para que somente o usuário bigdocker possa lê-lo e escrevê-lo:

    .. code-block:: bash

        chmod 600 .env

- Verifique as credenciais no arquivo .env:
    Verifique as credenciais e outras variáveis configuradas no arquivo .env para garantir que tudo está configurado corretamente:

    .. code-block:: bash

        cat .env


Atualizando e Baixando Imagens Docker
+++++++++++++++++++++++++++++++++++++

Baixe as imagens Docker que o STAC utilizará:

.. code-block:: bash

    docker compose pull

Esse comando baixa as versões mais recentes das imagens Docker especificadas no arquivo docker-compose.yml.



Testando Conectividade com o Banco de Dados
+++++++++++++++++++++++++++++++++++++++++++

O STAC se conecta a um banco de dados PostgreSQL. Para garantir que ele pode se conectar ao banco de dados, faça um teste de conectividade com o host onde o banco de dados está rodando. No exemplo, o nome do host é guaraniacu:

**OBS:** Você pode verificar o nome do host no arquivo **.env**

.. code-block:: bash

    curl guaraniacu.coids.inpe.br:5432

O comando curl tenta estabelecer uma conexão com o endereço e porta especificados. Se a conexão for bem-sucedida, o banco de dados está acessível.



Adicionando o IP da Máquina ao PostgreSQL
+++++++++++++++++++++++++++++++++++++++++

- Antes de permitir a conexão ao banco de dados, descubra o IP da máquina com o STAC:

.. code-block:: bash

    ip a

- Adicione o IP ao PostgreSQL:

    Para permitir que a máquina com o STAC acesse o banco de dados PostgreSQL, você precisa adicionar o IP da máquina à lista de permissões no arquivo pg_hba.conf do PostgreSQL:

    - Conecte-se à máquina guaraniacu via SSH:

    .. code-block:: bash

        ssh -p 22 guaraniacu.coids.inpe.br

    - Edite o arquivo de configuração do PostgreSQL (pg_hba.conf) adicionando uma linha com o IP da máquina com o STAC para permitir o acesso.:

    .. code-block:: bash

        sudo vim /etc/postgresql/16/main/pg_hba.conf

    - Recarregue a configuração do PostgreSQL para aplicar as mudanças:

        Primeira opção para recarregar o PostgreSQL: 
        
        .. code-block:: bash

            sudo -u postgres psql -c "SELECT pg_reload_conf();"

        Segunda opção para recarregar o PostgreSQL: 

        .. code-block:: bash

            sudo systemctl reload postgresql


Verificando o STAC
++++++++++++++++++

Para garantir que o STAC está funcionando como esperado, faça uma solicitação ao serviço rodando localmente:

.. code-block:: bash

    curl 127.0.0.1:8000

Se tudo estiver correto, você verá uma resposta do serviço STAC.


Configuração do NGINX
---------------------

Verificando e Atualizando o NGINX
+++++++++++++++++++++++++++++++++

Antes de qualquer coisa, verifique qual versão do NGINX está instalada e se há alguma política de instalação ativa:

.. code-block:: bash

    apt policy nginx

Se precisar atualizar o NGINX, siga as instruções no arquivo **docs/nginx.md** dentro do diretório de configuração do **iac**.

**Exemplo:**

.. code-block:: bash

    ansible-playbook -l araguari playbooks/test-prepare.yaml --tags nginx


Configurando o NGINX para o STAC
++++++++++++++++++++++++++++++++

- Confirme que o arquivo de configuração do NGINX inclui todas as configurações necessárias, como diretórios e arquivos:

.. code-block:: bash
    
    cat /etc/nginx/conf.d/default.conf


- Se o diretório /etc/nginx/apps/ ainda não existir, crie-o:

.. code-block:: bash
    
    sudo mkdir /etc/nginx/apps/

- Baseado em uma configuração existente **(por exemplo, o da Senegal)**, crie e edite um arquivo de configuração para o STAC:

.. code-block:: bash
    
    sudo vim /etc/nginx/apps/stac.conf


**Exemplo:**

.. code-block:: bash
    
    location /bdc/stac/v1/ {
        proxy_pass http://127.0.0.1:8000/;

        # Uncomment these next lines to customize STAC default variables
        # proxy_set_header X-Stac-Url "https://data.inpe.br/bdc/stac/v1/";
        # proxy_set_header X-Script-Name "https://data.inpe.br/bdc/";

        # Allow max of 2MB
        client_max_body_size 2M;

        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }


Essa configuração deve refletir as necessidades específicas do STAC, como os endereços e portas que ele utilizará.

- Após configurar o NGINX, teste a configuração para garantir que não há erros:

.. code-block:: bash
    
    sudo nginx -t

- Se o teste passar sem problemas, recarregue o NGINX para aplicar as novas configurações:

.. code-block:: bash
    
    sudo systemctl reload nginx

**OBS:** Não se esqueça de configurar o client_max_body_size para 2M no arquivo de configuração do NGINX e manter as variáveis de host e protocolos necessários para refletir as informações do host de origem.



Configurar o NGINX para Mapear os Dados
+++++++++++++++++++++++++++++++++++++++

Copie a configuração de uma máquina existente **(como a da Senegal)** para a nova máquina com o STAC:

.. code-block:: bash
    
    cat /etc/nginx/apps/data.conf

**Exemplo:**

.. code-block:: bash
    
    location /bdc/data/S2_L2A/ {
        rewrite /bdc/data/(.*) /$1 break;
        root /mnt/data/sentinel2_cog/archive/optical;
    }

- Após configurar o NGINX, teste a configuração para garantir que não há erros:

.. code-block:: bash
    
    sudo nginx -t

- Se o teste passar sem problemas, recarregue o NGINX para aplicar as novas configurações:

.. code-block:: bash
    
    sudo systemctl reload nginx