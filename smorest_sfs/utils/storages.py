#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mimetypes
import os
from pathlib import Path
from typing import TypeVar, Union

from flask import send_file
from werkzeug.datastructures import FileStorage

from .paths import (
    ProjectPath,
    UploadPath,
    get_avator_path,
    get_relative_pathstr,
    make_uploaded_path,
)

Response = TypeVar("Response")


def load_storage_from_path(filename: str, path: Union[Path, str]) -> FileStorage:
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    file_pointer = open(ProjectPath.get_subpath_from_project(path), "rb")
    return FileStorage(file_pointer, filename, "file", content_type)


def load_avator_from_path(avator_path: str) -> FileStorage:
    path = get_avator_path(avator_path)
    return load_storage_from_path(avator_path, path)


def save_storage_to_path(store: FileStorage, subdir: str) -> str:
    path = make_uploaded_path(subdir)
    store.stream.seek(0)
    store.save(str(path))
    store.stream.seek(0)
    return get_relative_pathstr(path)


def delete_from_rel_path(path: Union[Path, str]) -> None:
    filepath = ProjectPath.get_subpath_from_project(path)
    if filepath.exists() and not UploadPath.if_in_whitelst(filepath):
        os.remove(filepath)


def make_response_from_store(store: FileStorage) -> Response:
    resp: Response = send_file(
        store.stream,
        attachment_filename=store.filename,
        mimetype=store.content_type,
        as_attachment=False,
    )
    return resp
