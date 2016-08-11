import logging
import openvr

from LoLVRSpectate.utils import setup_logging
from LoLVRSpectate.main import start_app


def main():
    setup_logging(debug=False)
    try:
        logging.info("Starting main loop")
        start_app()
    except Exception:
        logging.exception("")
        input("Press enter to close the program")
        raise SystemExit(-1)
    finally:
        openvr.shutdown()

if __name__ == '__main__':
    main()

