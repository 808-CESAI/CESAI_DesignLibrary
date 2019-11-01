# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'access_key'
secret_key = 'secret_key'

url_head = 'url_head'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'cesai'



#上传后保存的文件名
key = 'img/user.png'

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = 'user.png'

ret, info = put_file(token, key, localfile)
print(info)
print(ret)
# assert ret['key'] == key
# # assert ret['hash'] == etag(localfile)
