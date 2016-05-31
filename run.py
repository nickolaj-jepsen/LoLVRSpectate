from utils import setup_logging
import logging


def main():
    try:
        setup_logging(debug=False)
        import logic  # Temp hack, i really need to refactor the loop
    except Exception as e:
        logging.exception("")
        import sys
        print(e)
        input()
        sys.exit("")

if __name__ == '__main__':
    main()

