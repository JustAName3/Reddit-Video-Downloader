import logging.config
import log 

logging.config.dictConfig(config= log.logger_config)

_logger = logging.getLogger("_startup")
_logger.info("Starting...")


import gui


logger = logging.getLogger("main")


try:
    App = gui.App()
    logger.info("Initialized gui.App")

    App.mainloop()
    logger.info("Closed app")

except Exception:
    logger.exception("")