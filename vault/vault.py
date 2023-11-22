from hvac import Client
from dotenv import load_dotenv
from os import getenv


class Vault():
    def __init__(self) -> None:
        load_dotenv(".env")
        print(getenv("token"))
        self.client = Client(
            url="http://192.168.2.19:8200", token=getenv("token"))

    def get_discord_token(self) -> str:
        read_response = self.client.secrets.kv.read_secret_version(
            path="discord")
        keyValue = read_response['data']['data']['bot']
        return keyValue
