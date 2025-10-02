Keycloak
========


As seguintes VMs sustentam o sistema Keycloak na DMZ:

.. rst-class:: open

- ``salvador``: Instância do keycloak, executando como contêiner. Essa VM é denominada ``salvador-bdc-keycloak``.

- ``sudao``: Instância primária do PostgreSQL, acessada diretamente pelo Keycloak. Essa VM é denominada ``sudao-bdc-keycloak-db-primary``.

- ``sudaosul``: Réplica usando o protocolo de stream do PostgreSQL. Essa VM é denominada ``sudaosul-bdc-keycloak-db-standby1``.


.. figure:: ../img/infra/pg-keycloak.png
    :alt: Máquinas virtuais que sustentam o Keycloak e seu banco de dados
    :width: 40%
    :figclass: align-center
    :name: fig:infra:pg-keycloak

    Máquinas virtuais que sustentam o Keycloak e seu banco de dados.


.. note::

    Existe uma instância do Keycloak usada no desenvolvimento. Esta intância encontra-se na máquina denominada ``caridade``.
    

Links: 

.. rst-class:: open

- `Interface de administração data.inpe.br <https://salvador.coids.inpe.br/iam/admin/master/console/>`__ (acessível apenas pela rede interna).

- `Gerenciador de conta de usuário do realm INPE <https://data.inpe.br/iam/realms/inpe/account/#/>`__.

- `Interface de administração da instância de desenvolvimento <https://caridade.coids.inpe.br/iam/admin/master/console>`__ (acessível apenas pela rede interna).
