#!/usr/local/bin/python3

from os import getcwd, chdir, remove
from os.path import dirname, exists
from shutil import copy2, rmtree, copytree
from subprocess import call
from tempfile import mkdtemp

import click

from callbacks import *


@click.command()
@click.argument("py_file",
                callback=check_py_file)
@click.option("-d", "--destination_directory",
              default=None,
              callback=check_destination_directory,
              help="directory to create the binary in")
@click.option("-o", "--optimize",
			  is_flag=True,
              help="compile with optimizations")
def main(py_file, destination_directory, optimize):

	owd = getcwd()  # save copy of current working directory to create absolute path in case of runtime error
	
	temporary_directory = mkdtemp()

	try:
		# -------------------------------------------- setup binary variables ---------------------------------------------
		py_file = Path(py_file)
		py_file_parent_directory = Path(dirname(py_file.absolute()))
		binary_name = py_file.stem
		if not destination_directory:
			binary_target_path = f"{py_file_parent_directory.absolute()}/{binary_name}"
		else:
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
		copytree(py_file_parent_directory.absolute(), f"{temporary_directory}/{py_file_parent_directory.name}")
		chdir(temporary_directory)

		if optimize:
			call([
				"python3", "-OO", "-m", "PyInstaller", f"{py_file_parent_directory.name}/{py_file.name}", "--onefile", 
				"--hidden-import", "pkg_resources.py2_warn"
			])
		else:
			call([
				"pyinstaller", f"{py_file_parent_directory.name}/{py_file.name}", "--onefile", "--hidden-import", 
				"pkg_resources.py2_warn"
			])
		
		chdir(owd)

		# ------------------------------------- extract binary to target destination --------------------------------------
		copy2(f"{temporary_directory}/dist/{binary_name}", binary_target_path)

		# ------------------------------------------------- cleanup ----------------------------------------------------
		rmtree(temporary_directory)

		# --------------------------------------------- show binary in finder ---------------------------------------------
		call(["open", "-R", binary_target_path])

	except Exception as error:	# TODO: specify Exception
		# ---------------------------------------- cleanup on error before exit ----------------------------------------
		if exists(temporary_directory):
			rmtree(temporary_directory)

		raise Exception(repr(error))


if __name__ == "__main__":
	main()
