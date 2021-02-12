# """The topic classification endpoints."""

# import heapq
# from typing import List
# from fastapi import APIRouter, Depends
# from fastai.text import load_learner
# from sqlalchemy.orm import Session
# from api.db.ops import get_soapbox_classification_model
# from api.db.schemas import TopicClassificationRequestSample
# from api.util import CONTAINER_MODEL_DIR
# from api.routers.utils import (
#     BASE_CLASSIFICATION_MODEL_NAME,
#     is_meaningful,
#     add_custom_classification_model,
# )
# from api.db import retrieve_database_connection

# router = APIRouter()

# original_learner = load_learner("api/models", "classification.pkl")
# base_learner = load_learner(CONTAINER_MODEL_DIR, BASE_CLASSIFICATION_MODEL_NAME)


# @router.post("")
# def single_topic_classification(
#     sample: TopicClassificationRequestSample,
#     db: Session = Depends(retrieve_database_connection),
# ):  # pylint: disable=line-too-long
#     """
#     Classifies a sample to one of the following categories:
#     1) Work
#     2) Communication
#     3) Growth
#     4) Motivation
#     5) None
#     """
#     if sample.soapbox_id:
#         return get_single_classification(sample, db)

#     return get_single_classification_no_soapbox_id(sample)


# @router.post("/bulk")
# def bulk_topic_classification(
#     samples: List[TopicClassificationRequestSample],
#     db: Session = Depends(retrieve_database_connection),
# ):  # pylint: disable=line-too-long
#     """
#     Classify batches of samples to one of the following categories:
#     1) Work
#     2) Communication
#     3) Growth
#     4) Motivation
#     5) None
#     """
#     classifications_response = []

#     for sample in samples:
#         classifications_response.append(single_topic_classification(sample, db))

#     return classifications_response


# def get_single_classification_no_soapbox_id(sample: TopicClassificationRequestSample):
#     """
#     Gets the classification for a sample without a unique Soapbox ID.

#     Parameters:
#         sample: The sample to classify.

#     Returns:
#         The response containing the most probable prediction of the sample text.
#     """
#     response = {"sample": sample.sample}
#     if sample.id:
#         response["id"] = sample.id

#     if sample.soapbox_id:
#         response["soapbox_id"] = sample.soapbox_id

#     if is_meaningful(sample.sample):
#         global original_learner  # pylint: disable=global-statement

#         if not original_learner:
#             original_learner = load_learner("api/models", "classification.pkl")

#         response["categories"] = get_classes(
#             (original_learner.predict(sample.sample)[2]).tolist()
#         )
#     else:
#         response["categories"] = []

#     return response


# def get_single_classification(sample: TopicClassificationRequestSample, db: Session):
#     """
#     Gets the classification for a single item.

#     Parameters:
#         sample: The sample to classify.
#         db: The database session.

#     Returns:
#         The response containing the most probable prediction of the sample text.
#     """
#     response = {"sample": sample.sample}
#     if sample.id:
#         response["id"] = sample.id

#     if sample.soapbox_id:
#         response["soapbox_id"] = sample.soapbox_id

#     add_custom_classification_model(db, sample.soapbox_id)
#     learner = get_learner(sample, db)
#     categories = get_classes((learner.predict(sample.sample)[2]).tolist())
#     response["categories"] = categories if is_meaningful(sample.sample) else []
#     return response


# def get_learner(sample: TopicClassificationRequestSample, db: Session):
#     """
#     Retrieves the classification learner for the requested Soapbox.

#     Parameters:
#         sample: The request sample.
#         db: The database session.

#     Returns:
#         The classification learner for the given Soapbox ID.
#     """
#     classification_model = get_soapbox_classification_model(db, sample.soapbox_id)
#     if classification_model.model_pkl_file == BASE_CLASSIFICATION_MODEL_NAME:
#         global base_learner  # pylint: disable=global-statement

#         if not base_learner:
#             base_learner = load_learner(
#                 CONTAINER_MODEL_DIR, BASE_CLASSIFICATION_MODEL_NAME
#             )

#         return base_learner

#     return load_learner(CONTAINER_MODEL_DIR, classification_model.model_pkl_file)


# def get_classes(class_dist):
#     """
#     Retrieves the word-equivalent classes given the probabilities.

#     Parameters:
#         class_dist: The probabilities of each of the classes.

#     Returns:
#         The list of word equivalent strings filtered based on their probabilities.
#     """
#     ret = []
#     classes = ["Communication", "Growth", "Motivation", "None", "Work"]
#     sorted_biggest = heapq.nlargest(2, class_dist)

#     if classes[class_dist.index(sorted_biggest[0])] == "None":
#         return ret

#     for x in sorted_biggest:
#         if x > 0.20:
#             index = class_dist.index(x)
#             if classes[index] != "None":
#                 ret.append([classes[index]][0])

#     return ret
