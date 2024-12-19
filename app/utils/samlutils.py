import os
from os.path import dirname, abspath, join
from saml2.client import Saml2Client
from saml2.config import Config
from saml2.metadata import create_metadata_string
import json

def load_saml_config_from_json():
    """Load SAML configuration from the config.json file."""
    config_path = join(dirname(dirname(abspath(__file__))), "config", "samlconfig.json")
    with open(config_path, "r") as f:
        saml_settings = json.load(f)

    # Load the configuration into the SAML client
    config_loader = Config()
    config_loader.load(saml_settings)
    return Saml2Client(config=config_loader)

def get_saml_client():
    """Create and return a SAML2 client using config from config.json."""
    return load_saml_config_from_json()

def generate_metadata():
    """Generate SAML metadata."""
    saml_client = get_saml_client()
    metadata = create_metadata_string(saml_client.config, None, 4, None, None)
    return metadata
