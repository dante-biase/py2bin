#!/usr/local/bin/python3

from os import getcwd, mkdir, chdir, remove
from shutil import rmtree, copy2
from subprocess import call

import click

from callbacks import *


@click.command()
@click.argument("py_file",
                callback=check_py_file)
@click.option("-d", "--destination_directory",
              default="bin",
              callback=check_destination_directory,
              help="directory to create the binary in")
@click.option("-o", "--optimize",
			  is_flag=True,
              help="compile with optimizations")
def main(py_file, destination_directory, optimize):

	cwd = getcwd()  # save copy of current working directory to create absolute path in case of runtime error

	try:
		# -------------------------------------------- setup binary variables ---------------------------------------------
		py_file = Path(py_file)
		binary_name = py_file.stem
		binary_target_path = f"{destination_directory}/{binary_name}"

		# ------------------------------------------- check binary target path --------------------------------------------
		if exists(binary_target_path):
			overwrite = ''
			while not (overwrite == 'y' or overwrite == 'n'):
				overwrite = str(input(f"{binary_target_path} already exists. Replace? [y/n] "))

			if overwrite == 'y':
				remove(binary_target_path)
			else:
				exit(0)
		
		# --------------------- create binary by isolating PyInstaller output in temporary directory ----------------------
		mkdir("temp")

		# copy py file to temp to contain creation of __pycache__ after calling pyinstaller
		copy2(py_file.absolute(), "temp")
		
		chdir("temp")
		if optimize:
			call(["python3", "-OO", "-m", "PyInstaller", py_file.name, "--onefile"])
		else:
			call(["pyinstaller", py_file.name, "--onefile"])
		
		chdir("..")

		# ------------------------------------- extract binary to target destination --------------------------------------
		copy2(f"temp/dist/{binary_name}", binary_target_path)

		# ------------------------------------------------- cleanup ----------------------------------------------------
		rmtree("temp")

		# --------------------------------------------- show binary in finder ---------------------------------------------
		call(["open", "-R", binary_target_path])

	except Exception as error:	# TODO: specify Exception

		# ---------------------------------------- cleanup on error before exit ----------------------------------------
		bin_directory = f"{cwd}/bin"
		if exists(bin_directory):
			rmtree(bin_directory)

		temp_directory = f"{cwd}/temp"		
		if exists(temp_directory):
			rmtree(temp_directory)

		raise Exception(repr(error))


if __name__ == "__main__":
	main()
