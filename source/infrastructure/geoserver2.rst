Geoserver
#########

.. epigraph:: Este documento apresenta a documentação de como publicar dados em uma instância do geoserver. A estrutura do documento esta dividido de acordo com o tipo de *datastore* desejado.

.. tip:: Para consultar diferentes formatos de dados servidos pelo GeoServer, veja https://docs.geoserver.org/latest/en/user/data/index.html.


SRIDS Customizados
==================

Alguns produtos de dados oferecidos pelos parceiros podem possuir um conjunto de SRIDs que não existem na tabela oficial do `EPSG <https://epsg.io/>`_. Deste modo, é necessário informa-lo no GeoServer para que possa identifica-lo e utiliza-lo na publicação de dados. Para isso, você deve editar o arquivo chamado ``epsg.properties``, localizado dentro da pasta ``user_projections`` do GeoServer. Se você estiver utilizando o Docker, este diretório se encontra possivelmente em ``/mnt/data/geoserver/data/user_projections``. Caso a instalação do GeoServer tenha sido feita diretamente na maquina host, o diretório é ``/var/lib/tomcat9/webapps/big#geoserver/data/``, onde **big#geoserver** representa o prefixo da instalação do GeoServer.

Basicamente, a assinatura do arquivo consiste em::

   <ID_SRID>=<CODIGO_WKT>


