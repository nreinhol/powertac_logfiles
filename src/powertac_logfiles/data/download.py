import urllib.request as request

from powertac_logfiles import data
from powertac_logfiles import output


def get_file_from_url(index, url, file_name, download_folder=None):
    try:
        print(url)
        u = request.urlopen(url)
        meta = u.info()
        file_size = round(int(meta["Content-Length"]) / 1000000, 3)
        output.print_download_info(index, url, file_size, local=True)

        download_folder_path = data.RAW_DATA_PATH if download_folder is None else download_folder
        with open(download_folder_path + file_name, 'wb') as file:
            file.write(u.read())

    except ValueError as error:
        print(error)
