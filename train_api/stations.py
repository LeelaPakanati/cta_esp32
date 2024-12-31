from train_api.route import Route
from train_api.responses import prepare_url
import json
import requests


class Stations:
    """Station information for the CTA stations and stops.

    Data source found in the API documentation.

    """

    url = "https://data.cityofchicago.org/resource/8pix-ypme.json"

    def __init__(self):
        pass
    @property
    def columns(self) -> list:
        """Useful columns for stations."""
        return [
                "stop_id",
                "stop_name",
                ]

    def lookup(self, route):
        full_url = prepare_url(self.url, {route:True, '$select':self.columns})
        return requests.get(full_url).json()
