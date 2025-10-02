Catálogo de Imagens
===================


O diagrama da :numref:`Figura %s <fig:infra:pg-catalogo>` mostra os servidores que suportam o catálogo de imagens servido pelo STAC.


.. figure:: ../img/infra/pg-catalogo.png
    :alt: Máquinas virtuais que sustentam o catálogo de imagens e seu banco de dados
    :width: 40%
    :figclass: align-center
    :name: fig:infra:pg-catalogo

    Máquinas virtuais que sustentam o catálogo de imagens e seu banco de dados.


Esses servidores encontram-se organizados nas redes de operação (212), interna ao INPE, e dmz (218), com máquinas que fornecem serviços e dados para o mundo externo. As seguintes VMs são mostrados no diagrama:

.. rst-class:: open

- ``parobe``: Instância primária do PostgreSQL com o banco do catálogo. Essa VM é localizada na rede Operacional sendo denominada ``parobe-bdc-db-primary``. Este servidor também contém um banco de dados denomidado ``cube_explorer``.

- ``somalia``: Réplica do servidor primário. Encontra-se na rede DMZ. Essa réplica é feita através de logs recebidos em um volume NetApp compartilhado. Essa VM é denominada ``somalia-bdc-db-standby1``.

- ``srilanca``: Réplica do servidor primário. Encontra-se na rede DMZ. Essa réplica é feita através de logs recebidos em um volume NetApp compartilhado. Essa VM é denominada ``srilanca-bdc-db-standby2``.

- ``guaraniacu``: Réplica do servidor primário. Encontra-se na rede Operacional. Essa réplica é feita através do protocolo stream-replication. Essa VM é denominada ``guaraniacu-bdc-db-standby3``.