import urllib.request as request

from powertac_logfiles import data


def get_file_from_url(url, file_name):
    try:

        u = request.urlopen(url)

        meta = u.info()
        file_size = round(int(meta["Content-Length"]) / 1000000, 3)

        print('Downloading: {}, Size: {} mb'.format(file_name, file_size))

        with open(data.RAW_DATA_PATH + '/' + file_name, 'wb') as file:
            file.write(u.read())

    except ValueError as error:
        print(error)


def main():
    url = 'http://ts.powertac.org/log/PowerTAC_2018_Finals_1.tar.gz'
    file_name = 'test.tar.gz'
    get_file_from_url(url, file_name)


if __name__ == '__main__':
    main()
