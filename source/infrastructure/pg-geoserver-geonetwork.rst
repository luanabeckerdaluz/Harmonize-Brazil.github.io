Banco de uso geral (GeoServer, GeoNetwork)
==========================================



O diagrama da :numref:`Figura %s <fig:infra:pg-geoserver-geonetwork>` apresenta o banco de uso geral utilizado pelo GeoServer e GeoNetwork. Este banco é responsável por servir dados para diversos sistemas do INPE, incluindo a BIG, BDC e Queimadas. A VM que opera este banco encontra-se na rede DMZ, fornecendo acesso controlado a serviços e dados para o mundo externo.

.. figure:: ../img/infra/pg-geoserver-geonetwork.png
    :alt: Instância única do GeoServer e GeoNetwork
    :width: 40%
    :figclass: align-center
    :name: fig:infra:pg-geoserver-geonetwork

    Instância única do GeoServer e GeoNetwork.


A seguir, está detalhada a VM envolvida:

.. rst-class:: open

- ``seicheles``: Instância única usada pelo GeoServer da BIG, BDC e Queimadas, e pelo GeoNetwork da BIG. Essa VM é denominada ``seicheles-db-general`` e fica localizada na DMZ.

