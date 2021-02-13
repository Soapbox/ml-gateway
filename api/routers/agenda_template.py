"""The endpoint for classifying calendar events."""

from typing import List, Optional
import requests
from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from api.db.schemas import AgendaTemplateRequestSample, AgendaTemplateResponseSample

CALENDAR_URL = "http://calendar:8500/agenda_template"

router = APIRouter()


# Calendar routes
@router.get("", response_model=List[AgendaTemplateResponseSample])
async def retrieve_agenda_templates(
    samples: List[AgendaTemplateRequestSample],
    callback: Optional[str] = Query(None, min_length=1),
):  # pylint: disable=line-too-long
    """Predicts the ideal agenda templates for calendar events."""
    if len(samples) == 0:
        return []

    data = jsonable_encoder(samples)
    response = requests.get(CALENDAR_URL, json=data, params={
                            "callback": callback}).json()
    return response
