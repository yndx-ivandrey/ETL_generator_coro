from typing import Self

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# использование load_dotenv() позволяет не заботиться о расположении .env файла
# если использовать опцию env_file из SettingsConfigDict, файл .env должен быть в текущем каталоге
load_dotenv()


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="postgres_",
        # env_file=".env",
        # env_file_encoding="utf-8",
        # extra="ignore",
    )

    dbname: str = Field("postgres", validation_alias="POSTGRES_DB")
    # альтернативный вариант определения поля
    # но для сериализации нужно вызывать model_dump(by_alias=True)
    # db: str = Field("postgres", serialization_alias="dbname")
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432


class AppSettings(BaseSettings):
    """Как в .env передать список значений"""

    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    #     extra="ignore",
    # )

    tables: str
    tables_list: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def prepare_tables_list(self) -> Self:
        self.tables_list = self.tables.split(",")
        del self.tables
        return self


class Settings(BaseModel):
    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)


settings = Settings()


if __name__ == "__main__":
    print(settings.database.model_dump(by_alias=True))
    print(settings.app.model_dump(by_alias=True))
