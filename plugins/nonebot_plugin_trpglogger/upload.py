import boto3
from botocore import UNSIGNED
from botocore.client import Config


def upload_file(
    file_name,
    bucket,
    object_name=None,
):

    if object_name is None:
        object_name = file_name

    s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

    response = s3_client.upload_file(file_name, bucket, object_name)

    return response


if __name__ == "__main__":
    file_name = "group_1026597971_1613984504.txt"
    print(upload_file(file_name, "dicelogger"))
