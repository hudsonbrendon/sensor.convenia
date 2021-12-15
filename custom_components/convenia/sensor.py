import hashlib
import json
import logging
import string
from collections import defaultdict
from datetime import datetime, timedelta

import homeassistant.helpers.config_validation as cv
import pytz
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_NAME,
    CONF_RESOURCES,
    STATE_UNKNOWN,
)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

ICON = "mdi:cash"

SCAN_INTERVAL = timedelta(minutes=60)

ATTRIBUTION = "Data provided by convenia api"

DOMAIN = "convenia"

CONF_EMPLOYE_NAME = "employe_name"
CONF_COMPANIE_ID = "companie_id"
CONF_EMPLOYE_ID = "employe_id"
CONF_TOKEN = "token"

BASE_URL = "https://core.convenia.com.br/api/v1/companies/{}/employees/{}/payslips"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMPLOYE_NAME): cv.string,
        vol.Required(CONF_COMPANIE_ID): cv.string,
        vol.Required(CONF_EMPLOYE_ID): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the currency sensor"""
    name = "{} - Convenia".format(config["employe_name"])
    companie_id = config["companie_id"]
    employe_id = config["employe_id"]
    token = config["token"]

    add_entities(
        [ConveniaSensor(hass, name, companie_id, employe_id, token, SCAN_INTERVAL)],
        True,
    )


class ConveniaSensor(Entity):
    def __init__(self, hass, name, companie_id, employe_id, token, interval):
        """Inizialize sensor"""
        self._state = STATE_UNKNOWN
        self._hass = hass
        self._interval = interval
        self._name = name
        self._companie_id = companie_id
        self._employe_id = employe_id
        self._token = token
        self._payslips = []

    @property
    def name(self):
        """Return the name sensor"""
        return self._name

    @property
    def icon(self):
        """Return the default icon"""
        return ICON

    @property
    def state(self):
        return len(self._payslips)

    @property
    def payslips(self):
        """Abastecimento."""
        return [
            {
                "name": payslip.get("type").get("data").get("name"),
                "month": payslip.get("month"),
                "year": payslip.get("year"),
                "file": payslip.get("file"),
                "type_id": payslip.get("type_id"),
                "created_at": payslip.get("created_at"),
                "updated_at": payslip.get("updated_at"),
            }
            for payslip in self._payslips
        ]

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self._token}"}

    @property
    def url(self):
        return BASE_URL.format(self._companie_id, self._employe_id)

    @property
    def device_state_attributes(self):
        """Atributos."""
        return {
            "payslips": self.payslips,
        }

    def update(self):
        """Atualiza os dados fazendo requisição na API."""
        response = requests.get(self.url, headers=self.headers)
        if response.ok:
            self._payslips = response.json().get("data", [])
        else:
            _LOGGER.error(f"Cannot perform the request: {response.text}")
