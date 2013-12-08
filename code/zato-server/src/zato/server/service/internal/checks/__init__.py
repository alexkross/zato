# -*- coding: utf-8 -*-

"""
Copyright (C) 2013 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from json import dumps, loads

# Bunch
from bunch import Bunch

# Zato
from zato.common import CHANNEL, DATA_FORMAT, ZATO_OK
from zato.server.service import Service

class CheckService(Service):
    """ Base class for services that check other Zato services using its own API.
    """
    def invoke_check(self, service, payload=None):

        invoke_request = {
            'name': service,
            'payload': dumps(payload).encode('base64'),
            'channel': CHANNEL.INTERNAL_CHECK,
            'data_format': DATA_FORMAT.JSON,
            'transport': 'plain_http',
        }

        out = self.outgoing.plain_http['zato.check.service']
        invoke_response = out.conn.post(self.cid, invoke_request).data

        self.logger.info('invoke_response "%s"', invoke_response)

        if invoke_response['zato_env']['result'] == ZATO_OK:
            invoke_response = invoke_response['zato_service_invoke_response']
            response = loads(invoke_response['response'].decode('base64'))
            self.logger.info('response "%s"', response)
            return Bunch(response['response'])
        else:
            return invoke_response
