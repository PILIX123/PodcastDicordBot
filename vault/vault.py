import hvac
import dotenv
import os

class Vault():
    def __init__(self) -> None:
        dotenv.load_dotenv(".env")
        self.client = hvac.Client(url="http://192.168.2.19:8200",token=os.getenv("token"))
    def get_discord_token(self)->str:
        read_response=self.client.secrets.kv.read_secret_version(path="discord")
        keyValue=read_response['data']['data']['bot']
        return keyValue