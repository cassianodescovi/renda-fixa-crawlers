import os
from datetime import datetime
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError

from loggers import logger
from utils.files import path_builder


def save_on_s3(soup, configs: dict, local=False):
    """
    Save the HTML content to S3 or locally
    :param soup:
    :param configs:
    :param local:
    :return:
    """

    html_content = soup.prettify()

    if local:
        path = path_builder(configs, transaction="local_write", local=local)
        with open(path, "w", encoding="utf-8") as file:
            file.write(html_content)
        logger.info(f"File saved locally at {path}")
    else:
        # Save the HTML content to S3
        s3 = boto3.client("s3")
        bucket_name = "your-bucket-name"  # Replace with your bucket name
        s3_path = path_builder(
            configs, transaction="S3_write", local=local
        )  # Get the file name from the path

        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=s3_path,
                Body=html_content,
                ContentType="text/html",
            )
            logger.info(f"File saved to S3 at {bucket_name}/{s3_path}")
        except NoCredentialsError:
            logger("Credentials not available.")


def read_from_s3(path, local=False):
    """
    Read the file from S3 or locally
    :param path:
    :param local:
    :return:
    """

    if local:
        # Read the file locally
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            logger.info(f"File read locally from {path}")
            return content
        except FileNotFoundError:
            logger.info(f"The file {path} does not exist.")
            return None
    else:
        s3 = boto3.client("s3")
        bucket_name = "your-bucket-name"
        s3_path = os.path.basename(path)

        try:
            obj = s3.get_object(Bucket=bucket_name, Key=s3_path)
            content = obj["Body"].read().decode("utf-8")
            logger.info(f"File read from S3 at {bucket_name}/{s3_path}")
            return content
        except NoCredentialsError:
            logger.info("Credentials not available.")
            return None
        except s3.exceptions.NoSuchKey:
            logger.info(
                f"The file {s3_path} does not exist in the bucket {bucket_name}."
            )
            return None


def search_parser_files(parser_name: str, folder: Path, local: bool = True) -> list:
    """
    Search for the files with the parser name in the folder
    :param parser_name:
    :param folder:
    :param local:
    :return:
    """

    current_date = datetime.now().strftime("%Y%m%d")

    # List to store the found files
    found_files = []

    if local:
        # Iterate over the files in the local folder
        for file in folder.iterdir():
            # Check if the file name contains the current date and the parser name
            if current_date in file.name and parser_name in file.name:
                found_files.append(file)
    else:
        # Connect to S3
        s3 = boto3.client("s3")
        bucket_name = "your-bucket-name"

        # List the objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=str(folder))

        # Iterate over the files in the S3 bucket
        for obj in response.get("Contents", []):
            file = obj["Key"]
            # Check if the file name contains the current date and the parser name
            if current_date in file and parser_name in file:
                found_files.append(file)

    return found_files


if __name__ == "__main__":
    file = read_from_s3("data_bacen.html", local=True)
