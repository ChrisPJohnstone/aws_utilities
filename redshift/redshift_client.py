from typing import Any, TypeAlias
from psycopg2 import connect, extensions
import boto3

JsonType: TypeAlias = dict[str, Any]


class RedshiftClient:
    def __init__(
        self,
        host: str,
        port: str,
        cluster: str,
        database: str,
        user: str,
    ) -> None:
        client = boto3.client("redshift")
        response: JsonType = client.get_cluster_credentials(
            ClusterIdentifier=cluster,
            DbName=database,
            DbUser=user,
        )
        print(
            f"export PGPASSWORD={response['DbPassword']} && "
            f"psql -h {host} -p {port} -d {database} -U {response['DbUser']}"
        )
        self.connection_kwargs: dict[str, str] = {
            "host": host,
            "port": port,
            "database": database,
            "user": response["DbUser"],
            "password": response["DbPassword"],
        }
    
    def run_query(self, query: str) -> None:
        connection: extensions.connection = connect(**self.connection_kwargs)
        cursor: extensions.cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
