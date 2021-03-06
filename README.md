# Arctime 自动登录+签到获取积分 定时任务

#### 项目介绍

做字幕神器[**Arctime**](http://m.arctime.cn/home/user/login.html)（懂的都懂），一般来讲是免费使用的，如需购买如面向非编软件的软字幕输出、专业视频格式压制输出、**全自动语音转写**等增值性功能，则需使用积分来购买，积分需要进行RMB充值方可获取，换算标准为1元=100积分。咱做视频教程的，最常用到的就是全自动语音转写功能啦，为了更好的（bai）给大家出课程（piao），我发现登录个人中心之后，每天可以进行签到！签到即可每日获取20积分，相当于0.2元RMB呀。而大致换算的话，10分钟的视频撰写费用是300积分，也就是说，我只要连续签到15天即可免字幕制作费给大家做一课10分钟的视频啦！~**严正声明，本项目仅供研究学习使用，切勿用于非法用途或者破坏官方规则谋取利益等**

于是我研究了一个python小脚本用来自动登录和签到。

最开始的时候我是放在我写的定时任务框架`xjobs`：

Gitee码云：[https://gitee.com/xueshanlinghu/xjobs](https://gitee.com/xueshanlinghu/xjobs)

Github：[https://github.com/xueshanlinghu/xjobs](https://github.com/xueshanlinghu/xjobs)

中来运行，xjobs托管在服务器中。

最近研究的时候发现Github有Github Actions功能，它可以提供一系列的链式方式执行线上自动化持续部署（CI/CD），还能支持定时任务，于是我就研究了一下各类文档，将本项目改造成一个依托于Github Actions功能的自动化每日定时任务项目，这样连服务器都省啦，而且也有日志方便查询。

那么如果你也想拥有这样的自动化功能，要怎么复用呢？



#### 手动调用（仅供测试脚本是否还能用使用，定时任务不推荐）

使用python3.8.2开发，建议python3.6+环境。

1. 安装依赖：

```powershell
pip install -r requirements.txt
```

2. 调用脚本：

主脚本为：`arctime_auto_sign.py`

传入的第一个参数为用户名，第二个参数为密码，运行即可自动登录并签到。

如：

```powershell
python arctime_auto_sign.py 13000000000 pass123456
```



#### Github Actions定时任务（目前极度推荐！！！）

本地无需安装环境！！！

请提前准备好Arctime的**用户名**和**密码**。

享用方式：

1. Fork本项目到你自己的仓库库。

2. 点击Settings → Secrets，创建五个Secrets。（别担心，放进去并保存后连你自己都无法再看到明文，只允许更新或删除，不会公开的）必须要设置哦，否则脚本会运行失败！如图所示：

   ![image-20201023161159757](assets/image-20201023161159757.png)

   它们分别为：

   * USERNAME                           arctime用户名
   * PASSWORD                           arctime密码
   * MAIL_USERNAME                 qq邮箱号
   * MAIL_PASSWORD                 qq邮箱授权码（不懂怎么获取的可以问我）
   * MAIL_TO                                 收件邮箱

3. 点击Actions，当项目Fork之后，为了避免风险，项目都会自动关闭Actions的开启，所以我们需要手动开始，点击按钮`I understand my workflows, go ahead and enable them`即可启用定义好的执行代码。到点了会自动进行执行。如图所示：

   ![image-20201021135430385](assets/image-20201021135430385.png)

4. 自定义任务：定时任务配置已经写好了，存放在`.github/workflow/auto_sign.yaml`文件中。目前默认会自动运行脚本的触发条件有两个，第一是当push项目的时候，第二是定时每天早上约8点30分（北京时间）的时候（线上因为定时任务排队可能会有半小时左右的延期）。如需个性定制化Github Actions或修改定时任务时间，请打开该文件，修改定时任务的时间，可以修改`cron`的值，该值目前定义的时间为每天的0点30分（UTC时间），目前发现该表达式仅支持UTC时间（格林威治时间），北京时间为东八区，如果以北京时间为准就是该时间加上8个小时。设定的时候需要注意一下。其他的内容如果你知道如何设定，可以按照你自己的需要进行设定。如果不知道就不要动了。【温馨提示：实测如果你是免费版Github Actions，定时执行的时间可能会不准，我遇到过比定时迟了二十到三十分钟执行的情况】

   如果你不知道如何设定自己需要的cron时间表达式，可以到这个网站看看：[https://crontab.guru/](https://crontab.guru/)

当自动执行完毕后，可以到Actions下查看运行的日志。成功打勾，失败打叉。然后你也可以到arctime官网上验证一下是否签到成功了。

尽情享用吧！



#### 关于项目贡献

本项目完全开源，大家可以各取所需。

如果你有自己的**想法**、**建议**、**bug问题**等，欢迎在码云Gitee或者Github提`Issue`。

如有其它代码贡献，欢迎提`Pull requests`。

看了一下码云应该还未有该功能，希望在不久后的未来能看到码云也有这样的功能。~



#### 更新日志
v1.2 20201028:

1. 进行定时任务时间调试等，修改对应的README文件。



v1.1 20201023：

1. 添加发送日志邮件的功能



v1.0 20201021：

1. 完成项目整体布局开发，自动部署改造，编写完成详细的说明文档。摸摸哒~



