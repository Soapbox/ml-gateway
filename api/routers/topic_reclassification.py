# """The topic reclassification endpoint for retraining individual Soapbox models."""

# from typing import List
# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from api.db.models import ClassificationItems
# from api.routers.utils import (
#     SUPPORTED_CATEGORICAL_FILTERS,
#     add_custom_classification_model,
# )
# from api.db import retrieve_database_connection
# from api.db.ops import get_classification_categories, get_item, update_item, add_item
# from api.db.schemas import TopicReclassificationRequestSample

# router = APIRouter()


# @router.post("")
# def bulk_topic_reclassification(
#     samples: List[TopicReclassificationRequestSample],
#     db: Session = Depends(retrieve_database_connection),
# ):  # pylint: disable=line-too-long
#     """
#     Reclassifies a batch of samples and reconsiders them as training data for
#     each topic classifier.
#     """
#     for sample in samples:
#         if sample.category.title() not in SUPPORTED_CATEGORICAL_FILTERS:
#             raise HTTPException(
#                 status_code=422,
#                 detail=f'The category "{sample.category}" is not supported.',
#             )

#         get_single_reclassification(sample, db)


# def get_single_reclassification(sample: TopicReclassificationRequestSample, db: Session):
#     """
#     Processes a reclassification sample and updates the database accordingly.

#     Parameters:
#         db: The database session.
#         sample: A sample that needs to be reclassified.
#     """
#     classification_categories = get_classification_categories(db)
#     for classification_category in classification_categories:
#         if classification_category.category == sample.category.title():
#             category_id = classification_category.id
#             break

#     item = get_item(db, sample.item_id, sample.soapbox_id)
#     if item:
#         update_item(db, item, sample.sample, category_id)
#     else:
#         add_custom_classification_model(db, sample.soapbox_id)
#         item = ClassificationItems(
#             text_item=sample.sample,
#             category_id=category_id,
#             item_id=sample.item_id,
#             soapbox_id=sample.soapbox_id,
#             is_trained=False,
#         )
#         add_item(db, item)
