.. include:: ../../def.rst

.. _sec_procedimentos_atualizar-versao-postgres:

Atualização do PostgreSQL em um Ambiente com Replicação
=======================================================

Esta documentação orienta sobre a atualização do PostgreSQL em um ambiente Ubuntu com configuração de replicação, utilizando dois servidores: o servidor principal (primary) e uma réplica (standby).

.. warning::

    **Atenção:** Sempre atualize a réplica primeiro para verificar a compatibilidade e garantir a segurança da atualização.


Configuração e Backup na Máquina Cedro
--------------------------------------

A máquina Cedro é responsável por realizar os backups do banco de dados. Antes de qualquer atualização no PostgreSQL, é essencial garantir que a máquina Cedro esteja configurada corretamente para receber os backups e que o processo de backup seja executado com sucesso. Isso assegura que, caso ocorra algum problema durante a atualização, os dados possam ser restaurados sem perda.


Verificar a conectividade com o servidor primário
+++++++++++++++++++++++++++++++++++++++++++++++++

Certifique-se de que a máquina Cedro consegue se conectar à VM primária:

.. code-block:: bash

    curl forquetinha:5432

Uma resposta como curl: **(52) Empty reply from server** indica que a conexão foi estabelecida, mas o servidor não respondeu.


Adicionar o IP da Cedro ao arquivo pg_hba.conf
++++++++++++++++++++++++++++++++++++++++++++++

No servidor primário, adicione o IP da Cedro às configurações de autenticação:

.. code-block:: bash

    sudo nano /etc/postgresql/16/main/pg_hba.conf
    host    bdqueimadas    postgres    150.163.212.16/32    trust


Em seguida, recarregue as configurações do PostgreSQL:

.. code-block:: bash

    sudo systemctl reload postgresql


Realizar o backup do banco de dados na Cedro
++++++++++++++++++++++++++++++++++++++++++++

Inicie uma sessão screen na Cedro:


.. code-block:: bash

    screen -S backup_pg


Dentro dessa sessão, execute o comando de backup:

.. code-block:: bash

    pg_dump --username=postgres \
        --no-owner \
        --no-privileges \
        --no-password \
        --host forquetinha.coids.inpe.br \
        --port 5432 bdqueimadas | gzip > /mnt/data/backup/postgresql/bdqueimadas/forquetinha_bdqueimadas.gz

.. tip::

    - Para sair temporariamente da sessão screen sem interromper o backup, use ``Ctrl + A`` seguido de ``D``.

    - Para verificar o progresso, confira o tamanho do arquivo gerado:

        .. code-block:: bash

            ls -lh /mnt/data/backup/postgresql/bdqueimadas/forquetinha_bdqueimadas.gz

    - Verificar o backup:

        .. code-block:: bash

            screen -r backup_pg
    
    - Para encerrar a sessão, digite ``exit``.


Atualização do PostgreSQL
-------------------------

Verifique versão atual
++++++++++++++++++++++

Em ambos os servidores (standby e primary), verifique a versão do PostgreSQL com o comando abaixo:

.. code-block:: bash

    psql --version

.. tip::

    Se você quiser consultar as versões do PostgreSQL disponíveis no repositório, execute o seguinte comando para verificar tanto as versões padrão quanto as disponíveis:


    .. code-block:: bash

        sudo apt-cache search postgresql-server


    A saída será algo como:

    .. code-block::

        postgresql-server-dev-14 - development files for PostgreSQL 14 server-side programming
        postgresql-server-dev-all - extension build tool for multiple PostgreSQL versions
        postgresql-server-dev-10 - development files for PostgreSQL 10 server-side programming
        postgresql-server-dev-11 - development files for PostgreSQL 11 server-side programming
        postgresql-server-dev-12 - development files for PostgreSQL 12 server-side programming
        postgresql-server-dev-13 - development files for PostgreSQL 13 server-side programming
        postgresql-server-dev-15 - development files for PostgreSQL 15 server-side programming
        postgresql-server-dev-16 - development files for PostgreSQL 16 server-side programming
        postgresql-server-dev-17 - development files for PostgreSQL 17 server-side programming
        postgresql-server-dev-17-dbgsym - debug symbols for postgresql-server-dev-17


    Para ver a versão mais recente, execute:

    .. code-block:: bash

        apt policy postgresql-16

    
    A saída será algo como:

    .. code-block::

        postgresql-16:
            Installed: 16.2-1.pgdg22.04+1
            Candidate: 16.5-1.pgdg22.04+2
            Version table:
                16.5-1.pgdg22.04+2 500
                    500 https://apt.postgresql.org/pub/repos/apt jammy-pgdg/main amd64 Packages
            *** 16.2-1.pgdg22.04+1 100
                    100 /var/lib/dpkg/status



    Para detalhes sobre uma versão específica, execute:

    .. code-block:: bash

        sudo apt-cache search postgresql-16


    Isso exibirá uma listagem mais detalhada de pacotes relacionados à versão selecionada:

    .. code-block::

        postgresql-16 - The World's Most Advanced Open Source Relational Database
        postgresql-16-age - Graph database optimized for fast analysis and real-time data processing
        postgresql-16-age-dbgsym - debug symbols for postgresql-16-age
        postgresql-16-asn1oid - ASN.1 OID data type for PostgreSQL




