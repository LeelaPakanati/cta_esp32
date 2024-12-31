import requests
import os

from train_api.route import Route
from train_api.responses import prepare_url


class TrainClient:
    url = "http://lapi.transitchicago.com/api"

    def __init__(self, key):
        self.key = key
        self.version: int = 1
        self.max_number_params = 4

    @property
    def base_url(self) -> str:
        return f"{self.url}/{self.version:.1f}"

    def arrivals(
        self,
        mapid=None,
        stpid=None,
        max_entries=3
    ):
        url = f"{self.base_url}/ttarrivals.aspx"
        params = {'key':self.key, 'outputType':"JSON", 'max':max_entries}
        if mapid is not None:
            params['mapid'] = mapid
        elif stpid is not None:
            params['stpid'] = stpid
        else:
            return None

        full_url = prepare_url(url, params)

        return requests.get(full_url).json()
