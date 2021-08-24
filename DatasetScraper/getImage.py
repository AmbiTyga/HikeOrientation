import requests
import shutil
import os


def downloadImage(url, filepath, filename):
    """
    Download from url, save to the filepath with filename
    """

    r = requests.get(url, stream=True)
    destination = os.path.join(filepath, filename)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(destination, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        return filename
    else:
        return url
