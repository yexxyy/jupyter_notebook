#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rsa_test.py in jupyter_notebook
# Created by yetongxue at 2019-08-01

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

# 生成私钥$ openssl genrsa -out rsa_private_key.pem 2048
# 生成公钥$ openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem

RSA_PRIVATE_KEY = """
MIIEowIBAAKCAQEAwe+eDd8JuuNo3DWOPrBGUxLfwboZq8O3yTVKEOWy4tkEhI2t
zmkx1tLfq+rsE7IhlHsLQaqQXHxEICbfvNmere9NC0ksm1Sb1fBjtsSVJoVp5Sk8
fcdbNc7Xzi63QcXTqnMX74iIgZPeZglJYt0gwbVAZ2oOC42XqSRBl4B1Nxu8M3Lg
XKnM3fFBU1nmjyNJgsEqywXEN/aPHlW2mBFMLa4WqufX7aYHgXC+/8pfuDf2EwQa
NUYwMKvun0+asXlF3CG6BbKQPjz1oQzWa4gsIR9et8N22jFfr/WBMl1xHg2APBgY
+h2OJGyzyN8XOa47VYG0dHQyugpkRwPQvgEqxQIDAQABAoIBAB9PpZANw49l6ecr
ymR6p1AASxoHBuABgGm+7c9elowjh6QzD620tDQ/5ZbnHehsKRnE5+NZO2eDNKiQ
Pi1KYWEpsqGw1b/aYDKhVigLAx2uCpPSHY8dIa/FTnheeH3pB6yMWn/05j0td4m3
1B5fH0vHDLflmpDo8mR/kwt31PTpf+toS1WA4OlUWqEhISWKwf8yiNXh5tv+UC3o
AhWpAtFcrxE5PnEJvLeDDYGRHZ275BiV34DJJE5OFgTBhpPIydXHnQaT8p4lg0Ev
wfoN7CgDOQ0/mM55T3XwrHJZlwamSjwkGunwO1zvUygEHD/ab+utVNykQ63QC7bZ
zLL83F0CgYEA/KzOgv/3rBVX7IEUEJctkSivvq4bItMcpouLKdJM57SvskMoxAFx
IRbRW6JV9zm+pfxQGHZTtKktuS7Ua5iCawwOWCeifHuwfzBkm7vB2ikaKGU77wT6
SYAfLitoiE9pK0/sQRyK4OtHzkIJ1XvRF5aFkuRSvyu/h4sFQ0EVktMCgYEAxHzv
WV/7KSAm2EgUqpJrK6OIh7VlOrEPIb0/aJwswVJFS5u7gVKRhZW331Jb0oRjo4wq
0qwJLLGCUF8YtH9Ygx5uI83tA9BJs2rA4RmBmm6vLPjTTkwOB88zrkmccicKUERN
i2kS5jJglO1csKxnMqWfhsS53idy9rKFncBu3QcCgYAxn6KjObAjnMF60lLleztY
wdvaIAl2Sm3bC5bWLNYrv2GuKeBstjfIntmZHIWzmySlJqt4UmzYE03Gi7ruMrKS
YXjDuW0A863THOb1aueEeAQKIO+nXpvlKYN2JtJNywLFndmxY/Cmga7FhFS4F6wV
7Nro4Wya3PWtohDzh2m8PwKBgByPZGMDVoiVyc+qOobInZdMP+4p6brsPZzT20Gj
YcX/5V6mFk0n6UsXhhCJ8hrZb3o4R4kzxGmgq6ZvDDJASGdWpv/BUPA6+FuB6uNN
R89gw0mwKVa6K1frQEHXJUxabF9abkMTVNHtBKjhD5YGmUF9XYDDW5j09vrw3Acg
D31FAoGBANP/rXch32VJjY1SPePUAQVHPkbaApkR6Ufa8Zzq1yrN1o33BWEW2JW9
Xhk6Ks75ah5MzH2QDm3F8cxLufGZORIlnO5A81w3e2KY9adGAwZNhjzT9KNJZVcC
t7Ccy7VRnmZwTMNgTOdzspu26drofO2ttqwyBjIIuz+eEDU/wAO0
"""

RSA_PUBLIC_KEY = """
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwe+eDd8JuuNo3DWOPrBG
UxLfwboZq8O3yTVKEOWy4tkEhI2tzmkx1tLfq+rsE7IhlHsLQaqQXHxEICbfvNme
re9NC0ksm1Sb1fBjtsSVJoVp5Sk8fcdbNc7Xzi63QcXTqnMX74iIgZPeZglJYt0g
wbVAZ2oOC42XqSRBl4B1Nxu8M3LgXKnM3fFBU1nmjyNJgsEqywXEN/aPHlW2mBFM
La4WqufX7aYHgXC+/8pfuDf2EwQaNUYwMKvun0+asXlF3CG6BbKQPjz1oQzWa4gs
IR9et8N22jFfr/WBMl1xHg2APBgY+h2OJGyzyN8XOa47VYG0dHQyugpkRwPQvgEq
xQIDAQAB
"""


class RsaTool(object):

    def sign_data(self, data):
        key = b64decode(RSA_PRIVATE_KEY)
        rsakey = RSA.importKey(key)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data.encode('utf8'))
        sign = signer.sign(digest)
        return b64encode(sign)

    def verify_sign(self, data, sign):
        key = b64decode(RSA_PUBLIC_KEY)
        rsakey = RSA.importKey(key)
        verifier = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data.encode())
        verified = verifier.verify(digest, b64decode(sign))
        assert verified, '签名验证失败'


if __name__ == '__main__':
    rsa_tool = RsaTool()
    data = '我是将被加签的字符串'
    sign = rsa_tool.sign_data(data)
    rsa_tool.verify_sign(data, sign)
