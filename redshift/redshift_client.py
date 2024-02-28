from typing import Any, TypeAlias
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

        """
        I'm too lazy to build postgres functionality here atm so outputting
        a command that will let you connect via psql
        """
        print(
            f"export PGPASSWORD={response['DbPassword']} ** "
            f"psql -h {host} -p {port} -d {database} -U {response['DbUser']}"
        )
