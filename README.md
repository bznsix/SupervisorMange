# SupervisorMange
用于管理启动项的工具
这是一个用于管理supervisorctl的配置文件工具

配置文件的目录均在/etc/supervisor/conf.d下

配置文件的模板为：
```
[program:diaoyu_bsc]
directory=/home/server/Approve_scan
command=/home/server/miniconda3/envs/collector/bin/python -u eth_approve.py
autostart=true
autorestart=true
startsecs=1
user=server
stderr_logfile=/tmp/diaoyu_bsc_err.log
stdout_logfile=/tmp/diaoyu_bsc_stdout.log
redirect_stderr=true
stdout_logfile_maxbytes=20000000
stdout_logfile_backups=3
```

我会给你提供program名称 directory目录 需要执行的程序名字 例如eth_approve.py 除非特殊指定均使用/home/server/miniconda3/envs/collector/bin/python -u来执行文件
你需要对应的修改log file的名字 以program id 为定
同时在每个配置文件的第一行添加注释，这个注释由我手动输入 用来描述这个配置文件的内容

生成完配置文件后 我希望你能执行对应的指令 让对应的配置文件进行加载

以上代码均使用python 生成，设计合适的cli 来让我完成上述操作