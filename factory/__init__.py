DB = 'psycopg2'


if DB == 'psycopg2':
    from postgres_factory import PostgresFactory
    factory = PostgresFactory()
