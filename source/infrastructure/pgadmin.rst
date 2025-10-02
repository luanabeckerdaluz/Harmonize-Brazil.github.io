pgAdmin
=======


Na DMZ, a máquina virtual ``santalucia-bdc-monitor`` (santalucia.coids.inpe.br) contém uma instância do pgAdmin usada pela equipe de desenvolvimento e operação para acessar ou administrar os servidores de bancos de dados localizados nessa sub-rede. Essa instância do pgAdmin encontra-se instalada como um contêiner executado em modo *rootless*, ligando a porta 8443 da máquina virtual (*host*) à porta 443 (HTTPS) do contêiner (*guest*). Existe uma instância do NGINX na VM que serve de proxy reverso para a instância do pgAdmin no contêiner. O pgAdmin pode ser acessado através dos seguintes endereços:

- https://santalucia.coids.inpe.br/big/pgadmin 
- https://data.inpe.br/big/pgadmin (acessível apenas da sub-rede do INPE)


Na sub-rede de Operação, a máquina virtual ``arapua-bdc-ws`` (arapua.coids.inpe.br) contém uma instância do pgAdmin nos mesmos moldes da VM ``santalucia-bdc-monitor``. Essa instância pode ser acessada no seguinte endereço:

- https://arapua.coids.inpe.br/pgadmin


A lista de usuários com acesso ao pgAdmin pode ser vista na planilha de controle da infraestrutura ``PostgreSQL`` na guia pgAdmin.


As configurações do Docker Compose e do NGINX podem ser vistas no repositório `bdc/pgadmin <https://lajedao.coids.inpe.br/bdc/pgadmin>`__ do GitLab.


A recuperação de senhas é feita através do e-mail data.notifications@inpe.br.


.. tip:: 
    
    Para mais detalhes sobre a criação de contêineres do pgAdmin, veja a `documentação oficial <https://www.pgadmin.org/docs/pgadmin4/development/container_deployment.html>`__.


    Para saber mais sobre as variáveis de configuração que podem ser incluídas no arquivo ``.env``, consulte a seção `config.py <https://www.pgadmin.org/docs/pgadmin4/development/config_py.html#config-py>`__.