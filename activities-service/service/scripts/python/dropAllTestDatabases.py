from sqlalchemy import create_engine, text


def drop_test_databases():
    engine = create_engine(f"postgresql://postgres:postgres@db/postgres")
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")

        # Get all test DB names
        result = conn.execute(
            text(
                """
            SELECT datname FROM pg_database
            WHERE datname LIKE 'test%' AND datname NOT IN ('postgres', 'template0', 'template1');
        """
            )
        )

        for row in result:
            db_name = row[0]
            print(f"Dropping database: {db_name}")

            # Terminate connections to the DB
            conn.execute(
                text(
                    f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = :db_name AND pid <> pg_backend_pid();
            """
                ),
                {"db_name": db_name},
            )

            # Drop the database
            conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))

    engine.dispose()


drop_test_databases()
