import sys

try:
    from genskew.web import app
except ImportError:
    sys.exit("The genskew.web package need to be installed!")

if __name__ == "__main__":
    app.run()
