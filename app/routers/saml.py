from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from app.utils.samlutils import get_saml_client
from saml2.client import Saml2Client

router = APIRouter()

@router.get("/saml/metadata")
async def metadata():
    """Serve the metadata to the client."""
    metadata = get_saml_client().metadata()
    return metadata

@router.get("/saml/login")
async def login(saml_client: Saml2Client = Depends(get_saml_client)):
    """Initiate SAML login request."""
    reqid, reqinfo = saml_client.prepare_for_authenticate()
    redirect_url = reqinfo["url"]
    return RedirectResponse(redirect_url)

@router.post("/saml/acs")
async def acs(request: dict, saml_client: Saml2Client = Depends(get_saml_client)):
    """Handle the SAML response."""
    try:
        authn_response = saml_client.parse_authn_request_response(
            request["SAMLResponse"],
            entity.BINDING_HTTP_POST
        )
        user_info = authn_response.get_subject()
        return {"user_info": user_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SAML Response parsing failed: {e}")
