#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

try:
    import colorlog
except ImportError:
    colorlog = False

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

FORMATTER = (
    "%(asctime)s "
    "[%(log_color)s%(levelname)s%(reset)s] "
    "[%(cyan)s%(name)s:%(lineno)s%(reset)s] "
    "%(message_log_color)s%(message)s"
)

COLORS = {
    "DEBUG": "bold_cyan",
    "INFO": "bold_green",
    "WARNING": "bold_yellow",
    "ERROR": "bold_red",
    "CRITICAL": "bold_red,bg_white",
}

SECONDARY_COLORS = {
    "message": {
        "DEBUG": "white",
        "INFO": "bold_white",
        "WARNING": "bold_yellow",
        "ERROR": "bold_red",
        "CRITICAL": "bold_red",
    },
}


class ColorLoggerFactory:
    def __init__(self):
        self.formatter = None
        self.handler = None
        self._setup_formatter()
        self._get_stream_handler()

    def _setup_formatter(self):
        self.formatter = colorlog.ColoredFormatter(
            FORMATTER,
            reset=True,
            log_colors=COLORS,
            secondary_log_colors=SECONDARY_COLORS,
            style="%",
        )

    def _get_stream_handler(self):
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                self.handler = handler
                break
        else:
            self.handler = logging.StreamHandler()

    def set_formatter(self):
        self.handler.setFormatter(self.formatter)


def setup_colorlog():
    factory = ColorLoggerFactory()
    factory.set_formatter()


if colorlog is not False:
    setup_colorlog()
