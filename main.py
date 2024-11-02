import sys

from App import App


def main():
    application = App(sys.argv)
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
