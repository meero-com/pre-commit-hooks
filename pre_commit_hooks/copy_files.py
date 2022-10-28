from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
from typing import Sequence

def file_content_hash(filename: str) -> str:
    """
    Returns
    -------
        md5.hexdigest() is returned string containing only hexadecimal digits.
        or 'file_not_found' if file does not exists
    """
    if not os.path.exists(filename):
        return 'file_not_found'

    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def copy_file(src_path, dst_path) -> None:
    dst_dir = re.sub(r"^(?P<tree>/?.+)?/(?P<file_name>.+)$", r"\g<tree>", dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    shutil.copy(src_path, dst_path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    parser.add_argument('--src_regex', dest='src_regex', default='')
    parser.add_argument('--dst_regex', dest='dst_regex', default='')
    args = parser.parse_args(argv)

    input_regex = rf"{args.src_regex}"
    output_regex = rf"{args.dst_regex}"

    retval = 0

    for filename in args.filenames:
        if not re.match(input_regex, filename):
            continue

        destination_path = re.sub(input_regex, output_regex, filename)

        previous_file_hash = file_content_hash(destination_path)

        copy_file(filename, destination_path)

        new_file_hash = file_content_hash(destination_path)

        if previous_file_hash != new_file_hash:
            retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
