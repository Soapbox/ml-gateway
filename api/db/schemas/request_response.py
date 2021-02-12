"""Schemas for request and response objects made to the API."""

from typing import Optional
from pydantic import BaseModel


class Sample(BaseModel):  # pylint: disable=too-few-public-methods
    """The base request class."""

    id: Optional[int] = None
    sample: str


class TopicClassificationRequestSample(Sample):  # pylint: disable=too-few-public-methods
    """The class when making a topic classification request."""

    soapbox_id: Optional[int] = None


class TopicReclassificationRequestSample(
    Sample
):  # pylint: disable=too-few-public-methods
    """The request representing a topic reclassification sample."""

    sample: str
    category: str
    soapbox_id: int
    item_id: int


class AgendaTemplateRequestSample(BaseModel):  # pylint: disable=too-few-public-methods
    """The request representing an agenda template request."""

    id: str
    event_name: str
    event_description: str
    num_attendees: int
    is_recurring: bool


class AgendaTemplateResponseSample(
    AgendaTemplateRequestSample
):  # pylint: disable=too-few-public-methods
    """The response representing an agenda template response."""

    agenda_template_id: Optional[int]
    agenda_template_name: str
