"""Helper functions for ODBC connection strings.

Demonstration of list comprension, string formating.
"""


def buildconnectionstring(params: dict[str, str]) -> str:
    """Build a connection string from a dictionary of parameters. Returns string."""

    return ";".join([f"{k}={v}" for (k, v) in params.items()])


if __name__ == "__main__":
    myParams = {"server": "rparkes", "database": "master", "uid": "sa", "pwd": "secret"}
    print(buildconnectionstring(myParams))
