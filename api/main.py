"""Main entrypoint for the ML API."""

import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .routers import ROUTERS, PREFIXES, TAGS

app = FastAPI()


def import_routers():
    """Imports routers to expose to the main application."""
    for router, prefix, tag in zip(ROUTERS, PREFIXES, TAGS):
        app.include_router(router, prefix=prefix, tags=tag)


import_routers()


def customize_openapi_schema():
    """
    Configures the documentation layout.

    Returns:
        An OpenAPI schema.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Machine Learning API", version="1.0.0", description="", routes=app.routes
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://soapbox-v5.s3.us-west-1.amazonaws.com/soapbox-1/S2EG7qzgTR0dpRTOrZxVBwKzJIkXGC3b2wjtoDER.png"  # pylint: disable=line-too-long
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


if os.environ.get("USE_PRODUCTION_ENV"):
    app.openapi_url = ""
else:
    app.openapi_schema = customize_openapi_schema()
