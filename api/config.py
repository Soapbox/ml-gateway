"""The configuration file to use for the project."""

import os

if os.environ.get("USE_PRODUCTION_ENV"):
    # Database Credentials
    db_private_ip = "<replace_me>"
    db_username = "<replace_me>"
    db_password = "<replace_me>"
    db_database_name = "<replace_me>"

    # AWS Credentials
    aws_public_key = "<replace_me>"
    aws_secret_key = "<replace_me>"
    aws_region = "<replace_me>"
    aws_bucket_name = "<replace_me>"

    # API Keys
    yelp_api_key = "rVQRrwc46ifXIGVrHwnk-wQRNvJCtgM_AdGAIUliu0fgEFIRP99Nybz2S01moBqYBxI4E9YH1maWlEA0itZf41Zb8vxioLzRRSyKOtTn00B_SmyNkUx-Nw6ft6NVXXYx"  # pylint: disable=line-too-long

    # Signed request
    signed_request_key = "secret"
    signed_request_signature_header_name = "GoodTalk-Signature"
    signed_request_algorithm_header_name = "GoodTalk-Algorithm"
else:
    # Database Credentials
    db_private_ip = "db"
    db_username = "ml"
    db_password = "secret"
    db_database_name = "machine_learning"

    # AWS Credentials
    aws_public_key = "AKIAT7WYARTBVVKWLXO2"
    aws_secret_key = "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"
    aws_region = "us-west-1"
    aws_bucket_name = "soapbox-v5-local"

    # API Keys
    yelp_api_key = "rVQRrwc46ifXIGVrHwnk-wQRNvJCtgM_AdGAIUliu0fgEFIRP99Nybz2S01moBqYBxI4E9YH1maWlEA0itZf41Zb8vxioLzRRSyKOtTn00B_SmyNkUx-Nw6ft6NVXXYx"  # pylint: disable=line-too-long

    # Signed request
    signed_request_key = "secret"
    signed_request_signature_header_name = "GoodTalk-Signature"
    signed_request_algorithm_header_name = "GoodTalk-Algorithm"
