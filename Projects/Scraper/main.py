# -*- coding: utf-8 -*-
"""
Main app for fetching data from a home-page and save it to a mongo-db

_author__ =  "Daniel Grafström"
__license__ = "GPL"
__status__ = "Experimental"
"""

import logging

def create_logger():
    logger = logging.getLogger('main_scraper')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('main_scraper.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Main_scraper started")
    logger.debug("Main_scraper started")
    logger.error("Main_scraper started")
# todo, init database connections.
# todo, call schedule and start tasks

