from os import system, chdir
from os.path import exists, join
from shutil import copytree, ignore_patterns

def install_pkg(info, out):
    pkg, version = info
    system("py -3.7 -m pip install  {}=={} >> {}".format(pkg, version, out))

### Copy Scriptfolder from Share

# Copy data to C:/Ausgabe_Skript
from_path = "C:\\Users\\Brian-PC\\Desktop\\Files"
to_path = "C:\\Ausgabe_Skript\\Script\\"

if not exists(to_path):
    copytree(from_path, to_path, ignore=ignore_patterns('*.pyc', 'tmp*', '__pycache__*'))

### Setup Python Enviroment

# Append cmd output to setup_output.txt
out = join(to_path, "setup_output.txt")

# Packages and version to install
packages = [
    ('--upgrade pip', '20.0.2'),
    ('--upgrade setuptools', '45.2.0'),
    ('--upgrade wheel', '0.34.2'),
    ('numpy', '1.15.2'),
    ('matplotlib',  '3.0.0'),
    ('pandas', '0.23.4'),
    ('PySimpleGui', '4.11.0'),
    ('xlrd', '1.1.0')
]

# Option to upgrade pip form local py file for 3.4
for package in packages:
    install_pkg(package, out)







