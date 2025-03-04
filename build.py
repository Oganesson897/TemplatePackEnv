#!/usr/bin/env python3

"""build client & server bundles"""

import argparse
import os
import sys
import shutil
import subprocess
import zipfile
import requests
import json

from pathlib import Path

from build.download import start

def parse_args():
    parser = argparse.ArgumentParser(prog="build", description=__doc__)
    parser.add_argument("--clean", action="store_true",
                        help="clean output dirs")
    parser.add_argument("-c", "--client", action="store_true",
                        help="only builds the client pack")
    return parser.parse_args()

def packwiz():
    if os.name == 'posix':
        subprocess.run(['chmod', '+x', './packwiz'], check=True)
        return './packwiz'
    if os.name == 'nt':
        return 'packwiz.exe'

basePath = os.path.normpath(os.path.realpath(__file__)[:-8])
packwizName = packwiz()

def build(args):
    os.makedirs('./buildOut/', exist_ok=True)
    Path("index.toml").touch()

    if args.clean:
        shutil.rmtree(basePath + "/buildOut",
                      ignore_errors=True)
        sys.exit(0)

    refresh()
    export_client_pack()
    export_cleanroom_pack()

    if args.client:
        return

    export_modlist()
    export_server_pack()

def refresh():
    subprocess.run([packwizName, 'refresh'], check=True)

def export_client_pack():
    print("Client Pack Exporting")
    subprocess.run([packwizName, 'curseforge', 'export', '-o', 'client.zip'], check=True)
    shutil.copy('./client.zip', './buildOut/')
    os.remove('./client.zip')
    print("Client Pack Export Done")

def export_server_pack():
    print("Server Pack Exporting")
    server_pack = "server.zip"

    start()

    shutil.copy("LICENSE", "build/server/LICENSE")

    os.chdir("build/server")
    subprocess.run(['java', '-jar', 'packwiz-installer-bootstrap.jar', '-s', 'server', '../../pack.toml'], check=True)

    with zipfile.ZipFile(server_pack, 'w') as zipf:
        for folder in ['config', 'groovy', 'libraries', 'mods', 'structures']:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start='.')
                    zipf.write(file_path, arcname)

        for file in ['launch.sh', 'forge-1.12.2-14.23.5.2860.jar', 'LICENSE', 'minecraft_server.1.12.2.jar']:
            zipf.write(file, file)

    os.chdir("../..")
    shutil.move(f"build/server/{server_pack}", f"buildOut/{server_pack}")
    print("Server Pack Export Done")

def export_cleanroom_pack():
    print("Cleanroom Pack Exporting")

    response = requests.get("https://api.github.com/repos/CleanroomMC/Cleanroom/releases/latest")
    if response.status_code == 200:
        release_data = response.json()
        assets = release_data.get("assets", [])
        if assets:
            download_url = assets[-1].get("browser_download_url")
            if download_url:
                file_name = "cleanroom.zip"
                print(f"Downloading from {download_url}...")
                file_response = requests.get(download_url, stream=True)
                if file_response.status_code == 200:
                    with open(file_name, "wb") as file:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    print(f"Downloaded to {file_name}.")
                else:
                    print(f"Failed to download the file: {file_response.status_code}")
            else:
                print("No download URL found in the latest asset.")
        else:
            print("No assets found in the latest release.")
    else:
        print(f"Failed to fetch release data: {response.status_code}")

    cleanroom = "cleanroom.zip"

    shutil.copy("LICENSE", "build/cleanroom/LICENSE")

    os.chdir("build/cleanroom")
    subprocess.run(['java', '-jar', 'packwiz-installer-bootstrap.jar', '../../pack.toml'], check=True)

    os.chdir("..")
    with zipfile.ZipFile(cleanroom, 'w') as zipf:
        for folder in os.walk("cleanroom"):
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start='.')
                    zipf.write(file_path, arcname)

        for file in ['LICENSE']:
            zipf.write(file, file)

    os.chdir("../..")
    shutil.move(f"build/cleanroom/{cleanroom}", f"buildOut/{cleanroom}")
    print("Cleanroom Pack Export Done")

def export_modlist():
    print("Modlist Exporting")
    result = subprocess.run([packwizName, 'list'], capture_output=True, encoding='utf-8').stdout.strip().split('\n')
    with open(basePath + "/buildOut/modlist.html", "w") as file:
        data = "<html><body><h1>Modlist</h1><ul>"
        for mod in result:
            data += "<li>" + mod + "</li>"
        data += "</ul></body></html>"
        file.write(data)
    print("Modlist Export Done")


if __name__ == "__main__":
    build(parse_args())