Banco de dados auxiliar do BDC
==============================


O diagrama da :numref:`Figura %s <fig:infra:pg-banco-auxiliar-BDC>` ilustra a configuração do banco de dados auxiliar do BDC, utilizado para ingestão e disseminação de dados auxiliares através de serviços OGC. As instâncias estão localizadas na rede Operacional, garantindo a replicação e disponibilidade dos dados.

.. figure:: ../img/infra/pg-banco-auxiliar-BDC.png
    :alt: Máquinas virtuais que sustentam o Banco de dados auxiliar do BDC
    :width: 40%
    :figclass: align-center
    :name: fig:infra:pg-banco-auxiliar-BDC

    Máquinas virtuais que sustentam o Banco de dados auxiliar do BDC.


A seguir, estão descritas as VMs envolvidas:

.. rst-class:: open

- ``quatis``: Servidor primário localizado na rede Operacional para ingestão de dados auxiliares do BDC que são replicados para disseminação através de serviços OGC. A VM é denominada ``quatis-bdc-db-general-primary``.

- ``uruguai``: Réplica do servidor primário feita através de logs recebidos em um volume NetApp compartilhado. Essa VM é denominada ``uruguai-bdc-db-general-standby`` e fica localizada na rede DMZ.

