目录结构
==================

根目录
------------------

::

    .
    ├── config/ (配置文件目录)
    ├── deploy/ (发布相关配置目录)
    ├── docker-compose.yml
    ├── Dockerfile  
    ├── docs/
    ├── gunicorn.py  (gunicorn目录)
    ├── kube/   (k8s目录)
    ├── LICENSE
    ├── Makefile
    ├── migrations/  (迁移目录)
    ├── mypy.ini
    ├── poetry.lock
    ├── pyproject.toml
    ├── README.rst
    ├── requirements.txt
    ├── scripts/  (其他脚本目录)
    ├── smorest_sfs/  (核心目录)
    ├── tasks/  (invoke执行脚本目录)
    ├── tests/  (测试目录)
    └── uploads/  (上传文件目录)


核心需要关注的是smorest_sfs目录以及tests目录，下面是对

smorest_sfs
-------------------
