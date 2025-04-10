#!/usr/bin/env python3
import os
import click
from rich.console import Console
from rich.prompt import Prompt
import subprocess

console = Console()
SUPERVISOR_CONF_DIR = "/etc/supervisor/conf.d"

def generate_config(program_name, directory, script_name, comment, python_path="/home/server/miniconda3/envs/collector/bin/python -u"):
    """生成Supervisor配置文件"""
    config = f"""# {comment}
[program:{program_name}]
directory={directory}
command={python_path} {script_name}
autostart=true
autorestart=true
startsecs=1
user=server
stderr_logfile=/tmp/{program_name}_err.log
stdout_logfile=/tmp/{program_name}_stdout.log
redirect_stderr=true
stdout_logfile_maxbytes=20000000
stdout_logfile_backups=3
"""
    return config

def write_config(program_name, config):
    """写入配置文件"""
    config_path = os.path.join(SUPERVISOR_CONF_DIR, f"{program_name}.conf")
    try:
        # 使用sudo写入配置文件
        subprocess.run(['sudo', 'tee', config_path], input=config.encode(), check=True)
        console.print(f"[green]配置文件已成功写入: {config_path}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]写入配置文件时出错: {str(e)}[/red]")
        return False

def reload_supervisor():
    """重新加载Supervisor配置"""
    try:
        subprocess.run(['sudo', 'supervisorctl', 'reread'], check=True)
        subprocess.run(['sudo', 'supervisorctl', 'update'], check=True)
        console.print("[green]Supervisor配置已重新加载[/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]重新加载Supervisor配置时出错: {str(e)}[/red]")
        return False

@click.group()
def cli():
    """Supervisor配置文件管理工具"""
    pass

@cli.command()
@click.option('--program-name', prompt='请输入程序名称', help='Supervisor程序名称')
@click.option('--directory', prompt='请输入工作目录', help='程序工作目录')
@click.option('--script-name', prompt='请输入脚本名称', help='要执行的Python脚本名称')
@click.option('--comment', prompt='请输入配置文件注释', help='配置文件的注释说明')
def create(program_name, directory, script_name, comment):
    """创建新的Supervisor配置文件"""
    config = generate_config(program_name, directory, script_name, comment)
    if write_config(program_name, config):
        if click.confirm('是否立即重新加载Supervisor配置？'):
            reload_supervisor()

@cli.command()
@click.argument('program_name')
def remove(program_name):
    """删除Supervisor配置文件"""
    config_path = os.path.join(SUPERVISOR_CONF_DIR, f"{program_name}.conf")
    try:
        os.remove(config_path)
        console.print(f"[green]配置文件已删除: {config_path}[/green]")
        if click.confirm('是否立即重新加载Supervisor配置？'):
            reload_supervisor()
    except Exception as e:
        console.print(f"[red]删除配置文件时出错: {str(e)}[/red]")

@cli.command()
def reload():
    """重新加载所有Supervisor配置"""
    reload_supervisor()

if __name__ == '__main__':
    cli() 