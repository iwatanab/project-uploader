"""main.py"""
import tempfile
import uuid

import requests
from fastapi import FastAPI, HTTPException, Request
from jose import jwt
from pydantic import BaseModel
from requests.exceptions import RequestException
from sw_product_lib import service
from sw_product_lib.service import RequestContext


app = FastAPI()


class JWTRequest(BaseModel):
    resource_slug: str
    workspace_member_slug: str
    product_slug: str
    product_api_key: str


class ResponseModel(BaseModel):
    response_id: str
    payload: dict


@app.middleware("http")
async def generate_sw_platform_client(request: Request, call_next):
    """Middleware for appending a RequestContext object.

    Set up a RequestContext object to use for making calls to the platform through
    service-lib.
    """
    ignores = {"/token"}
    if request.url.path in ignores:
        return await call_next(request)

    ctx = RequestContext.from_request(request=request)
    request.state.ctx = ctx
    return await call_next(request)


@app.get("/")
async def root():
    return {"msg": "services examples from Bend, OR."}


@app.post("/token")
async def get_jwt(r: JWTRequest):
    """Generate JWT to use with testing."""
    message = {
        "ResourceSlug": r.resource_slug,
        "WorkspaceMemberSlug": r.workspace_member_slug,
        "ProductSlug": r.product_slug,
        "ResourceTokenID": "abcd-1234",
        "ResourceEntitlements": [],
        "iss": "strangeworks-test-env",
    }

    token = jwt.encode(message, key=r.product_api_key)
    return token


@app.get("/quote", response_model=ResponseModel)
async def get_quote(req: Request):
    """Example of a most basic service

    This is an example of a product which retrieves a quote from an (arguably)
    influential or famous person. The service makes a call to an external service,
    then creates a job entry on the platform and uploads the quote as a file.
    """

    try:
        # Do the work which for this product is retrieving a random quote from an
        # external service.
        r = requests.get("https://zenquotes.io/api/random")

        # if a quote was successfully retrieved (we got this far), obtain the
        # request context and use it to first create a job entry. Since we already
        # have the quote, the status of the job is set to COMPLETED.
        ctx = req.state.ctx
        sw_job = service.create_job(
            ctx,
            status="COMPLETED",
            external_identifier=uuid.uuid4().hex,
        )

        # next, upload the result (the quote) to the platform. Use the `slug` from
        # the Job object returned in the previous call to associate the quote with
        # the job.
        with tempfile.NamedTemporaryFile(mode="+w") as tmp:
            tmp.write(r.text)
            tmp.flush()
            service.upload_job_file(
                ctx=ctx,
                job_slug=sw_job.slug,
                name="result.json",
                path=tmp.name,
                json_schema=None,
            )

        # you can return pretty much anything. we ar
        return ResponseModel(response_id=uuid.uuid4().hex, payload=sw_job.__dict__)

    except RequestException:
        raise HTTPException(status_code=500, detail="Service Unavailable")
