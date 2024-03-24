import boto3
import tensorflow as tf


def load_model():
    print("=========Model loaded successfully========")
    return tf.keras.models.load_model("ml_models/pdc_model_v3.h5")


def create_db_client(aws_kwargs: dict):
    client = boto3.client(
        "dynamodb",
        **aws_kwargs,
    )
    print("=========Dynamodb client created successfully========")

    return client


def create_db_resource(aws_kwargs: dict):
    resource = boto3.resource("dynamodb", **aws_kwargs)
    print("=========Dynamodb resource created successfully========")

    return resource


def create_s3_client(aws_kwargs: dict):
    client = boto3.client(
        "s3",
        **aws_kwargs,
    )
    print("=========S3 client created successfully========")

    return client

