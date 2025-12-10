"""Helper functions for ODBC connection strings."""


def buildconnectionstring(params: dict[str, str]) -> str:
    """Build a connection string from a dictionary of parameters. Returns string."""

    return ";".join([f"{k}={v}" for (k, v) in params.items()])


if __name__ == "__main__":
    myParams = {"server": "rparkes", "database": "master", "uid": "sa", "pwd": "secret"}
    print(buildconnectionstring(myParams))
