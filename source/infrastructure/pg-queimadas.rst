Queimadas
=========


O diagrama da :numref:`Figura %s <fig:infra:pg-queimadas>` apresenta a infraestrutura de servidores que suportam o Banco de Dados Queimadas. Esses servidores estão organizados em redes Operacional e DMZ.

.. figure:: ../img/infra/pg-queimadas.png
    :alt: Máquinas virtuais que sustentam o Banco de Dados Queimadas
    :width: 40%
    :figclass: align-center
    :name: fig:infra:pg-queimadas

    Máquinas virtuais que sustentam o Banco de Dados Queimadas.


A seguir, são descritas as principais VMs envolvidas:

.. rst-class:: open

- ``forquetinha``: Instância primária do BDQueimadas, localizada na rede Operacional sendo denominada ``forquetinha-queimadas-db-primary``.

- ``usbequistao``: Réplica do servidor primário do BDQueimadas, localizada na rede DMZ. Essa réplica é feita através de logs recebidos em um volume NetApp compartilhado. A VM é denominada ``usbequistao-queimadas-db-standby``.

- ``olindina``: Instância primária do banco de operação do Queimadas, localizada na rede Operacional. Essa VM é denominada ``olindina-queimadas-db-oper-primary``.

- ``doresopolis``: Réplica do banco de operação do Queimadas. Encontra-se na rede Operacional. Essa réplica é feita através do protocolo stream-replication. Essa VM é denominada ``doresopolis-queimadas-db-oper-standby``.
