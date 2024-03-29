from argparse import ArgumentParser, Namespace
from typing import Any, TypeAlias
import boto3

from redshift_client import RedshiftClient

Event: TypeAlias = dict[str, str]


def handler(event: Event, context: Any) -> int:
    delete_query: str = (
        f"DELETE FROM {event['redshift_schema']}.{event['redshift_table']} "
        f"WHERE "
        f"        date >= '{event['start_date']}'"
        f"    AND date < '{event['end_date']}'"
        f";"
    )
    print(delete_query)

    redshift_client: RedshiftClient = RedshiftClient(
        host=event["redshift_host"],
        port=event["redshift_port"],
        cluster=event["redshift_cluster"],
        database=event["redshift_database"],
        user=event["redshift_user"],
    )
    rows_deleted: int = redshift_client.run_query(delete_query)
    return rows_deleted


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
    arg_parser.add_argument(
        "--redshift-schema",
        dest="redshift_schema",
        required=True,
        help="Redshift table to delete data from",
    )
    arg_parser.add_argument(
        "--redshift-table",
        dest="redshift_table",
        required=True,
        help="Redshift table to delete data from",
    )
    arg_parser.add_argument(
        "--start-date",
        dest="start_date",
        required=True,
        help="Date to delete data from",
    )
    arg_parser.add_argument(
        "--end-date",
        dest="end_date",
        required=True,
        help="Date to delete data to",
    )
    args: Namespace = arg_parser.parse_args()

    boto3.setup_default_session(profile_name=args.aws_profile)
    local_event: Event = {
        "redshift_host": args.redshift_host,
        "redshift_port": args.redshift_port,
        "redshift_cluster": args.redshift_cluster,
        "redshift_database": args.redshift_database,
        "redshift_user": args.redshift_user,
        "redshift_schema": args.redshift_schema,
        "redshift_table": args.redshift_table,
        "start_date": args.start_date,
        "end_date": args.end_date,
    }
    rows_deleted: int = handler(local_event, None)
    print(f"{rows_deleted} rows deleted")
