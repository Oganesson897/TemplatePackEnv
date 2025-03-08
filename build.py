#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import subprocess

basePath = os.path.normpath(os.path.realpath(__file__)[:-8])

def packwiz():
    os.chdir(os.path.join(basePath, 'common'))
    if os.name == 'posix':
        subprocess.run(['chmod', '+x', './packwiz'], check=True)
        return './packwiz'
    if os.name == 'nt':
        return 'packwiz.exe'

packwizName = packwiz()

def build():
    os.makedirs('./buildOut/', exist_ok=True)
    Path("index.toml").touch()

    forge()
    cleanroom()


def forge():
    print("Forge Pack Exporting")
    copy('./common', './forge')
    # Run packwiz
    os.chdir('forge')
    refresh()
    subprocess.run([packwizName, 'curseforge', 'export', '-o', 'forge.zip'], check=True)
    shutil.copy('./forge.zip', './buildOut/')

def cleanroom():
    print("Cleanroom Pack Exporting")
    copy('./common', './cleanroom')
    # Run packwiz
    os.chdir('cleanroom')
    refresh()
    subprocess.run([packwizName, 'curseforge', 'export', '-o', 'cleanroom.zip'], check=True)
    shutil.move('./cleanroom.zip', './buildOut/')

def refresh():
    subprocess.run([packwizName, 'refresh'], check=True)

def copy(src_dir, dst_dir):
    for src_dir_path, dirs, files in os.walk(src_dir):
        dst_dir_path = src_dir_path.replace(src_dir, dst_dir, 1)

        if not os.path.exists(dst_dir_path):
            os.makedirs(dst_dir_path)
        
        for file_ in files:
            src_file = os.path.join(src_dir_path, file_)
            dst_file = os.path.join(dst_dir_path, file_)
            if not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_dir_path)
            else:
                print(f"Pass: {dst_file}")

if __name__ == "__main__":
    build()