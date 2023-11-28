from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = "cook-it-up-keys"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

mongo_uri = "MONGO-URI"
edamam_id = "EDAMAM-APP-ID"
edamam_key = "EDAMAM-APP-KEY"

ATLAS_URI = client.get_secret(mongo_uri).value
EDAMAM_APP_ID = client.get_secret(edamam_id).value
EDAMAM_APP_KEY = client.get_secret(edamam_key).value

# print(ATLAS_URI)
# print(EDAMAM_APP_ID)
# print(EDAMAM_APP_KEY)
