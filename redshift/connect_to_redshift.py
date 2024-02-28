from argparse import ArgumentParser, Namespace
from typing import Any, TypeAlias
import boto3

from redshift_client import RedshiftClient

Event: TypeAlias = dict[str, str]


def handler(event: Event, context: Any) -> None:
    redshift_client: RedshiftClient = RedshiftClient(
        host=event["redshift_host"],
        port=event["redshift_port"],
        cluster=event["redshift_cluster"],
        database=event["redshift_database"],
        user=event["redshift_user"],
    )


if __name__ == "__main__":
    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument(
        "--aws-profile",
        dest="aws_profile",
        required=True,
        help="AWS Profile to use for auth",
    )
    arg_parser.add_argument(
        "--redshift-host",
        dest="redshift_host",
        required=True,
        help="Redshift host to connect to",
    )
    arg_parser.add_argument(
        "--redshift-port",
        dest="redshift_port",
        required=True,
        help="Redshift port to connect to",
    )
    arg_parser.add_argument(
        "--redshift-cluster",
        dest="redshift_cluster",
        required=True,
        help="Redshift cluster to connect to",
    )
    arg_parser.add_argument(
        "--redshift-database",
        dest="redshift_database",
        required=True,
        help="Redshift database to connect to",
    )
    arg_parser.add_argument(
        "--redshift-user",
        dest="redshift_user",
        required=True,
        help="Redshift user to use for auth",
    )
    args: Namespace = arg_parser.parse_args()

    boto3.setup_default_session(profile_name=args.aws_profile)
    local_event: Event = {
        "redshift_host": args.redshift_host,
        "redshift_port": args.redshift_port,
        "redshift_cluster": args.redshift_cluster,
        "redshift_database": args.redshift_database,
        "redshift_user": args.redshift_user,
    }
    handler(local_event, None)
