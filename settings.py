from pydantic import BaseSettings
import os

os_env = os.environ


class Settings(BaseSettings):
    emissions_url = os_env.get("EMISSIONS_URL",
                               "https://api.v2.emissions-api.org/api/v2/")
    record_limit = os_env.get("RECORD_LIMIT", 30000)
    emission_data = dict()
