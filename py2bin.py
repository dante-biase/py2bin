#!/usr/local/bin/python3

from os import getcwd, chdir, remove
from os.path import dirname, exists
from shutil import copy2, rmtree, copytree
from subprocess import call, check_output, STDOUT, CalledProcessError
from tempfile import mkdtemp

import click

from callbacks import *


@click.command()
@click.argument("py_file",
                callback=check_py_file)
@click.option("-r", "--resources_directory",
              default=None,
              callback=check_resources_directory,
              help="directory that contains resources for binary")
@click.option("-d", "--destination_directory",
              default=None,
              callback=check_destination_directory,
              help="directory to create the binary in")
@click.option("-o", "--optimize",
			  is_flag=True,
              help="compile with optimizations")
def main(py_file, resources_directory, destination_directory, optimize):

	owd = getcwd()  # save copy of original working directory to create absolute path in case of runtime error
	temporary_directory = mkdtemp()	# create temporary directory

	try:
		# -------------------------------------------- setup binary variables ---------------------------------------------
		py_file = Path(py_file)
		py_file_parent_directory = Path(dirname(py_file.absolute()))
		binary_name = f"{py_file.stem}"

		if not destination_directory:
			binary_target_path = f"{py_file_parent_directory.absolute()}/{binary_name}"
		else:
			binary_target_path = f"{destination_directory}/{binary_name}"

		# ------------------------------------------- check binary target path --------------------------------------------
		if exists(binary_target_path):
			overwrite = ""
			while not (overwrite == 'y' or overwrite == 'n'):
				overwrite = str(input(f"{binary_target_path} already exists. Replace? [y/n] "))

			if overwrite == 'y':
				remove(binary_target_path)
			else:
				exit(0)
				
		# --------------------------- copy parent directory of script to temporary directory ---------------------------
		copytree(py_file_parent_directory.absolute(), f"{temporary_directory}/{py_file_parent_directory.name}")
		
		# ----------------------------------------- go to temporary directory ------------------------------------------
		chdir(temporary_directory)
		py_file_copy = f"{py_file_parent_directory.name}/{py_file.name}"

		# -------------------------------------------- execute pyinstaller ---------------------------------------------
		
		if optimize:
			pyinstaller_call = ["python3", "-OO", "-m", "PyInstaller"]
		else:
			pyinstaller_call = ["pyinstaller"]
		pyinstaller_call.append(f"{py_file_parent_directory.name}/{py_file.name}")

		pyinstaller_arguments = ["--onefile", "--hidden-import", "pkg_resources.py2_warn"]
		if resources_directory:
			pyinstaller_arguments += ["--add-data", f"{resources_directory}:resources"]
		
		try:
			check_output(pyinstaller_call + pyinstaller_arguments, stderr=STDOUT)
		except CalledProcessError as error:
			print(error.output.decode("UTF8"))
			exit(1)

		# ------------------------------------- extract binary to target destination --------------------------------------
		copy2(f"dist/{binary_name}", binary_target_path)																

		# ------------------------------------------------- cleanup ----------------------------------------------------
		chdir(owd)
		rmtree(temporary_directory)

		# ------------------------------------------- show new binary in finder -------------------------------------------
		call(["open", "-R", binary_target_path])

	except Exception as error:	# TODO: specify Exception

		# ---------------------------------------- cleanup on error before exit ----------------------------------------
		if exists(temporary_directory):
			rmtree(temporary_directory)

		raise error


if __name__ == "__main__":
	main()
