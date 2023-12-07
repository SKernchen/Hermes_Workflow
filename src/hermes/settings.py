from pydantic import BaseModel
import json
import toml
import pathlib
from typing import Any, Dict, Tuple, Type

from pydantic.fields import FieldInfo


from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class HarvestCff(BaseModel):
    enable_validation: bool


class HarvestSettings(BaseModel):
    sources: list[str]
    cff: HarvestCff = HarvestCff


class DepositTargetSettings(BaseModel):
    site_url: str
    communities: list[str] = None
    access_right: str


class DepositSettings(BaseModel):
    target: str
    invenio: DepositTargetSettings = DepositTargetSettings
    invenio_rdm: DepositTargetSettings = DepositTargetSettings


class HermesSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding='utf-8')

    harvest: HarvestSettings = HarvestSettings
    deposit: DepositSettings = DepositSettings

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            TomlConfigSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )


class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a TOML file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        encoding = self.config.get('env_file_encoding')
        file_content_toml = toml.load(
            pathlib.Path("hermes.toml")
        )
        field_value = file_content_toml.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d
