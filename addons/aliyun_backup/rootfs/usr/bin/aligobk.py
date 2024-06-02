# pip install git+https://github.com/5high/aligo.git
import sys
import threading
import schedule
import time
import os
import logging
from unittest import result
import requests
import base64
import json
from aligo import set_config_folder, Aligo
from aligo.error import AligoFatalError
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import pytz
from datetime import datetime
from dateutil import parser
from operator import itemgetter

# 签到开始
from dataclasses import dataclass, field
from typing import List, Dict

from datclass import DatClass

from aligo import Aligo
from aligo.core import Config

global sign_in_count
s_sign_in_rewards = []  # 初始化一个空列表用于存储签到奖励的通知

@dataclass
class Reward(DatClass):
    action: str = None
    background: str = None
    bottleId: str = None
    bottleName: str = None
    bottleShareId: str = None
    color: str = None
    description: str = None
    detailAction: str = None
    goodsId: int = None
    name: str = None
    notice: str = None
    subNotice: str = None


@dataclass
class Signinlogs(DatClass):
    calendarChinese: str = None
    calendarDay: str = None
    calendarMonth: str = None
    day: int = None
    icon: str = None
    isReward: bool = None
    notice: str = None
    pcAndWebIcon: str = None
    poster: str = None
    reward: Reward = None
    rewardAmount: int = None
    status: str = None
    themes: str = None
    type: str = None


@dataclass
class Result(DatClass):
    blessing: str = None
    description: str = None
    isReward: bool = None
    pcAndWebRewardCover: str = None
    rewardCover: str = None
    signInCount: int = None
    signInCover: str = None
    signInLogs: List[Signinlogs] = field(default_factory=list)
    signInRemindCover: str = None
    subject: str = None
    title: str = None


@dataclass
class SignInList(DatClass):
    arguments: str = None
    code: str = None
    maxResults: str = None
    message: str = None
    nextToken: str = None
    result: Result = None
    success: bool = None
    totalCount: str = None


@dataclass
class SignInReward(DatClass):
    arguments: str = None
    code: str = None
    maxResults: str = None
    message: str = None
    nextToken: str = None
    result: Reward = None
    success: bool = None
    totalCount: str = None


class CAligo(Aligo):
    V1_ACTIVITY_SIGN_IN_LIST = '/v1/activity/sign_in_list'
    V1_ACTIVITY_SIGN_IN_REWARD = '/v1/activity/sign_in_reward'

    def _sign_in(self, body: Dict = None):
        return self.post(
            CAligo.V1_ACTIVITY_SIGN_IN_LIST,
            host=Config.MEMBER_HOST,
            body=body, params={'_rx-s': 'mobile'}
        )

    def sign_in_list(self) -> SignInList:
        resp = self._sign_in({'isReward': True})
        return SignInList.from_str(resp.text)

    def sign_in_festival(self):
        return self._sign_in()

    def sign_in_reward(self, day) -> SignInReward:
        resp = self.post(
            CAligo.V1_ACTIVITY_SIGN_IN_REWARD,
            host=Config.MEMBER_HOST,
            body={'signInDay': day},
            params={'_rx-s': 'mobile'}
        )
        return SignInReward.from_str(resp.text)

def signdaily():
    ali = CAligo(level=logging.ERROR)
    # noinspection PyProtectedMember
    log = ali._auth.log
    # 获取签到列表
    sign_in_list = ali.sign_in_list()
    log.info('本月签到次数: %d', sign_in_list.result.signInCount)
    sign_in_count = sign_in_list.result.signInCount
    os.environ['SIGN_IN_COUNT'] = str(sign_in_count)

    # 签到
    for i in sign_in_list.result.signInLogs:
        if i.isReward:
            continue
        if i.status == 'normal':
            sign_in_reward = ali.sign_in_reward(i.day)
            notice = sign_in_reward.result.notice
            log.info('签到成功: %s', notice)

# 签到结束

global supervisor_token

from http.server import SimpleHTTPRequestHandler, HTTPServer

sys.stdout.flush()

config= '/data/'
set_config_folder(config)

# 创建一个格式化程序
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将格式化程序添加到一个日志记录器
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.formatter = formatter

# 记录一条消息
logger.info("Staring Aliyun Drive Backup Service ...")

# 获取环境变量
supervisor_token = os.environ.get("SUPERVISOR_TOKEN")
# 读取 JSON 文件
with open(config+'options.json', 'r') as file:
    options_data = json.load(file)

