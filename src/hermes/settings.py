import json
from typing import Any, List, Tuple, Type

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)


class HarvestCff(BaseModel):
    enable_validation: bool = False


class HarvestSettings(BaseModel):
    from_: list[str] = [ "cff", "git" ]
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


class TOMLSource(EnvSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        if field_name == 'hermes':

            return json.loads(value)
        return json.loads(value)


class Settings(BaseSettings):
    numbers: List[int]

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TOMLSource(settings_cls),)

    hermes: HermesSettings = HermesSettings()
