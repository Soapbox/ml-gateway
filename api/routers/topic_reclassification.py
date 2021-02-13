"""The topic reclassification endpoint for retraining individual Soapbox models."""

import requests
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from api.db.schemas import TopicReclassificationRequestSample

router = APIRouter()

RECLASSIFICATION_URL = "http://classification:8500/reclassify"


@router.post("")
def bulk_topic_reclassification(
    samples: List[TopicReclassificationRequestSample],
):  # pylint: disable=line-too-long
    """
    Reclassifies a batch of samples and reconsiders them as training data for
    each topic classifier.
    """

    data = jsonable_encoder(samples)
    response = requests.post(RECLASSIFICATION_URL, json=data).json()
    return response