Pare o Serviço do PostgreSQL 16
+++++++++++++++++++++++++++++++

**1.** Verificar o Serviço do PostgreSQL 16:

Se você está usando o systemd, pode verificar se o serviço do PostgreSQL 16 está ativo com o comando:

.. code-block:: bash

    sudo systemctl status postgresql@16-main


**2.** Parar o serviço do PostgreSQL 16:

.. code-block:: bash

    sudo systemctl stop postgresql@16-main



Atualizar o cliente PostgreSQL
++++++++++++++++++++++++++++++

No servidor primário, execute:

.. code-block:: bash

    sudo apt-get update
    sudo apt-get upgrade postgresql-client-16


.. tip::

    A mensagem abaixo irá aparecer. Dê um **ok**.

    .. code-block::

        │ Newer kernel available                                                    │ 
        │                                                                           │ 
        │ The currently running kernel version is 5.15.0-106-generic which is not   │ 
        │ the expected kernel version 5.15.0-125-generic.                           │ 
        │                                                                           │ 
        │ Restarting the system to load the new kernel will not be handled          │ 
        │ automatically, so you should consider rebooting.                          │


    Depois, vai aparecer uma mensagem assim, com algumas opções selecionadas:

    .. code-block::

        Which services should be restarted?


    - Aperte em **cancelar**

    Como o sistema mexeu em algo do Kernel, para não ter problema com as reinstalações sugeridas, iremos fazer o reboot manualmente, já que a máquina precisa ser rebotada. Use o comando reboot:

    .. code-block:: bash

        sudo reboot



Testar se a Réplica Continua Recebendo Dados da Primária (Evitar Realizar Este Teste)
-------------------------------------------------------------------------------------

Na VM primária, execute o seguinte comando (se for réplica em redes diferentes que utilizam replicação por disco):

.. code-block:: bash

    sudo -u postgres psql
    CREATE TABLE teste2 (id BIGINT);
    INSERT INTO teste2 (id) SELECT * FROM generate_series(1, 10000);

Verifique se o arquivo foi criado na VM primária com o comando:

.. code-block:: bash
    
    ls -lah /mnt/data/pg-wal/archive

Na VM da réplica, os mesmos arquivos devem estar presentes no mesmo diretório.



Testar se a Réplica Continua Recebendo Dados Através do repmgr
--------------------------------------------------------------

Para verificar se a réplica está recebendo dados corretamente, execute o seguinte comando usando o repmgr (se for réplica e primária na mesma rede):

.. code-block:: bash

    repmgr -f /etc/postgresql/16/main/repmgr.conf service status



Verificar o Espaço Ocupado pelos Diretórios Principais do PostgreSQL
--------------------------------------------------------------------

**1.** Verificar o Tamanho do Diretório de Dados

O diretório de dados é onde as informações do banco de dados são armazenadas. No PostgreSQL, o diretório de dados padrão geralmente fica em `/var/lib/postgresql/`. Para verificar o espaço ocupado por esse diretório, use o comando:

.. code-block:: bash

    sudo du -sh /var/lib/postgresql/16

**2.** Verificar o Tamanho dos Arquivos de Configuração

Os arquivos de configuração do PostgreSQL estão localizados no diretório `/etc/postgresql/`. Embora esses arquivos geralmente ocupem menos espaço, é importante verificar o tamanho deles para garantir que tudo esteja correto após a atualização. Use o comando:

.. code-block:: bash

    sudo du -sh /etc/postgresql/16

**3.** Comparar o Tamanho Total dos Diretórios de Dados e de Configuração

Para uma visão mais abrangente, você pode comparar o espaço ocupado tanto pelo diretório de dados quanto pelos arquivos de configuração com um único comando:

.. code-block:: bash

    sudo du -sh /var/lib/postgresql/16 /etc/postgresql/16
