#!/usr/bin/env python
__author__ = "Abhishek"

"""This file contains some configuration / setup routines
for logger and GFLAGS."""

import sys
import gflags
import logging

# gflags config
LOG_LEVELS = {'debug':logging.DEBUG,
              'info':logging.INFO,
              'warning':logging.WARNING,
              'error':logging.ERROR,
              'critical':logging.CRITICAL,
              }

LOG_FMT_STR = '%(asctime)s-%(module)s:%(lineno)s-%(levelname)s - %(message)s'

gflags.DEFINE_enum('log_level', 'info', LOG_LEVELS, 'Log level for root logger')
FLAGS = gflags.FLAGS

def ConfigLoggerAndFlags(argv=sys.argv):
    # parse flags with baseline logger config
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError, e:
        PrintFlagsHelpAndDie(e)

    # configure the logger
    log_level = LOG_LEVELS.get(FLAGS.log_level, logging.NOTSET)
    logging.basicConfig(level=log_level,format=LOG_FMT_STR)
    return argv

def PrintFlagsHelpAndDie(error_msg):
    logging.error('%s\nUsage: %s ARGS\n%s', error_msg, sys.argv[0], FLAGS)
    sys.exit(1)
