"""Named entity recognition endpoints for recognizing names and dates."""

import requests
from fastapi import APIRouter
from api.db.schemas import Sample

NEXT_STEPS_SERVICE_URL = "http://next-steps:8500/entity"

router = APIRouter()


@router.get("")
async def retrieve_next_step_entities(sample: Sample):
    """Finds name and date entities given a sample."""

    data = {"sample": sample.sample}
    response = requests.get(NEXT_STEPS_SERVICE_URL, json=data).json()
    return response
