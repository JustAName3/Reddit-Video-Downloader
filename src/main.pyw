import log
import logging
import gui


def main():
    """
    Main function for initiating the gui.
    Catches exceptions that were not expected.
    """
    _logger = logging.getLogger("_startup")
    _logger.info("App started")

    logger = logging.getLogger("main")

    try:
        app = gui.App()
        logger.info("Initialized gui.App")

        app.mainloop()
        logger.info("Closed app")
    except Exception:
        logger.exception("Unexpected Exception: ")



if __name__ == "__main__":
    main()
