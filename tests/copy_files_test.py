from __future__ import annotations

import pytest
import os
import shutil

from pre_commit_hooks.copy_files import main
from testing.util import get_destination_path, get_resource_path

def setup_module(module):
    print('*****SETUP*****')
    destination_directory = get_destination_path('')

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # set existing file
    shutil.copy(get_resource_path('new_readme.md'), get_destination_path('up_to_date.md'))
    shutil.copy(get_resource_path('old_readme.md'), get_destination_path('updated.md'))


def teardown_module(module):
    print('******TEARDOWN******')
    shutil.rmtree(get_destination_path(''))

@pytest.mark.parametrize(
    ('filename', 'new_name', 'expected_retval'), (
        ('new_readme.md', 'created.md', 1),
        ('new_readme.md', 'updated.md', 1),
        ('new_readme.md', 'up_to_date.md', 0),
    ),
)
def test_main(capsys, filename, new_name, expected_retval):
    ret = main([get_resource_path(filename), f'--src_regex={get_resource_path(filename)}', f'--dst_regex={get_destination_path(new_name)}'])
    assert ret == expected_retval
