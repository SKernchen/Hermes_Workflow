import json
from typing import Any, List, Tuple, Type

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)


class HarvestCff(BaseModel):
    enable_validation: bool = False


class HarvestSettings(BaseModel):
    from_: list[str]
    cff: HarvestCff = HarvestCff()


class DepositTargetSettings(BaseModel):
    site_url: str = 'https://sandbox.zenodo.org'
    communities: list[str] = ["zenodo"]
    access_right: str = "open"


class DepositSettings(BaseModel):
    target: str = 'invenio_rdm'
    invenio: DepositTargetSettings = DepositTargetSettings()
    invenio_rdm: DepositTargetSettings = DepositTargetSettings()


class HermesSettings(BaseModel):
    harvest: HarvestSettings = HarvestSettings()
    deposit: DepositSettings = DepositSettings()


class Settings(BaseSettings):
    hermes: HermesSettings = HermesSettings()
    model_config = SettingsConfigDict(env_prefix='hermes_')
