from io import BytesIO

from PIL import Image

from amazonstorage.client import bucket_name, minio_client


def image_upload(file, format, name):
    img = Image.open(file)
    with BytesIO() as flow:
        img.save(flow, format=format)
        flow.seek(0)
        ret = minio_client.put_object(
            bucket_name, name, flow, flow.getbuffer().nbytes, content_type="image/jpeg"
        )

        return ret


def delete_image_file(url):
    name = url.rpartition("/")[-1]
