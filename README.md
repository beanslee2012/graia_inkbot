# graia_inkbot
基于graia Ariadne 框架的斯普拉顿3（splatoon3） qq机器人（建设中，基本可用）



基于框架:
https://github.com/mamoe/mirai/releases/

https://github.com/GraiaProject/Ariadne

mirai 加载器:

https://github.com/iTXTech/mirai-console-loader/releases

插件:

https://github.com/KasukuSakura/mirai-login-solver-sakura/releases

https://github.com/cssxsh/fix-protocol-version/releases

windows版本主要流程：
===================================
解压
mirai和mcl

mcl.cmd --update-package net.mamoe:mirai-api-http --channel stable-v2 --type plugin

mcl.cmd -u
启动成功后出现 >提示符
/autoLogin add qq号 qq密码
启动过程中如果弹出验证码验证的窗口，将url复制到浏览器，打开开发者模式的网络。然后刷新页面，完成2次验证码拖动。在监控信息中找到cap_union_new_verify的响应信息
复制tickets 对应的值，然后粘贴到验证窗口的tickets文本框确认即可。
如果过程中提示短信或扫码验证等，按提示完成操作即可。

修改mirai 端口
config/net.mamoe.mirai-api-http/setting.yml中的端口（2处）

================

pip3 install  poetry


git下载代码
进入目录
poetry init  
poetry env use python3.8 # 版本号已本地实际为准
poetry add graia-ariadne
poetry add graia-saya
poetry add pillow
poetry add requests

把go_cqhttp的inkbot中的resource/目录下的文件夹及内容 复制到本项目的resource目录
修改main.py的配置和config/bot.conf中的路径(qq号、秘钥等信息，代码没有写)
poetry run python main.py

================

qq群中
、图
、工

