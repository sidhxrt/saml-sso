from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from app.utils.samlutils import get_saml_client, generate_metadata
from saml2.client import Saml2Client
from saml2 import BINDING_HTTP_POST

router = APIRouter()

@router.get("/login")
async def login(saml_client: Saml2Client = Depends(get_saml_client)):
    """Initiate SAML login request."""
    try:
        reqid, reqinfo = saml_client.prepare_for_authenticate(
            requested_authn_context=None
        )
        print("Request Info:", reqinfo)  # Log reqinfo for debugging
        redirect_url = reqinfo.get("url")
        if not redirect_url:
            raise ValueError("Redirect URL is missing or None")
        return RedirectResponse(redirect_url)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Failed to initiate login: {error_details}")

@router.post("/acs")
async def acs(SAMLResponse: str = Form(...), saml_client: Saml2Client = Depends(get_saml_client)):
    """Handle SAML Response (ACS Endpoint)."""
    try:
        authn_response = saml_client.parse_authn_request_response(
            SAMLResponse, BINDING_HTTP_POST
        )
        user_info = authn_response.get_subject()
        return {"message": "Login successful", "user_info": user_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SAML Response parsing failed: {e}")

@router.get("/metadata")
async def metadata():
    """Return Service Provider Metadata as XML."""
    try:
        metadata_xml = generate_metadata()
        return Response(content=metadata_xml, media_type="application/xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate metadata: {str(e)}")