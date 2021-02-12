"""Common constants used throughout the routers module."""

from .agenda_template import router as agenda_template_router
# from .blogs import router as blogs_router
from .next_steps import router as next_steps_router

# router configuration
ROUTERS = [
    next_steps_router,
    agenda_template_router,
]
PREFIXES = ["/entity", "/agenda_template"]
TAGS = [["entity"], ["agenda_template"]]
