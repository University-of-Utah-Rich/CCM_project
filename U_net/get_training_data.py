import zipfile
import requests
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download&confirm=1"

    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc='Training Data') as t:
        CHUNK_SIZE = 32768
        chunks = 1
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    t.update_to(b=chunks, bsize=CHUNK_SIZE, tsize=1.81e9)
                    chunks = chunks + 1

    
def extract_training_data(src, dest):
    with zipfile.ZipFile(src, 'r') as zip_ref:
        zip_ref.extractall(dest)

if __name__ == "__main__":
    print('Downloading training data')
    file_id = '1IWHsyye3yQpAj-QskOKU_rRKvt_OONxN'
    destination = './train.zip'
    download_file_from_google_drive(file_id, destination)
    print('Extracting data')
    extract_training_data(destination, './training_data')
    print('Done')