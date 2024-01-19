from .constants import acceptable_file_formats


def construct_url_for_image(storage_endpiont: str, bucket_name: str, file_name: str):
    return "http://" + storage_endpiont + ":9000" + "/" + bucket_name + "/" + file_name


def convert_format_suffix(file_name, format):
    new_neme = file_name.rpartition(".")[0] + "." + format.lower()
    return new_neme


def check_format_valid(format):
    return format in acceptable_file_formats
