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
- [py2x](https://github.com/dante-biase/py2x)

## Installation and Usage

|          	| Installation                                                                                                                          	| Usage                           	|
|----------	|---------------------------------------------------------------------------------------------------------------------------------------	|---------------------------------	|
| **Homebrew** 	| $ brew install dante-biase/x2x/py2bin                                                                                          	| $ py2bin PY_FILE [OPTIONS]      	|
| **Manual**   	| $ git clone https://github.com/dante-biase/py2bin.git<br>$ cd py2bin<br>$ pip3 install -r requirements.txt<br>$ chmod +x py2bin.py 	| $ ./py2bin.py PY_FILE [OPTIONS] 	|

### PY_FILE
> specifies the py file to be converted into a binary, required

### [OPTIONS]
```
  -r, --resources_directory     TEXT    directory that contains binary resources
  -d, --destination_directory   TEXT    directory to create the binary in
  -o, --optimize                TEXT    compile with optimizations
  --help                                print this message and exit
```
## Notes

### Resources
1. If your binary requires any resources, you must consolidate these files into a single directory - `resources_directory`
2. Install [py2x](https://github.com/dante-biase/py2x)

       $ pip3 install py2x
3. Add this import statement to any script that references resources you might need:
      
       from py2x import Resources
4. Update references:

   **EXAMPLE:** if you need to read a text file located within your `resources_directory`:
          
   change:
   
       text_file = open("path/to/resources/file.txt", "r")

   to:
   
       text_file = open(Resources.get("file.txt"), "r")`

5. Execute py2bin while making sure to pass the path to your `resources_directory` to the `-r` flag:
   
       py2bin main.py -r path/to/resources [OTHER OPTIONS]

### Output
1. the output binary will be named with the stem of `PY_FILE`
2. if `destination_directory` is not specified, the binary will be placed in the same directory as `PY_FILE`
