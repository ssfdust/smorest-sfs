#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List

import pytest
from freezegun import freeze_time

from smorest_sfs.utils.paths import (
    WHITE_LIST,
    ProjectPath,
    UploadPath,
    check_ext,
    get_avator_path,
    get_relative_pathstr,
    make_uploaded_path,
)


class TestProjectPath:
    @pytest.mark.parametrize("_dir", ["tests", "smorest_sfs"])
    def test_project_path(self, _dir: str) -> None:
        project_path = ProjectPath.get_project_path()
        dir_path = Path(project_path, _dir)
        assert dir_path.exists()


@freeze_time("1994-09-11 08:20:00")
class TestUploadPath:
    @pytest.mark.parametrize(
        "storetype, withdate, args",
        [("a", True, ["1994", "09", "11"]), ("b", False, [])],
    )
    def test_uploads_subdir(
        self, storetype: str, withdate: bool, args: List[str]
    ) -> None:
        project_path = ProjectPath.get_project_path()
        dir_path = Path(project_path, "uploads", storetype, *args)
        assert UploadPath.get_uploads_subdir(storetype, withdate) == dir_path


@freeze_time("1994-09-11 08:20:00")
@pytest.mark.usefixtures("patch_uuid")
@pytest.mark.usefixtures("clean_dirs")
@pytest.mark.parametrize("key", ["foo", "bar", "new"])
def test_make_uploaded_path(key: str) -> None:
    path = make_uploaded_path(key)
    pathstr = get_relative_pathstr(path)
    abs_path = ProjectPath.get_subpath_from_project(pathstr)

    assert pathstr == f"uploads/{key}/1994/09/11/123456789" and path == abs_path


def test_white_lst() -> None:
    for path in WHITE_LIST:
        assert os.path.exists(ProjectPath.get_subpath_from_project(path))


@pytest.mark.parametrize(
    "avator_path", ["default/AdminAvator.jpg", "default/DefaultAvator.jpg"]
)
def test_avator_path(avator_path: str) -> None:
    path = get_avator_path(avator_path)
    assert path.exists()


@pytest.mark.parametrize(
    "filename, ext", [("AdminAvator.jpg", "jpg"), ("DefaultAvator.jpg", ".jpg")]
)
def test_check_ext_success(filename: str, ext: str) -> None:
    assert check_ext(filename, ext)


@pytest.mark.parametrize(
    "filename, ext",
    [
        (".~AdminAvator.jpg", ".jpg"),
        (".~DefaultAvator.jpg", "jpg"),
        ("other.xlsx", "jpg"),
        ("other.xlsx", ".jpg"),
    ],
)
def test_check_ext_fail(filename: str, ext: str) -> None:
    assert not check_ext(filename, ext)
