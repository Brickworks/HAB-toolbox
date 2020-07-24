#!/usr/bin/env python3

##########################
# shared utility functions
##########################

import logging
import os
import json
from collections import namedtuple

log = logging.getLogger()


def test_logger():
    # these messages only appear if --debug is set
    log.debug('test debug')

    # these messages only appear if --verbose is set
    log.info('test info')

    # these messages always appear
    log.warning('test warning')
    log.critical('test critical')
    log.error('test error')
