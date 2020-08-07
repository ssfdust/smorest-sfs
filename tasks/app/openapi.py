"""OpenApi管理

用于上传openapi的json到yapi以及存储到本地
"""
import json
import os
from urllib import parse, request

from ._utils import app_context_task


@app_context_task
def dump_swagger(context):
    """dump到本地swagger文件"""
    from smorest_sfs.extensions import api

    with open("openapi.json", "w") as f:
        json.dump(api.spec.to_dict(), f, indent=4)
    os.system(
        "api-spec-converter --from=openapi_3 --to=swagger_2 openapi.json > swagger.json"
    )
    os.remove("openapi.json")


@app_context_task
def upload(context):
    """上传到yapi服务器"""

    dump_swagger(context)

    if os.path.exists(".uploadcfg"):
        with open(".uploadcfg", "r") as f:
            url, token = f.readlines()
    else:
        with open(".uploadcfg", "w") as f:
            url = input("请输入url: ")
            token = input("请输入token: ")
            f.writelines([url, "\n", token])

    with open("swagger.json") as f:
        upload_data = parse.urlencode(
            [
                ("type", "swagger"),
                ("json", f.read()),
                ("merge", "merge"),
                ("token", token),
            ]
        )
        req = request.Request(f"{url.strip()}/api/open/import_data")
        with request.urlopen(req, data=upload_data.encode("utf-8")) as f:
            res = json.loads(f.read().decode())
            print(res["errmsg"])

    os.remove("swagger.json")
