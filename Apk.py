#!/usr/bin/python
#-*-coding:utf-8-*-

import os
import sys
import ConfigParser
import getopt
import commands
import json
import jiagu

# 获取参数


def getParams(argv):
    global dir, channels, apkPath, jiagu360Channels
    try:
        opts, args = getopt.getopt(
            argv, "hd:c:f:j", ["help", "dir=", "channels=", "file=", "jiagu360"])
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
        elif opt in ("-f", "--file"):
            apkPath = arg
        elif opt in ("-j", "--jiagu360"):
            jiagu360Channels = '_360'
# 读取配置文件


def initCongig(configPath):
    global keystorePath, keyAlias, keystorePassword, keyPassword, apkName, AndroidBuildToolPath, _360user, _360pwd
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
    if cf.has_option(configSection, '_360user'):
        _360user = cf.get(configSection, '_360user')
    if cf.has_option(configSection, '_360pwd'):
        _360pwd = cf.get(configSection, '_360pwd')

# 校验v2签名


def checkV2(apk):
    output = commands.getoutput(
        "java -jar " + checkAndroidV2Signature + " " + apk)
    print output
    return json.loads(output)['isV2OK']


def package(apk, isJiagu360):
    if checkV2(apk):
        channelAPkPath = apk
    else:
        print '未签名'
        # zipalign
        zipalignCmd = zipalign + " -v 4 " + apk + " " + zipalignedApkPath
        commands.getoutput(zipalignCmd)
        # sign
        signCmd = apksigner + " sign --ks " + keystorePath \
            + " --ks-key-alias " + keyAlias \
            + " --ks-pass pass:" + keystorePassword \
            + " --key-pass pass:" + keyPassword \
            + " --out " + signedApkPath + " " + zipalignedApkPath
        commands.getoutput(signCmd)
        channelAPkPath = signedApkPath
     # walle
    walleCmd = "java -jar " + walle
    if isJiagu360:
        walleCmd += " batch -c " + jiagu360Channels + " "
    elif channels != '':
        walleCmd += " batch -c " + channels + " "
    else:
        walleCmd += " batch -f " + channelPath + " "
    walleCmd = walleCmd + channelAPkPath + " " + outputPath
    print commands.getoutput(walleCmd)
    # 删除中间文件
    if os.path.exists(zipalignedApkPath):
        os.remove(zipalignedApkPath)
    if os.path.exists(signedApkPath):
        os.remove(signedApkPath)


dir = ''
channels = ''
apkPath = ''
jiagu360Channels = ''
if __name__ == "__main__":
    getParams(sys.argv[1:])
# 根目录
rootPath = sys.path[0]
appPath = rootPath
if dir != '':
    appPath = os.path.join(rootPath, dir)
# 读取配置文件
configSection = 'info'
initCongig(os.path.join(rootPath, 'defaultConfig.conf'))
if dir != '':
    initCongig(os.path.join(dir, 'config.conf'))
# print keystorePath, keyAlias, keystorePassword, keyPassword, apkName, AndroidBuildToolPath
# 文件路径
libPath = os.path.join(rootPath, 'lib')
walle = os.path.join(libPath, 'walle-cli-all.jar')
checkAndroidV2Signature = os.path.join(libPath, 'CheckAndroidV2Signature.jar')
zipalign = os.path.join(AndroidBuildToolPath, 'zipalign')
apksigner = os.path.join(AndroidBuildToolPath, 'apksigner')
if apkPath == '':
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

package(apkPath, False)
if jiagu360Channels != '':
    jiagu.login(_360user, _360pwd)
    jiagu.jiagu(apkPath, outputPath)
    jiaguApkPath = jiagu.findJiaguApk(apkPath, outputPath)
    package(jiaguApkPath, True)
    if os.path.exists(jiaguApkPath):
        os.remove(jiaguApkPath)


print '打包结束'
