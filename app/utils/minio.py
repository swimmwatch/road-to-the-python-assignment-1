from io import BytesIO

from PIL import Image

from amazonstorage.client import bucket_name, minio_client


def get_flow_in_format_and_write(file, format, name):
    img = Image.open(file)
    with BytesIO() as flow:
        img.save(flow, format=format)
        flow.seek(0)
        ret = minio_client.put_object(
            bucket_name, name, flow, flow.getbuffer().nbytes
        )  # не смог вынести в отдельную функцию изза потока
        return ret


def delete_image_file(url):
    name = url.rpartition("/")[-1]