# 将 options_data 中的每个键都变成全局变量
for key, value in options_data.items():
    globals()[key] = value

# 用于生成HTML的函数
def generate_html_listcloud():
    global user, space
    sign_in_count = os.environ.get('SIGN_IN_COUNT')
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>阿里云盘备份列表</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: white;
            }
            h1 {
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                width: 300px;
                background-color: #f2f2f2;
            }
            .info {
                margin-top: 10px;
                text-align: left;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <h1>阿里云盘备份</h1>
    """
    html_content += f"""
        <h2>{user} 您的剩余空间还有: {space}</h2>
    """
    html_content += f"""
        <style>
            a {{
                text-decoration: none;
                color: #808080;  /* 设置超链接的颜色，可以根据需要修改 */
            }}
        </style>
        <marquee behavior="alternate" direction="left" scrollamount="5">
            <a href="https://sumju.net/?p=7943" target="_blank">【官方硬件优惠卷，最高可省60元～】</a>
            <a href="https://sumju.net/?p=8022" target="_blank">【大陆地区优化版本HassOS】</a>
            <a href="http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=NDQnzpDKRzaB7EMzQdPuU1yQPTN248-P&authKey=cjGRmNWaFSrUh%2B6yTOD0OtmmmzaJz93%2BRAC%2BQK6yBROTbYZ6PsLSJUOgIlt%2B41BK&noverify=0&group_code=248505081" target="_blank">【加QQ交流群】</a>
            <a href="https://sumju.net/" target="_blank">【插件作者博客】</a>
            <a href="https://space.bilibili.com/441936678" target="_blank">【B站频道首页】</a>
        </marquee>
    """
    html_content += """
        <table>
            <thead>
                <tr>
                    <th>备份时间</th>
                    <th>备份名称</th>
                    <th>本地</th>
                    <th>云上</th>
                </tr>
            </thead>
            <tbody>
    """
    for file_detail in backup_list():
        html_content += f"                <tr>\n                    <td>{file_detail['date']}</td>\n                    <td>{file_detail['name']}</td>\n                <td>{file_detail['local']}</td>\n     <td>{file_detail['cloud']}</td>\n</tr>\n"

    html_content += """
            </tbody>
        </table>
        <div class="info">

            """
    if sign_in_count is not None:
        html_content += f"<h3>您本月已经签到 {sign_in_count} 次</h3>"
    html_content += """
            <p>每日备份时间：{backup_time}</p>
            <p>本地保留数量：{keep_days_local}</p>
            <p>云盘保存数量：{keep_days_cloud}</p>
            <p>如需修改备份设置，请在插件的配置页面进行修改。</p>
        </div>
    </body>
    </html>
    """.format(
        backup_time=backup_time,
        keep_days_local=keep_days_local,
        keep_days_cloud=keep_days_cloud
    )

    return html_content

# 自定义请求处理程序，继承自SimpleHTTPRequestHandler
class BackupFilesHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if "404" in format or "500" in format:
            super().log_message(format, *args)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        refresh_tag = '<meta http-equiv="refresh" content="60">'
        # 生成HTML内容
        html_content = generate_html_listcloud()
        content = f"{refresh_tag}{html_content}"
        # 将HTML内容写入响应
        self.wfile.write(content.encode())

    def do_POST(self):
        if self.path == 'restore':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = parse_qs(post_data)

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            file_id = post_params.get('file_id', [''])[0]
            message = f"Received POST data. File ID: {file_id}"
            self.wfile.write(bytes(message, "utf8"))
        elif self.path == 'backup':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            message = f"Received POST data. "
            self.wfile.write(bytes(message, "utf8"))

class BackupFullHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if "404" in format or "500" in format:
            super().log_message(format, *args)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.end_headers()

        # 一行居中的文本
        centered_text = "<h1 style='text-align: center; margin-top: 1em;'>云盘已满无法继续备份</h1>"

        refresh_tag = '<meta http-equiv="refresh" content="5">'
        content = f"{refresh_tag}{centered_text}"
        self.wfile.write(content.encode())

class MyRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if "404" in format or "500" in format:
            super().log_message(format, *args)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.end_headers()
        refresh_tag = '<meta http-equiv="refresh" content="8">'
        title = "<h1 style='text-align: center; margin-top: 1em;'>阿里云盘扫码登录</h1>"
        image_tag = f'<div style="text-align: center;"><img src="data:image/png;base64,{read_image_to_base64()}" alt="Aliyun Drive QR Code" style="display: inline-block;"></div>'
        content = f"{refresh_tag}{title}<br>{image_tag}"
        self.wfile.write(content.encode())

def read_image_to_base64():
    image_url = 'http://127.0.0.1:8080/login.png'
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    try:
        response = requests.get(image_url, headers=headers)
        if response.status_code == 200:
            base64_image = base64.b64encode(response.content).decode('utf-8')
            return base64_image
        else:
            #print(f"Failed to fetch image. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        #print(f"An error occurred: {e}")
        return None

global user
global phone
global space
global folderid
global drive_id

lock = threading.Lock()

def get_user_info():
    global user
    global phone
    global drive_id
    try:
        ali = Aligo(level=logging.ERROR,port=8080)
        user_info = ali.get_user()
        drive_id = ali.default_drive_id
        with lock:
            user = user_info.nick_name
            phone = user_info.phone
    except AligoFatalError as e:
        if "EXPIRED" in str(e):
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Login time out , qrcode expired ... ")
        else:
            # print(f"AligoFatalError: {e}")
            pass

def convert_bytes(byte_size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while byte_size > 1024 and unit_index < len(units) - 1:
        byte_size /= 1024.0
        unit_index += 1
    return f"{byte_size:.2f} {units[unit_index]}"


def get_remaining_space():
    ali = Aligo(level=logging.ERROR)
    personal_info = ali.get_personal_info()
    used_size = personal_info.personal_space_info.used_size
    total_size = personal_info.personal_space_info.total_size
    remaining_space = max(total_size - used_size, 0)
    return convert_bytes(remaining_space)

def get_free_space():
    ali = Aligo(level=logging.ERROR)
    personal_info = ali.get_personal_info()
    used_size = personal_info.personal_space_info.used_size
    total_size = personal_info.personal_space_info.total_size
    remaining_space = max(total_size - used_size, 0)
    return remaining_space

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def check_internet():
    url_to_check = "https://www.baidu.com"
    try:
        response = requests.get(url_to_check, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False

def check_space_periodically():
    global space
    while True:
        space = get_remaining_space()
        if space is not None:
            pass
        else:
            restart_program()
        time.sleep(30)

class BaseFile:
    def __init__(self, type, file_id, name, parent_file_id):
        self.type = type
        self.file_id = file_id
        self.name = name
        self.parent_file_id = parent_file_id

class CreateFileResponse:
    def __init__(self, file_name, type, file_id, parent_file_id):
        self.file_name = file_name
        self.type = type
        self.file_id = file_id
        self.parent_file_id = parent_file_id

def folder_exsist():
    global folderid
    exsist = False
    ali = Aligo(level=logging.ERROR)
    ll = ali.get_file_list()
    folders = [item for item in ll if item.type == 'folder']
    for folder in folders:
        #print(f"文件夹名称: {folder.name}, 文件夹ID: {folder.file_id}, 父文件夹ID: {folder.parent_file_id}")
        if folder.name == folder_name:
            folderid  = folder.file_id
            exsist = True
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Backup folder exsist ... ")
    if not exsist:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Creating backup folder ... ")
        try:
            result = ali.create_folder(name=folder_name)
            folderid  = result.file_id
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Creating backup folder success ... ")
        except Exception as e:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Creating backup folder failed ... ")
            pass

# 云盘文件列表处理
from typing import List

def ls_cloud(folderid: str) -> List[dict]:
    ali = Aligo(level=logging.ERROR)
    file_list = ali.get_file_list(folderid)

    details_list = []
    for file_info in file_list:
        details_list.append({
            "file_id": file_info.file_id,
            "name": file_info.name,
            "date": file_info.created_at
        })

    return details_list

def ls_local():
    global supervisor_token
    url = "http://supervisor/backups"
    headers = {
        "Authorization": f"Bearer {supervisor_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            backups = data.get("data", {}).get("backups", [])

            result = []
            for backup in backups:
                backup_info = {
                    "name": backup.get("name", ""),
                    "slug": backup.get("slug", ""),
                    "date": backup.get("date", "")
                }
                result.append(backup_info)

            return result
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []

# 差集
def get_specific_difference(A, B, key_a, key_b):
    set_a = {row[key_a] + ".tar" if ".tar" not in row[key_a] else row[key_a]: row for row in A}
    set_b = {row[key_b] + ".tar" if ".tar" not in row[key_b] else row[key_b]: row for row in B}
    unique_keys_A = set_a.keys() - set_b.keys()
    difference = [set_a[key] for key in unique_keys_A]
    return difference

# 交集
def get_intersection(A, B, key_a, key_b):
    # 从集合 A 和集合 B 中获取键值对应的集合。
    set_a = {row[key_a] + ".tar" if ".tar" not in row[key_a] else row[key_a]: row for row in A}
    set_b = {row[key_b] + ".tar" if ".tar" not in row[key_b] else row[key_b]: row for row in B}

    # 获取集合 A 和集合 B 的键的交集。
    intersection_keys = set(set_a) & set(set_b)

    # 创建一个新的集合，用来存储交集。
    intersection = [set_a[key] for key in intersection_keys]

    return intersection


def simulate_upload(slug_value,folderid):
    ali = Aligo(level=logging.ERROR)
    ali.upload_file(f'/backup/{slug_value}.tar',folderid)

def simulate_backup():
    # signdaily()
    url = "http://supervisor/backups/new/full"
    headers = {
        "Authorization": f"Bearer {supervisor_token}",
        "Content-Type": "application/json"
    }
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
    data = {
        "name": f"Full-Backup-{current_datetime}",
        "compressed": True
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Starting backup and upload process ... ")
        json_response = response.json()
        slug_value = json_response.get("data", {}).get("slug")
        if slug_value:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Full backup complet staring upload process ... ")
            simulate_upload(slug_value,folderid)
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Upload process finshed ... ")
            delete_expired()
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Clean expired backups finshed ... ")
            restart_program()
        else:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Slug value not found in JSON response ... ")
    else:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+f" Backup request failed. Status code: {response.status_code} ... ")

def running_schedule():
    while True:
        global supervisor_token
        if supervisor_token != os.environ.get("SUPERVISOR_TOKEN"):
            supervisor_token = os.environ.get("SUPERVISOR_TOKEN")
        schedule.run_pending()
        time.sleep(1)

def supervisor_timezone(utc_time):
    global supervisor_token
    api_url = "http://supervisor/info"
    token = supervisor_token
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", {})
        timezone_name = data.get("timezone", "UTC")

        # 解析 UTC 时间字符串
        utc_datetime = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%f%z")

        # 获取 UTC 时间对应的时区
        tz_utc = pytz.utc

        # 将 UTC 时间转换为服务器所在时区的时间
        local_datetime = utc_datetime.replace(tzinfo=tz_utc).astimezone(pytz.timezone(timezone_name))

        return local_datetime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        print(f"Failed to get timezone. Status code: {response.status_code}")
        return None

def sort_backup_by_date(all_backup):
    # 自定义比较函数，按照日期时间进行排序
    def compare_dates(item):
        return parser.parse(item["date"])
    # 对 all_backup 进行倒序排序
    sorted_backup_reverse = sorted(all_backup, key=compare_dates, reverse=True)
    return sorted_backup_reverse

def backup_list():
    cloud_backups_info = ls_cloud(folderid)
    local_backups_info = ls_local()

    result_backup = []  # 创建局部变量

    intersection = get_intersection(local_backups_info, cloud_backups_info, "slug", "name")
    for item in intersection:
        backup_info = {
            "name": item["name"],
            "slug": item["slug"],
            "date": supervisor_timezone(item["date"]),
            "local": "✔️",
            "cloud": "✔️"
        }
        result_backup.append(backup_info)

    difference_local = get_specific_difference(local_backups_info, cloud_backups_info, "slug", "name")
    for item in difference_local:
        backup_info = {
            "name": item["name"],
            "slug": item["slug"],
            "date": supervisor_timezone(item["date"]),
            "local": "✔️",
            "cloud": "✘"
        }
        result_backup.append(backup_info)

    difference_cloud = get_specific_difference(cloud_backups_info, local_backups_info, "name", "slug")
    for item in difference_cloud:
        backup_info = {
            "name": item["name"],
            "slug": None,
            "date": supervisor_timezone(item["date"]),
            "local": "✘",
            "cloud": "✔️"
        }
        result_backup.append(backup_info)

    result_backup = sort_backup_by_date(result_backup)  # 使用局部变量

    return result_backup  # 返回局部变量

def handle_low_space():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Checking available space...")
    counter = 0
    while space is None and counter < 3:
        time.sleep(1)
        counter += 1
        if space is not None:
            break
    # 如果剩余空间足够，则执行正常操作
    if get_free_space() > 0:
        folder_exsist()
    else:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " No enough space to store backup files...")

        # 启动一个简单的HTTP服务器以显示磁盘空间满的消息
        httpdfull = HTTPServer(('0.0.0.0', 8099), BackupFullHandler)
        httpfull_thread = threading.Thread(target=httpdfull.serve_forever, name="DiskFull", daemon=True)
        httpfull_thread.start()

        # 检查空间，直到满足条件
        while True:
            time.sleep(15)
            print(get_free_space())
            if get_free_space() > 2147483648:
                folder_exsist()
                httpdfull.server_close()
                httpdfull.shutdown()
                httpfull_thread.join()
                break

def loginprocess():
    user_thread = threading.Thread(target=get_user_info, name="UserThread", daemon=True)
    user_thread.start()
    counter = 0
    while user is None and counter < 3:
        time.sleep(1)
        counter += 1
        if user is not None:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Login success ... ")
            break

    while True:
        if user is not None:
            break
        else:
            if user_thread.is_alive():
                httpd = HTTPServer(('0.0.0.0',8099), MyRequestHandler)
                http_thread = threading.Thread(target=httpd.serve_forever, name="Addon-Web", daemon=True)
                http_thread.start()
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Waittting for scan qrcode ... ")
                user_thread.join()
                if httpd:
                    httpd.server_close()
                    httpd.shutdown()
                    http_thread.join()
                    restart_program()

def create_threa_afterlogin():
    # 创建循环检查云盘空间线程
    space_thread = threading.Thread(target=check_space_periodically, daemon=True)
    space_thread.start()
    # 创建一个线程来执行定时任务
    run_schedule = threading.Thread(target=running_schedule, name="schedule", daemon=True)
    run_schedule.start()
    # 设置计划任务执行备份
    schedule.every().day.at(backup_time).do(simulate_backup)

def filter_and_print_date(records, key_name, num_to_keep):
    sorted_records = sorted(records, key=itemgetter('date'), reverse=True)
    if len(sorted_records) > num_to_keep:
        to_print = sorted_records[num_to_keep:]
    return to_print

def delete_backup_record_cloud(file_id):
    global drive_id
    ali = Aligo(level=logging.ERROR)
    try:
        ali.move_file_to_trash(file_id, drive_id)
        print(f"Successfully moved file {file_id} to trash.")
    except Exception as e:
        print(f"Error moving file {file_id} to trash. Error: {e}")

def delete_cloud():
    tobe_delete_cloud = filter_and_print_date(ls_cloud(folderid),'file_id',keep_days_cloud)
    if tobe_delete_cloud:
        print("Deleting the following cloud records:")
        for record in tobe_delete_cloud:
            #print(record['file_id'])
            delete_backup_record_cloud(record['file_id'])

def delete_backup_record_local(slug):
    global supervisor_token
    api_url = "http://supervisor/backups/" + slug
    if not supervisor_token:
        print("Error: Supervisor Token not found in environment variables.")
        return
    headers = {
        "Authorization": f"Bearer {supervisor_token}"
    }
    try:
        response = requests.delete(api_url, headers=headers)

        if response.status_code == 200:
            print(f"Backup record with slug '{slug}' deleted successfully.")
        else:
            print(f"Failed to delete backup record with slug '{slug}'. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while deleting backup record with slug '{slug}': {str(e)}")

def delete_local():
    tobe_delete_local = filter_and_print_date(ls_local(),'slug',keep_days_local)
    if tobe_delete_local:
        print("Deleting the following local records:")
        for record in tobe_delete_local:
            #print(record['slug'])
            delete_backup_record_local(record['slug'])

def delete_expired():
    delete_local()
    delete_cloud()

if __name__ == '__main__':
    user = space = None
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Checking Internet Connection ... ")
    while not check_internet():
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Waittting for internet connection ... ")
        time.sleep(5)

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Staring Home Assistant Aliyun Backup ... ")

    loginprocess()
    create_threa_afterlogin()
    handle_low_space()
    # 启动显示备份列表页面
    httpdhtml = HTTPServer(('0.0.0.0',8099), BackupFilesHandler)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" Serve Http protal  ... ")
    httpdhtml.serve_forever()
