![Image description](https://i.ibb.co/9vY7xCY/banner.png)


# py2bin

**py2bin** is a hassle-free, command-line-tool that allows you to easily convert a Python file into a binary file with a single line of code.

>py2bin is a streamlined version of and built from: [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/).

## py2bin vs PyInstaller?
- **minimal** command-line-interface
- **cleaner** output and file handling
- **constrained** functionality 

## Compatibility
- Mac OSX
- Python >= 3.6

## Dependencies
- [PyInstaller](https://github.com/pyinstaller/pyinstaller)
- [Click](https://github.com/pallets/click)

## Installation and Usage

|          	| Installation                                                                                                                          	| Usage                           	|
|----------	|---------------------------------------------------------------------------------------------------------------------------------------	|---------------------------------	|
| **Homebrew** 	| $ brew install dante-biase/x2appUtils/py2bin                                                                                          	| $ py2bin PY_FILE [OPTIONS]      	|
| **Manual**   	| $ git clone https://github.com/dante-biase/py2bin.git<br>$ cd py2bin<br>$ pip3 install -r requirements.txt<br>$ chmod +x py2bin.py 	| $ ./py2bin.py PY_FILE [OPTIONS] 	|

### PY_FILE
> specifies the py file to be converted into a binary, required

### [OPTIONS]
```
  -d, --destination_directory   TEXT    directory to create the binary in
  -o, --optimize                TEXT    compile with optimizations
  --help                                print this message and exit
```
### NOTES
1. the output binary will be named with the stem of `PY_FILE`
2. if `destination_directory` is not specified, the binary will be placed in the same directory as `PY_FILE`
