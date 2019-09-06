import sys

try:
    from genskew.cli import main
except ImportError:
    sys.exit("The genskew.cli package need to be installed!")

sys.exit(main())
