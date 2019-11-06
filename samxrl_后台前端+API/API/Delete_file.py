# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth
from qiniu import BucketManager


def delete(fileName):
    access_key = 'access_key'
    secret_key = 'secret_key'
    #初始化Auth状态
    q = Auth(access_key, secret_key)
    #初始化BucketManager
    bucket = BucketManager(q)
    #你要测试的空间， 并且这个key在你空间中存在
    bucket_name = 'cesai'
    key = fileName
    #删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
    return info
