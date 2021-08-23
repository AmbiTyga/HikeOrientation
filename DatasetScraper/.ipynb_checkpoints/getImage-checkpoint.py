import requests 
import shutil

def downloadImage(url,filename):
    r = requests.get(url, stream = True)
    
    if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return filename
    else:
        return url