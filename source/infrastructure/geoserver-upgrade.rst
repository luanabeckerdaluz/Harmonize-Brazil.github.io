Atualização do GeoServer
########################

.. epigraph:: Este documento fornece instruções sobre como atualizar uma instância do GeoServer. Neste exemplo, estamos utilizando a versão `2.25.2` e faremos a atualização para a versão `2.26.1`.


Requisitos
----------

Primeiramente, você precisa preparar a imagem Docker da nova versão do GeoServer. Verifique em nosso repositório [bdc/geoserver](https://lajedao.coids.inpe.br/bdc/geoserver) se estamos atualizados com a versão mais recente. Se não, siga as instruções do repositório para suportar a nova versão.

Realizando o backup do diretório de dados do GeoServer
++++++++++++++++++++++++++++++++++++++++++++++++++++++

É recomendado criar uma cópia do diretório de dados do GeoServer antes de realizar a atualização para manter um backup das configurações.

Antes de iniciar, crie um diretório de backup::

    sudo mkdir -p /mnt/data/geoserver/backups


Dê as permissões ao usuário bigdocker para controlar esse diretório::

    sudo chown bigdocker:bigdocker /mnt/data/geoserver/backups
    sudo su - bigdocker


Pare o serviço atual com o seguinte comando::

    docker compose down


Agora, faça o backup do diretório de dados::

    cd /mnt/data/geoserver
    cp -r data backups/data.2.25.2-2024-12-27


(Repita este processo em cada nó do GeoServer - ```saovicente.coids.inpe.br```, ```saocristovao.coids.inpe.br``` e ```suecia.coids.inpe.br```)

Atualizando o arquivo docker-compose.yml
----------------------------------------

.. note::

    Certifique-se de **NÃO** pular versões **maiores** entre as atualizações. Por exemplo, se você está na versão ```2.24.x``` e deseja ir para a ```2.27.x```, é preferível passar pela ```2.25.x``` e ```2.26.x``` antes, para minimizar erros nas configurações do GeoServer.


O processo de atualização é bastante simples e deve funcionar para a maioria das versões do GeoServer. Basta definir a versão principal do GeoServer no arquivo ```docker-compose.yml``` (ou no arquivo ```.env``` para versões <= ```2.24.x```).

Verifique se as variáveis no arquivo ```.env``` são compatíveis com a nova versão 2.26.1::

    cd containers/geoserver
    nano .env


No arquivo .env da versão 2.25.2 para 2.26.1, é necessário adicionar a seguinte flag::

    # Enable HTTPS (Make sure to mount /certs/server.key and /certs/server.pem). Defaults to false
    HTTPS_ENABLED=true


Depois disso, inicie os contêineres Docker::

    docker compose up -d


Verifique os logs para identificar possíveis problemas durante a atualização::

    docker compose logs -f

