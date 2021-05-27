"""Common constants used throughout the routers module."""

from .agenda_template import router as agenda_template_router
from .blogs import router as blogs_router
from .next_steps import router as next_steps_router
from .topic_classification import router as topic_classification_router
from .topic_reclassification import router as topic_reclassification_router

# router configuration
ROUTERS = [
    next_steps_router,
    agenda_template_router,
    blogs_router,
    topic_classification_router,
    topic_reclassification_router,
]
PREFIXES = ["/entity", "/agenda_template",
            "/blogs", "/classify", "/reclassify"]
TAGS = [["entity"], ["agenda_template"], [
    "blogs"], ["classify"], ["reclassify"]]
