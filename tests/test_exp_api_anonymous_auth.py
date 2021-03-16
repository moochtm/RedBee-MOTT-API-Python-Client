
from rbm_mott_cli.exp_api_client.exp_api import ExposureApiClient

import logging
logging.basicConfig(level=logging.DEBUG)

exp_api = ExposureApiClient()
with exp_api.customer('Matt').business_unit('MattTV') as bu:
    print(bu.sessionToken)
