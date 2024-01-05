# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import sys
import subprocess  # use Python executable (for pip usage)
from pathlib import Path  # Object-oriented filesystem paths since Python 3.4
import importlib


def install_package(package, params=''):
    py_exec = ensure_pip()

    if bpy.app.version[0] == 2 and bpy.app.version[1] < 91:
        update_pip(py_exec)
        
    if is_not_installed(package) or params == '--upgrade':
        try:
            command = [py_exec, '-m', 'pip', 'install', package] + params.split()
            print(f'Installing package {package} with "{" ".join(command)}"')

            output = subprocess.check_output((command))
            print(output)

        except subprocess.CalledProcessError as e:
            print(f"Couldn't install {package}")
            raise Exception(e.output)

        print(f"{package} installed")

def install_packages(packages, params):
    if len(packages) != len(params):
        raise Exception("Packages and params must be same length")
    for index, package in enumerate(packages):
        try:
            install_package(package, params[index])
        except Exception as e:
            print(f"Package '{package}' install failed with exception: {e}")

def upgrade_package(package, params):
    params = params.rstrip()
    params += ' --upgrade'
    install_package(package, params=params)

def is_not_installed(package):
    #https://stackoverflow.com/questions/1051254/check-if-python-package-is-installed
    if package in sys.modules:
        print(f"{package!r} already was imported")
    elif (spec := importlib.util.find_spec(package)) is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[package] = module
        spec.loader.exec_module(module)
        print(f"{package!r} has been imported")
    else:
        return True

def ensure_pip():
        # TODO check permission rights
        # TODO Windows ask for permission:
        # https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
        # TODO Is there a way to install packages without pip so uac is not required?

        # pip in Blender:
        # https://blender.stackexchange.com/questions/139718/install-pip-and-packages-from-within-blender-os-independently/
        # pip 2.81 issues: https://developer.blender.org/T71856

        # no pip enabled by default version < 2.81
        if bpy.app.version[0] == 2 and bpy.app.version[1] < 81:
            # find python binary OS independent (Windows: bin\python.exe; Linux: bin/python3.7m)
            py_path = Path(sys.prefix) / "bin"
            py_exec = str(next(py_path.glob("python*")))  # first file that starts with "python" in "bin" dir

            if subprocess.call([py_exec, "-m", "ensurepip"]) != 0:
                raise Exception("Couldn't activate pip.")

        # from 2.81 pip is enabled by default
        else:
            try:
                # will likely fail the first time, but works after `ensurepip.bootstrap()` has been called once
                import pip
                print("Pip imported")
            # pip not enabled
            except ModuleNotFoundError as e:
                # only first attempt will reach here
                print(f"Pip import failed with: {e}")
                print("Pip not activated, trying bootstrap()")
                try:
                    import ensurepip
                    ensurepip.bootstrap()
                except:  # catch *all* exceptions
                    e = sys.exc_info()[0]
                    raise Exception(f"bootstrap failed with: {e}")

                print("Pip activated!")
            # 2.81 >= Blender < 2.91
            if bpy.app.version[0] == 2 and bpy.app.version[1] < 91:
                py_exec = bpy.app.binary_path_python
            # (tested on 2.93 LTS & 3.3 LTS) Blender >= 2.91
            else:
                py_exec = sys.executable

        return py_exec

def update_pip(py_exec):
        # pip update
        try:
            output = subprocess.check_output([py_exec, '-m', 'pip', 'install', '--upgrade', 'pip'])
            print(output)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Couldn't update pip. Please restart Blender and try again. \n {e.output}")
        print("Pip has been updated")




# def get_header_files():
#     # https://blender.stackexchange.com/questions/81740/python-h-missing-in-blender-python#:~:text=Download%20and%20install%20the%20python,cd%20~%2FDownloads%2F
    
#     import sys
#     from sysconfig import get_paths
#     import tarfile 
#     import shutil
#     import os
#     from os import listdir
#     from os.path import isfile, join, isdir

#     #Get python version
#     py_version = sys.version.split()[0]

#     # Download python version
#     print("Downloading python")
#     url = f'https://www.python.org/ftp/python/{py_version}/Python-{py_version}.tgz'
#     import requests
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open("python", "wb") as file:
#             file.write(response.content)
#         print("Python downloaded successfully.")
#     else:
#         print(f"Failed to download Python. Status code: {response.status_code}")

#     #Unzip python
#     print("Unzipping python")
#     file = tarfile.open('python') 
#     file.extractall('./contents') 
#     file.close()
#     print("Python unzipped")

#     #Get include dir and contents
#     include_dir = get_paths()['include']
#     # include_dir =  os.path.dirname(include_dir)

#     include_dir_files = [join(include_dir, file) for file in os.listdir(include_dir)]


#     #Remove existing include directory files
#     for file in include_dir_files:
#         try:
#             shutil.rmtree(file)
#         except:
#             os.remove(file)

#     #Get downloaded include directory and contents
#     downloaded_include_path = f'./contents/Python-{py_version}/Include/'
#     downloaded_include_files = [join(downloaded_include_path, f) for f in listdir(downloaded_include_path)]

#     #Copy downloaded contents to include directory
#     for item in downloaded_include_files:
#         # TODO Fix directory copying not working
#         # TODO I think its possible to greatly simplify this by using just one shutil.copytree
#         if isdir(item):
#             copy_to = join(include_dir, os.path.basename(os.path.normpath(item)))
#             destination = shutil.copytree(item, copy_to)
#             print(f"DIRECTORY: {item} copied succesfully to {destination}")
#         if isfile(item):
#             destination = shutil.copy(item, include_dir)
#             print(f"FILE: {item} copied succesfully to {destination}")
    
#     #Remove downloaded files
#     os.remove('python')
#     shutil.rmtree('contents')

#     print("Python headers installed succesfully")
                
