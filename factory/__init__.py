from elysium.factory.postgresql_factory import PostgreSQLFactory
from elysium import config


if config['DATABASE']['DBMS'] == 'postgresql':
    factory = PostgreSQLFactory()
else:
    raise Exception()

