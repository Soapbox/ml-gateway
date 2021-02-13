"""The blogs router implementation."""

import requests
from typing import Optional
from fastapi import APIRouter, HTTPException
from api.routers.utils import SUPPORTED_CATEGORICAL_FILTERS

router = APIRouter()

BLOGS_URL = "http://blogs:8500/blogs"


@router.get("")
def recommended_blogs_from_categories(
    first_category: str,
    second_category: Optional[str] = None,
):
    """
    Retrieves a list of recommended blog posts given categorical filters.

    Possible categorical filters are:
    1) Work
    2) Communication
    3) Growth
    4) Motivation
    """
    first_category = first_category.title()
    if first_category not in SUPPORTED_CATEGORICAL_FILTERS or first_category == "None":
        raise HTTPException(
            status_code=422,
            detail=f'The first_category "{first_category}" is not supported.',
        )

    if second_category is None or second_category == "":
        second_category = first_category

    second_category = second_category.title()
    if second_category not in SUPPORTED_CATEGORICAL_FILTERS or second_category == "None":
        raise HTTPException(
            status_code=422,
            detail=f'The second_category "{second_category}" is not supported.',
        )

    payload = {"first_category": first_category,
               "second_category": second_category}

    response = requests.get(BLOGS_URL, params=payload).json()
    return response
