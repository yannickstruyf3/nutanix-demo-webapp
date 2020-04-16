from flask import Flask, url_for
from flask import render_template
import boto3
import json
import requests
import os
import socket
from config import Config
from googletrans import Translator

app = Flask(__name__)
config = Config()
translator = Translator()


@app.route("/")
@app.route("/index")
def index():
    # config = Config()
    urls = {
        "nutanix_logo": __get_image_url("nutanix_logo"),
        "nutanix_background": __get_image_url("nutanix_background"),
        "nutanix_favicon": __get_image_url("nutanix_favicon"),
    }
    return render_template(
        "index.html",
        title="Home",
        urls=urls,
        core_values=__translate_core_values(),
        rights_reserved=__translate_rights_reserved(),
        designed_by=__translate_designed_by(),
        # hostname=host_name,
        customer=config.CUSTOMER,
        info_dict=create_info_dict()
        # ip=host_ip,
    )


def create_info_dict():
    host_name = "unknown"
    host_ip = "unknown"
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    except:
        pass
    return {
        "Hostname": host_name,
        "IP": host_ip,
        "Datacenter": config.get("DATACENTER", None),
    }


def __translate_rights_reserved():
    return __translate(config.RIGHTS_RESERVED)


def __translate_designed_by():
    return __translate(config.DESIGNED_BY)


def __translate_core_values():
    core_values = config.get_core_values()
    source_language = config.SOURCE_LANGUAGE.lower()
    destination_language = config.DESTINATION_LANGUAGE.lower()
    if source_language == destination_language:
        return core_values
    translated_core_values = []
    for value in core_values:
        translated_core_values.append(__translate(value))
    return translated_core_values
    ##translate


def __translate(value, source_language=None, destination_language=None):
    if not source_language:
        source_language = config.SOURCE_LANGUAGE.lower()
    if not destination_language:
        destination_language = config.DESTINATION_LANGUAGE.lower()
    if source_language == destination_language:
        return value
    language_mapping = config.LANGUAGE_MAPPING
    return translator.translate(
        value,
        src=language_mapping.get(source_language),
        dest=language_mapping.get(destination_language),
    ).text


def __get_core_values():
    if config.USE_BUCKETS:
        url = __create_presigned_url("nutanix_core_values")
        return requests.get(url).json().get("values", [])
    return config.CORE_VALUES


def __get_image_url(image_key):
    if config.USE_BUCKETS:
        return __create_presigned_url()
    return url_for("static", filename=config.IMAGE_MAPPING.get(image_key))


def __create_presigned_url(object_name, expiration=3600):
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client(
        "s3",
        endpoint_url=config.ENDPOINT_URL,
        aws_access_key_id=config.ACCESS_KEY,
        aws_secret_access_key=config.SECRET_KEY,
    )
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": config.BUCKET, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=5000)
