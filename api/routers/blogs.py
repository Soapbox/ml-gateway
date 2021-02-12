"""The blogs router implementation."""

import random
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from api.db import retrieve_database_connection
from api.db.models import Blogs
from api.db.ops import get_blogs
from api.routers.utils import SUPPORTED_CATEGORICAL_FILTERS

router = APIRouter()


@router.get("")
def recommended_blogs_from_categories(
    first_category: str,
    db: Session = Depends(retrieve_database_connection),
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

    potential_blogs_first_category = get_blogs_for_category(db, first_category)
    potential_blogs_second_category = get_blogs_for_category(db, second_category)

    first_blog_post = None
    second_blog_post = None

    if len(potential_blogs_first_category) > 0:
        first_blog_post = random.choice(potential_blogs_first_category)

    if len(potential_blogs_second_category) > 0:
        if first_blog_post:
            potential_blogs_second_category = [
                blog_post
                for blog_post in potential_blogs_second_category
                if blog_post.title != first_blog_post.title
            ]  # pylint: disable=line-too-long

        second_blog_post = random.choice(potential_blogs_second_category)

    return [serialize_blog(blog) for blog in [first_blog_post, second_blog_post]]


def serialize_blog(blog: Optional[Blogs]):
    """
    Serializes the blog information.

    Args:
        blog: The blog information.

    Returns:
        A dictionary containing the serialized blog.
    """
    serialized_blog = {
        "title": blog.title if blog else "",
        "description": blog.description if blog else "",
        "link": blog.link if blog else "",
        "published_date": blog.published_date if blog else "",
        "image": blog.image if blog else "",
        "categories": (blog.categories if blog else "")
        .replace("_", " ")
        .title()
        .split(","),
        "author": blog.author if blog else "",
    }
    return serialized_blog


def get_mapped_categories(category: str):
    """Creates a mapping between the model's item category mappings against blog post tags
    and returns the mapping of a given category.

    Args:
        category: The category to retrieve its mapping with the model.

    Returns:
        The corresponding model mapping of a given category.
    """
    mapping = {
        "Communication": [
            "Communication",
            "Remote_teams",
            "Difficult_conversations",
            "Feedback",
            "Productive_meetings",
            "Management_skills",
            "New_manager",
            "Senior_manager",
            "Change_management",
        ],
        "Growth": ["Team_tools", "New_manager", "Senior_manager", "Growth"],
        "Motivation": ["Employee_motivation", "Employee_engagement"],
        "Work": ["Time_management", "Accountability", "Building_trust", "Work"],
    }

    return mapping[category]


def get_blogs_for_category(db: Session, category: str):
    """Retrieves the blog post information based on a given category.

    Args:
        cur: The database cursor
        category: The category to filter the blog posts with.

    Returns:
        The list of blogs that match a given category.
    """
    categories = get_mapped_categories(category)
    return get_blogs(db, categories=categories)
