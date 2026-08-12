import sys

from elt.console_view import main as view_main
from elt.run_pipeline import run_pipeline


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "view":
        view_main()
    else:
        run_pipeline()
