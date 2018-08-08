from elysium import config
from elysium.exceptions import ConfigurationError
from elysium.factory.constants import POSTGRESQL, DBMS_SPLITTER
from elysium.factory.postgresql_factory import PostgreSQLFactory


if config['DATABASE']['DBMS'] == POSTGRESQL:
    factory = PostgreSQLFactory()
else:
    raise ConfigurationError('The DBMS is not set correctly. Choices are: %s' %
                             DBMS_SPLITTER.join([POSTGRESQL]))

