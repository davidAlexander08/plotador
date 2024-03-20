from apps.cli import cli
import os
import pathlib
from apps.utils.log import Log


def main():
    os.environ["APP_INSTALLDIR"] = os.path.dirname(os.path.abspath(__file__))
    BASEDIR = pathlib.Path().resolve()
    os.environ["APP_BASEDIR"] = str(BASEDIR)
    Log.configure_logging(BASEDIR)
    cli()


if __name__ == "__main__":
    main()
