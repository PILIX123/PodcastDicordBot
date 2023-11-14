from pytest import MonkeyPatch
from hvac.api.secrets_engines.kv_v2 import KvV2
from botmodules.vaultModule.vault import Vault


def test_vault_get_discord_token(monkeypatch: MonkeyPatch) -> None:
    def mockReadSecret(*args, **kwargs):
        return dict(
            {'data': dict({'data': dict({'bot': "test"})})})
    monkeypatch.setattr(
        KvV2, "read_secret_version", mockReadSecret)
    vault = Vault()
    assert vault.get_discord_token() == "test"
