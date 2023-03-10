# Home Assistant Add-on: Hass Remote

Sets up an SSL proxy with Hass Remote and redirects traffic from http port to https port.
and get a sub domain access your Home Assistant from anywhere~!

Easy to control your home from outside.
Easy to build in webhook applications.(eg. OwnTracks, GpsLogger)

出门在外也可控制 Home Assistant
轻松接入基于 Webhook 的应用程序（如 OwnTracks, GpsLogger）

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield]

## About

Sets up an SSL proxy with reverse web server. It is typically used to forward SSL internet traffic while allowing unencrypted local traffic to/from a Home Assistant instance.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

## Installation

Follow these steps to get the add-on installed on your system:
根据下面提示进行安装：

1. Navigate in your Home Assistant frontend to **Supervisor** -> **Add-on Store**.
   通过Github连接添加自定义库。
2. Find the "Hass Remote" add-on and click it.
   找到Hass Remote的加载项安装。
3. Click on the "INSTALL" button.
   点击安装按钮。

## How to use

1. Start your addon.
   点击运行按钮。
2. Get your key from addon web interface.
   稍等十几秒从加载项的网页界面获取Key
3. fill the key in to addon configuration.
   把获取到的Key填写到加载项的配置页面。
4. Save configuration.
   点击保存按钮。
5. Restart the add-on.
   重启加载项。
6. Have some patience and wait a couple of minutes.
   等待加载项启动，大概需要十几秒。
7. Check the add-on log output to see the result.
   可以从加载项的日志部分查看错误信息。
