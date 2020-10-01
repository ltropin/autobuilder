import os
import time
import requests
import argparse
import configparser
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import pyqrcode

search_paths = [
    "diawi_uploader.ini",
    ".diawi_uploader.ini",
    os.path.expandvars("$HOME/.diawi_uploader.ini"),
    os.path.expandvars("$HOME/.config/diawi_uploader.ini"),
]


def bytes_to_str(val, fractional=1):
    suffixes = ["B", "KB", "MB", "GB", "TB"]
    mult = 1024
    idx = 0
    while val >= mult:
        val /= mult
        idx += 1
    return ("{0:." + str(fractional) + "f} {1}").format(val, suffixes[idx])


def upload(token: str, file_path: str):
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('--token', type=str)
    # argparser.add_argument('--qr', action='store_true')
    # argparser.add_argument("file", nargs="+", type=str)

    # args = argparser.parse_args()

    # token = None
    # if args.token is None:
    #     config = configparser.ConfigParser()
    #     cfg_path = None
    #     for search_path in search_paths:
    #         if os.path.exists(search_path):
    #             cfg_path = search_path
    #             break

    #     if cfg_path is None:
    #         print("Create diawi_uploader.ini config file first or specify token via command line")
    #         exit(1)
    #     elif cfg_path is not None:
    #         config.read(cfg_path)
    #         if not config.has_option("default", "token"):
    #             print("Token is not specified")
    #             exit(1)
    #         token = config.get("default", "token")
    # else:
    #     token = args.token

    # generate_qr = args.qr

    # links = {}
    # for path in args.file:
    # print("Uploading file {}...".format(file_path))

    multipart_encoder = MultipartEncoder(fields={
        "token": token,
        "wall_of_apps": "0",
        "find_by_udid": "0",
        "file": (os.path.basename(file_path), open(file_path, "rb"), 'application/octet-stream'),
    })

    events = 0

    def upload_callback(monitor):
        nonlocal events
        events += 1
        if events % 10 == 0:
            print("\r{0:>9s} / {1:9s} [{2:2.0f}%]".format(
                    bytes_to_str(monitor.bytes_read),
                    bytes_to_str(monitor.len),
                    monitor.bytes_read / monitor.len * 100), end='', flush=True)

    # multipart_encoder_monitor = MultipartEncoderMonitor(multipart_encoder, upload_callback)

    resp = requests.post("https://upload.diawi.com",
                            data=multipart_encoder,
                            headers={'Content-Type': multipart_encoder.content_type})

    js = resp.json()
    job_id = js["job"]
    # print()
    # print("Uploaded, processing...")

    while True:
        resp = requests.get("https://upload.diawi.com/status",
                            params={"token": token, "job": job_id})

        data = resp.json()
        msg = data["message"]

        if msg == "Ok":
            link = data["link"]
            return link

        time.sleep(1)

# for path in args.file:
# link = links[path]
# print(os.path.basename(path), link)


# if __name__ == "__main__":
#     main()