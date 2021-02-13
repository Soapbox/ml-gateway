"""The topic classification endpoints."""

import requests
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi import APIRouter
from api.db.schemas import TopicClassificationRequestSample

router = APIRouter()

CLASSIFICATION_URL = "http://classification:8500/classify"


@router.post("")
def single_topic_classification(
    sample: TopicClassificationRequestSample,
):  # pylint: disable=line-too-long
    """
    Classifies a sample to one of the following categories:
    1) Work
    2) Communication
    3) Growth
    4) Motivation
    5) None
    """

    data = jsonable_encoder(sample)
    response = requests.post(CLASSIFICATION_URL, json=data).json()
    return response


@router.post("/bulk")
def bulk_topic_classification(
    samples: List[TopicClassificationRequestSample],
):  # pylint: disable=line-too-long
    """
    Classify batches of samples to one of the following categories:
    1) Work
    2) Communication
    3) Growth
    4) Motivation
    5) None
    """

    encodedSamples = jsonable_encoder(samples)
    response = requests.post(CLASSIFICATION_URL +
                             "/bulk", json=encodedSamples).json()
    return response
