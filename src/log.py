import pathlib
import logging.config

# Has to be imported before anything gets logged
# Configures the loggers on import

stdout_level: str = "INFO"  # Sets level for stdout handler
log_file_size: int = 100000 # Sets maxBytes for log  files --> 100kB
backup_count: int = 1       # Sets backupCount for log files

log_path = pathlib.Path(__file__).parent.parent / "logs"

debug_path = log_path / "debug.log"
info_path = log_path / "info.log"


logger_config: dict = {
    "version": 1,
    "disable_existing_logger": False,

    "formatters": {
        "standard": {
            "format": "%(levelname)s|%(name)s|Function: %(funcName)s()| %(message)s"
        },

        "date": {
            "format": "\n\n%(asctime)s|%(name)s: %(message)s\n"
        }
    },

    "handlers": {
        "stdout":{
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "standard",
            "level": stdout_level
        },

        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(info_path),
            "formatter": "standard",
            "level": "INFO",
            "maxBytes": log_file_size,
            "backupCount": backup_count
        },

        "debug_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": str(debug_path),
            "level": "DEBUG",
            "maxBytes": log_file_size,
            "backupCount": backup_count
        },

        "_df": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "date",
            "level": "DEBUG",
            "filename": str(debug_path),
            "maxBytes": log_file_size,
            "backupCount": backup_count
        },

        "_f": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "date",
            "level": "DEBUG",
            "filename": str(info_path),
            "maxBytes": log_file_size,
            "backupCount": backup_count
        }
    },

    "loggers": {
        "main.gui": {
            "level": "DEBUG",
            "propagate": True
        },

        "main.functions": {
            "level": "DEBUG",
            "propagate": True
        },

        "main": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stdout", "file", "debug_file"]
        },

        "_startup": {
            "level": "DEBUG",
            "propagate": False,
            "formatter": ["date"],
            "handlers": ["_df", "_f"]
        }
    }
}

# Configures the loggers on import
logging.config.dictConfig(config= logger_config)