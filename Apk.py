#!/usr/bin/python
#-*-coding:utf-8-*-

import os
import sys
import ConfigParser
import getopt
import commands
import json

# 获取参数


def getParams(argv):
    global dir, channels
    try:
        opts, args = getopt.getopt(argv, "hd:c:", ["help","dir=", "channels="])
    except getopt.GetoptError:
        print 'APK.py -d <appdir> -c <channels>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'APK.py -d <appdir> -c <channels>'
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir = arg
        elif opt in ("-c", "--channels"):
            channels = arg
# 读取配置文件


def initCongig(configPath):
    global keystorePath, keyAlias, keystorePassword, keyPassword, apkName, AndroidBuildToolPath
    cf = ConfigParser.ConfigParser()
    cf.read(configPath)
    if cf.has_option(configSection, 'keystorePath'):
        keystorePath = cf.get(configSection, 'keystorePath')
    if cf.has_option(configSection, 'keyAlias'):
        keyAlias = cf.get(configSection, 'keyAlias')
    if cf.has_option(configSection, 'keystorePassword'):
        keystorePassword = cf.get(configSection, 'keystorePassword')
    if cf.has_option(configSection, 'keyPassword'):
        keyPassword = cf.get(configSection, 'keyPassword')
    if cf.has_option(configSection, 'apkName'):
        apkName = cf.get(configSection, 'apkName')
    if cf.has_option(configSection, 'AndroidBuildToolPath'):
        AndroidBuildToolPath = cf.get(configSection, 'AndroidBuildToolPath')
# 校验v2签名


def checkV2(apkPath):
    output = commands.getoutput(
        "java -jar " + checkAndroidV2Signature + " " + apkPath)
    print output
    return json.loads(output)['isV2OK']


dir = ''
channels = ''
if __name__ == "__main__":
    getParams(sys.argv[1:])
# 根目录
rootPath = os.getcwd()
appPath = rootPath
if dir != '':
    appPath = os.path.join(rootPath, dir)
# 读取配置文件
configSection = 'info'
initCongig('defaultConfig.conf')
if dir != '':
    initCongig(os.path.join(dir, 'config.conf'))
# print keystorePath, keyAlias, keystorePassword, keyPassword, apkName, AndroidBuildToolPath
# 文件路径
libPath = os.path.join(rootPath, 'lib')
walle = os.path.join(libPath, 'walle-cli-all.jar')
checkAndroidV2Signature = os.path.join(libPath, 'CheckAndroidV2Signature.jar')
zipalign = os.path.join(AndroidBuildToolPath, 'zipalign')
apksigner = os.path.join(AndroidBuildToolPath, 'apksigner')
apkPath = os.path.join(appPath, apkName)
channelPath = os.path.join(appPath, 'channel')
if not os.path.exists(channelPath):
    channelPath = os.path.join(rootPath, 'channel')
zipalignedApkPath = apkPath[:-4] + "_aligned.apk"
signedApkPath = zipalignedApkPath[:-4] + "_signed.apk"
outputPath = os.path.join(appPath, 'apks')
try:
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
except Exception:
    pass

if checkV2(apkPath):
    channelAPkPath = apkPath
else:
    # zipalign
    zipalignCmd = zipalign + " -v 4 " + apkPath + " " + zipalignedApkPath
    print commands.getoutput(zipalignCmd)
    # sign
    signCmd = apksigner + " sign --ks " + keystorePath \
        + " --ks-key-alias " + keyAlias \
        + " --ks-pass pass:" + keystorePassword \
        + " --key-pass pass:" + keyPassword \
        + " --out " + signedApkPath + " " + zipalignedApkPath
    print commands.getoutput(signCmd)
    channelAPkPath = signedApkPath
# walle
walleCmd = "java -jar " + walle
if channels != '':
    walleCmd += " batch -c " + channels + " "
else:
    walleCmd += " batch -f " + channelPath + " "
walleCmd = walleCmd + channelAPkPath + " " + outputPath
print commands.getoutput(walleCmd)
