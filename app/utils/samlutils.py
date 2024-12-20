from saml2.config import Config
from saml2.client import Saml2Client
from saml2.metadata import entity_descriptor
from app.utils.config_loader import load_saml_config

def get_saml_client():
    """Create and return a SAML2 client using loaded configurations."""
    saml_config = load_saml_config()
    config_loader = Config()
    config_loader.load(saml_config)
    return Saml2Client(config=config_loader)

def generate_metadata():
    """Generate and return SP metadata XML."""
    saml_client = get_saml_client()
    sp_metadata = entity_descriptor(saml_client.config)
    return sp_metadata.to_string()
