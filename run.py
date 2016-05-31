from utils import setup_logging
from logic import MainLogic
import logging
from openvr import shutdown


def main():
    setup_logging(debug=False)
    try:
        logging.info("Starting main loop")
        MainLogic().run()
    except Exception:
        logging.exception("")
        input("Press enter to close the program")
        raise SystemExit(-1)
    finally:
        shutdown()

if __name__ == '__main__':
    main()

