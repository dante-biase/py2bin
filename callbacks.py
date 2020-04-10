from os import mkdir
from shutil import rmtree
from pathlib import Path

from assertions import *


def check_py_file(ctx, param, file_path):
	assert_file_type(file_path, '.py')
	return Path(file_path).absolute()

def check_resources_directory(ctx, param, resources_path):
	if resources_path:
		assert_is_dir(resources_path)
		resources_path = Path(resources_path).absolute()

	return resources_path

def check_destination_directory(ctx, param, directory_path):
	if directory_path:
		assert_is_dir(directory_path)
		directory_path = Path(directory_path).absolute()

	return directory_path
