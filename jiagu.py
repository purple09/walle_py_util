#!/usr/bin/python
#-*-coding:utf-8-*-

import commands
import os
import sys

# 赋予权限
# chmod 777 /Users/guizhen/work/python/walle_py_util/lib/jiagu/java/bin/java
# 执行/Users/guizhen/work/python/walle_py_util/lib/jiagu/java/bin/java -jar /Users/guizhen/work/python/walle_py_util/lib/jiagu/jiagu.jar
# 打开界面，手动勾选需要的服务，比如 x86 支持，命令行有 bug


def login(user, pwd):
    loginCmd = '%s -jar %s -login %s %s' % (
        jiaguJavaPath, jiaguJarPath, user, pwd)
    # 废话太多，只打最后的结果
    print commands.getoutput(loginCmd).split('\n')[-1]


def jiagu(apkPath, outPath):
    jiaguCmd = '%s -jar %s  -jiagu %s %s' % (
        jiaguJavaPath, jiaguJarPath, apkPath, outPath)
    # 废话太多，只打最后的结果
    print commands.getoutput(jiaguCmd)


def findJiaguApk(apkPath, outPath):
    jiaguApkPath = ''
    apkName = os.path.basename(apkPath)[:-4]
    for child in os.listdir(outPath):
        childPath = os.path.join(outPath, child)
        if(os.path.isfile(childPath) and child.startswith(apkName) and child.endswith('jiagu.apk')):
            jiaguApkPath = childPath
            break
    return jiaguApkPath


def showconfig():
    print commands.getoutput('%s -jar %s -showconfig' % (jiaguJavaPath, jiaguJarPath))


jiaguRootPath = sys.path[0]
jiaguJavaPath = 'java'
# jiaguJavaPath = jiaguRootPath + '/lib/jiagu/java/bin/java'
jiaguJarPath = jiaguRootPath + '/lib/jiagu/jiagu.jar'
