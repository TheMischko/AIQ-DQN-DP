import hashlib


def generate_md5(string):
    # Generate MD5 hash of the string
    hash_object = hashlib.md5(string.encode())
    hash_value = hash_object.hexdigest()

    return hash_value
