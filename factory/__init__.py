from elysium.factory.postgres_factory import PostgresFactory
from elysium import config


if config['DATABASE']['DBMS'] == 'postgresql':
    factory = PostgresFactory()
else:
    raise Exception()

