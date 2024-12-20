import json
from pathlib import Path

CONFIG_PATH = Path("app/config/samlconfig.json")

def load_saml_config():
    """Load SAML configuration from JSON file."""
    with CONFIG_PATH.open("r") as file:
        return json.load(file)