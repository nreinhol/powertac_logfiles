import urllib.request as request

from powertac_logfiles import data
from powertac_logfiles import output


def get_file_from_url(index, url, file_name):
    try:
        u = request.urlopen(url)
        meta = u.info()
        file_size = round(int(meta["Content-Length"]) / 1000000, 3)

        output.print_download_info(index, url, file_size, local=True)

        with open(data.RAW_DATA_PATH + file_name, 'wb') as file:
            file.write(u.read())

    except ValueError as error:
        print(error)
