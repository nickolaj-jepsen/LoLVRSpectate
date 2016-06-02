import logging
import openvr

from LoLVRSpectate.VorpX import is_excluded
from LoLVRSpectate.main import VRSpectate
from LoLVRSpectate.utils import setup_logging


def main():
    setup_logging(debug=False)
    try:
        logging.info(is_excluded())
        logging.info("Starting main loop")
        VRSpectate().run()
    except Exception:
        logging.exception("")
        input("Press enter to close the program")
        raise SystemExit(-1)
    finally:
        openvr.shutdown()

if __name__ == '__main__':
    main()

