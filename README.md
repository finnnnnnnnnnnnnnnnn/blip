# Blip
A script to easily use pip in Blender addons.
There are 2 important functions:

 - install_package(package, params)   
    Installs the specificed package with the specified params, which are the same string they would be with pip in the command line, to specify package version put that in the package param, eg. ```install_package('package==1.0.0', 'params')```

 - install_packages(\[package], \[params])   
    Same as install package, but it installs multiple packages sequentially. Both of the inputs should be lists of the same length, and if a package has no params, it should just be an empty string
## Todo
 - Add NumesSanguis as an author in toml/add credit to him in files
 - Check to make sure license stuff is all good
 - Write the function install_packages better (maybe a dict would be better for input?)
 - Write a better api for params, replace params as string with funcion params, like ```install_module('package', extra-index-url='https://pypi.org/simple/')```
 - Get gcc to find Python.h for building certain packages. Currently get_header_files is a failed attempt at this