Abaixo se encontra um exemplo de como é a estrutura do arquivo ``user_projections/epsg.properties``::

   18001=PROJCS["Geoscience Australia Standard National Scale Lambert Projection",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS_1978",6378135,298.26],TOWGS84[0,0,0]],PRIMEM["Greenwich",0],UNIT["Decimal_Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["central_meridian",134.0],PARAMETER["latitude_of_origin",0.0],PARAMETER["standard_parallel_1",-18.0],PARAMETER["standard_parallel_2",-36.0],UNIT["Meter",1]]
   41001=PROJCS["WGS84 / Simple Mercator",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Decimal_Degree",0.0174532925199433]],PROJECTION["Mercator_1SP"],PARAMETER["central_meridian",0],UNIT["Meter",1]]


Considerando o `WKT oficial do BDC <https://brazil-data-cube.github.io/specifications/bdc-projection.html>`_ abaixo::

   PROJCS["unknown",GEOGCS["unknown",DATUM["Unknown based on GRS80 ellipsoid",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["latitude_of_center",-12],PARAMETER["longitude_of_center",-54],PARAMETER["standard_parallel_1",-2],PARAMETER["standard_parallel_2",-22],PARAMETER["false_easting",5000000],PARAMETER["false_northing",10000000],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]


Adicione-o no fim do arquivo, o SRID ``200000`` com a WKT acima, ficando o seguinte conteudo::

   200000=PROJCS["unknown",GEOGCS["unknown",DATUM["Unknown based on GRS80 ellipsoid",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["latitude_of_center",-12],PARAMETER["longitude_of_center",-54],PARAMETER["standard_parallel_1",-2],PARAMETER["standard_parallel_2",-22],PARAMETER["false_easting",5000000],PARAMETER["false_northing",10000000],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]


Ao salvar o arquivo, deve-se reiniciar a instância do GeoServer::

   docker restart geoserver
   # systemctl restart tomcat9


JNDI
====

`Java Naming and Directory Interface <https://en.wikipedia.org/wiki/Java_Naming_and_Directory_Interface>`_ é uma interface API do Java que permite acessar serviços de diretórios ou definições, por meio de nome de recursos. Dentro do GeoServer, esse recurso pode ser explorado por meio da um arquivo chamado ``context.xml``, localizado dentro do servidor web Apache Tomcat. Abaixo se encontra um exemplo de configuração:

.. code-block:: xml

   <Context antiResourceLocking="false" privileged="true" >
      <Resource name="jdbc/mosaics"
              auth="Container"
              type="javax.sql.DataSource"
              driverClassName="org.postgresql.Driver"
              url="jdbc:postgresql://<POSTGRES_HOST>:<POSTGRES_PORT>/<POSTGRES_DATABASE>"
              username="<POSTGRES_USER>"
              password="<POSTGRES_PASSWORD>"
              maxTotal="<MAX_CONNECTIONS>"
              initialSize="0"
              minIdle="0"
              maxIdle="8"
              maxWaitMillis="-1"
              timeBetweenEvictionRunsMillis="30000"
              minEvictableIdleTimeMillis="60000"
              testWhileIdle="true"
              validationQuery="SELECT 1"
         rollbackOnReturn="true" />
   </Context>

Onde os seguintes campos devem ser preenchidos:

- ``<POSTGRES_HOST>``: IP ou hostname de acesso ao banco de dados PostgreSQL*.

- ``<POSTGRES_PORT>``: Porta de acesso ao banco de dados PostgreSQL. Utilize **5432**.

- ``<POSTGRES_DATABASE>``: Nome da base de dados.

- ``<POSTGRES_USER>``: Usuario de conexão com banco de dados.

- ``<POSTGRES_PASSWORD>``: Senha de acesso ao banco de dados.

- ``<MAX_CONNECTIONS>``: Total de conexões que podem ser abertas pelo Java. Considere que esse total será utilizado e compartilhado entre todos os **stores** que usarem esse recurso.

Demais valores podem ser alterados de acordo com as caracteristicas e tuning do banco de dados.

A localização deste arquivo ``context.xml`` é dentro da pasta ``conf`` no Apache Tomcat. Se você está utilizando a imagem Docker versão 2.25, o diretório é ``/opt/apache-tomcat-9.0.84/conf/``. Entretanto, é recomendavel que coloque o arquivo dentro de ``/opt/config_overrides`` pois é movido automaticamente pelo script **entrypoint** da imagem. Abaixo se encontra um exemplo, onde o arquivo no host esta localizado em ``volumes/context.xml``::

   services:
   geoserver:
     image: ${DOCKER_IMAGE}
     container_name: "geoserver"
     env_file: .env
     restart: unless-stopped
     volumes:
       # Volumes related GeoServer and Data
       - "/mnt/data/geoserver/data:/opt/geoserver_data"
       - "/mnt/data/mosaico_bdc/cubes/mosaics:/mnt/data/mosaico_bdc/cubes/mosaics"
       - "/mnt/data/thematic:/mnt/data/thematic:ro"
       # Mount SSL certs
       - "/home/bigdocker/.local/ssl/certs/<host>.pem:/certs/server.pem:ro"
       - "/home/bigdocker/.local/ssl/private/<host>.key:/certs/server.key:ro"
       # Mount context with JNDI
       - "./volumes:/opt/config_overrides"
     ports:
       - "127.0.0.1:8443:8443"


Caso a instalação seja feita no host diretamente, o diretorio esta localizado em ``/var/lib/tomcat9/conf/`` ou ``/etc/tomcat9``.

Ao utilizar esse recurso, você deve informar por meio da chave ``jndiReferenceName``. Por exemplo, ``jndiReferenceName=java:comp/env/jdbc/mosaics``.

Mais informações podem ser encontrados no link https://docs.geoserver.org/latest/en/user/data/database/jndi.html.



Image Mosaic
============

Para utilizar o ImageMosaic com arquivos TIFF temporais, é essencial preparar três arquivos de configuração: datastore.properties, indexer.properties e timeregex.properties. Esses arquivos devem ser colocados no diretório designado para eles.


Estrutura dos Arquivos de Configuração
---------------------------------------

A seguir, descrevemos a configuração recomendada para cada um dos arquivos.

- datastore.properties

.. code-block:: shell

   SPI=org.geotools.data.postgis.PostgisNGJNDIDataStoreFactory
   Loose\ bbox=true
   Estimated\ extends=false
   validate\ connections=true
   Connection\ timeout=10
   preparedStatements=true
   jndiReferenceName=java:comp/env/jdbc/mosaics

.. tip:: Usar a interface JNDI para conectar com o banco de dados. Desta forma, mais de um datastore utiliza a mesma conexão de banco de dados. https://docs.geoserver.org/latest/en/user/data/database/jndi.html

- indexer.properties

.. code-block:: shell

   TimeAttribute=ingestion
   ElevationAttribute=elevation
   Schema=*the_geom:Polygon,location:String,time:java.util.Date
   AbsolutePath=true
   GranuleHandler=org.geotools.gce.imagemosaic.granulehandler.ReprojectingGranuleHandlerFactory
   PropertyCollectors=TimestampFileNameExtractorSPI[timeregex](ingestion) CoverageNameCollectorSPI=org.geotools.gce.imagemosaic.namecollector.FileNameRegexNameCollectorSPI:regex=(MAPBIOMAS_BRASIL)
   IndexingDirectories=mapbiomas/brasil/v8
   Wildcard=*.tif
   Recursive=true

.. tip:: O regex descrito nesse arquivo será utilizado para realizar a busca dos dados no diretório e também para a criação da tabela para a indexação no banco de dados.


- timeregex.properties

.. code-block:: shell

   regex=([0-9 -]{10})


Estrutura de Diretórios
------------------------


Os data sources estão organizados no diretório ``/mnt/data/geoserver/data/datasources`` na máquina saovicente. A seguir, está a lista dos stores atualmente publicados na instância do GeoServer:

 - esa
 - mosaic-cbers4-brazil-3m
 - mosaic-s2-amazon-1m
 - mosaic-s2-cerrado-4m
 - terraclass-amazonia-v3
 - mapbiomas-brazil-v8
 - mosaic-landsat-amazon-3m
 - mosaic-s2-amazon-3m
 - mosaic-s2-paraiba-3m
 - terraclass-cerrado
 - mosaic-cbers4a-paraiba-3m
 - mosaic-landsat-brazil-6m
 - mosaic-s2-cerrado-2m
 - mosaic-s2-yanomami_territory-6m


Como exemplo, para a publicação dos dados do projeto MapBiomas, os arquivos de configuração mencionados anteriormente estão localizados no diretório ``/mnt/data/geoserver/data/datasources/mapbiomas-brazil-v8``.

Os dados em si estão armazenados em ``/data/thematic``. No caso do MapBiomas, especificamente em ``/mnt/data/thematic/mapbiomas/brasil/v8.`` Neste diretório, encontram-se 38 arquivos TIFF, nomeados de acordo com a convenção MAPBIOMAS_BRASIL_ANO.tif, permitindo que o ImageMosaic leia e publique os arquivos corretamente.


Publicação dos Dados
--------------------

Após a correta organização dos dados e dos arquivos de configuração, a publicação pode ser realizada de duas maneiras:

Via Interface Web: Acesse a interface do GeoServer, navegue até a seção de Stores, e siga as instruções para adicionar um novo datastore ImageMosaic.

Através da API do GeoServer: Utilize as chamadas da API REST do GeoServer para automatizar o processo de publicação.


Após realizar a publicação alguns arquivos são gerados no diretório junto às properties. Como por exemplo, MAPBIOMAS_BRASIL.properties, sample_image.dat mapbiomas-brazil-v8.properties.


Caso seja necessário realizar a republicação do dado, os arquivos esses arquivos criados pelo GeoServer devem ser deletados do diretório. E a tabela de indexação que foi criada no banco também deve ser apagada.


Permissão de Escrita em Workspace no GeoServer
==============================================

Conceder permissão de escrita a um usuário ou (role) em um workspace específico no GeoServer.

Criação de usuários/roles
-------------------------

No menu lateral, vá em:

.. code-block:: shell

   Security → Users, Groups and Roles

Nessa opção é possĩvel:

- Criar um novo usuário.
- Criar uma nova role.
- Associar usuários a roles.

Exemplo: criar uma role chamada ``WLTS_WRITER`` e adicionar nela os usuários que poderão publicar camadas no workspace ``wlts``.


Definir Regras de Acesso aos Dados
----------------------------------

No mesmo menu **Security**, vá em:

.. code-block:: shell

   Security → Data

Essa seção é responsável por definir as permissões de acesso a workspaces e camadas.

Clique em **Add new rule** e configure os campos:

- **Workspace**: selecione o workspace desejado (ex: ``wlts``).
- **Layer**: selecione ``*`` para aplicar a permissão a todas as camadas do workspace.
- **Access mode**: escolha ``Admin``.
- **Roles**: selecione a role desejada (ex: ``WLTS_WRITER``).


Observações:

- A permissão ``Admin`` no contexto de um workspace **permite criar, editar e excluir camadas** dentro desse workspace.
- **Isso não concede privilégios administrativos globais**. O usuário **não terá acesso** a:

  - Logs
  - Global Services
  - Tile Caching
  - Security
  - Configurações Globais

Essas áreas continuam restritas aos usuários com a role ``ADMIN``.

Usuários atribuídos à role configurada (ex: ``WLTS_WRITER``) terão acesso apenas ao workspace especificado (ex: ``wlts``), 
podendo gerenciar suas camadas e estilos, sem afetar o restante da configuração do GeoServer.

Permissões REST para Role personalizada no GeoServer
=====================================================

A seguir é apresentado como configurar permissões REST específicas para o workspace ``prodes``, permitindo que usuários com a role ``WLTS_WRITER`` tenham acesso de leitura (GET) e escrita (POST, PUT, DELETE).

Caminho do arquivo de configuração:
------------------------------------

``/opt/geoserver/data_dir/security/rest.properties``

Adicionar:

.. code-block:: properties

    # Permissões REST específicas para o workspace 'prodes'

    # Permitir leitura (GET) no workspace 'prodes' para administradores e usuários wlts_teste
    /rest/workspaces/prodes*;GET=ROLE_ADMINISTRATOR,WLTS_WRITER
    /rest/workspaces/prodes/**;GET=ROLE_ADMINISTRATOR,WLTS_WRITER

    # Permitir escrita (POST, PUT, DELETE) no workspace 'prodes' para administradores e usuários do WLTS_WRITER
    /rest/workspaces/prodes*;POST,PUT,DELETE=ROLE_ADMINISTRATOR,WLTS_WRITER
    /rest/workspaces/prodes/**;POST,PUT,DELETE=ROLE_ADMINISTRATOR,WLTS_WRITER

    # Opcional: restringir tudo fora do workspace 'prodes' apenas para administradores
    /**;GET=ROLE_ADMINISTRATOR
    /**;POST,PUT,DELETE=ROLE_ADMINISTRATOR

Após modificar o arquivo, reinicie o container ou o serviço do GeoServer para aplicar as alterações:



