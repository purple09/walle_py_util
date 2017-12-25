## 用途

自动签名未签名 apk，加固的请不要签名！然后调用[walle](https://github.com/Meituan-Dianping/walle)批量打渠道包。

## 使用方法
1.修改 defaultConfig.conf 配置文件；

2.channel 中添加渠道名，一行一个

3.把 apk 文件放到根目录，必须与配置文件中名字一致；

4.python apk.py

5.apks目录中即渠道包

## 可选命令

- -d 或 --dir \<dirName>,如 -d app1
- -c --channels \<channels>,如 -c baidu,tencent,wandoujia

## 子目录使用说明
- 子目录的 config.conf 覆盖 defaultConfig.conf,仅需配置要修改的字段
- 若子目录有 channel 文件，则不使用父目录的 channel 文件
- apk 文件也要放在子目录中，如命名不同记得修改 config.conf 文件
- 渠道包在子目录的 apks 目录中
- 可使用-d 命令实现多项目配置