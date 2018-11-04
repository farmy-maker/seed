# Seed Client

Project for Maker Faire Taipei 2018

## 制作方法

## 1. 準備零件

零件列表

| 名稱                 | 圖片                                                         | 型號     | memo                                                         | 購買 link (參考)                                    |
| -------------------- | ------------------------------------------------------------ | -------- | ------------------------------------------------------------ | -------------------------------------------- |
| Raspberry Pi         | ![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Raspberry-Pi-2-Bare-BR.jpg/1280px-Raspberry-Pi-2-Bare-BR.jpg?1501684061910) | -        | -                                                            | http://akizukidenshi.com/catalog/g/gM-11425/ |
| 光照傳感器           | ![](https://www.mysensors.org/uploads/57cc6e4595afb8801e529dab/image/BH1750.jpg.png) | BH1750   | [I²C](https://zh.wikipedia.org/zh-hans/I²C)                  | http://www.aitendo.com/product/10240         |
| 溫度傳感器（土壤用） | ![](http://www.mouser.cn/images/mouserelectronics/images/TO_92_3_t.jpg) | DS18B20+ | [1-Wire](https://www.maximintegrated.com/jp/app-notes/index.mvp/id/1796) | http://akizukidenshi.com/catalog/g/gI-05276/ |
| 濕度傳感器（土壌用） | ![](https://www.dfrobot.com/wiki/images/thumb/a/af/IMGP5217.jpg/300px-IMGP5217.jpg) | SEN0114  | -                                                            | http://akizukidenshi.com/catalog/g/gM-07047/ |
| 晶體管陣列           | ![](http://akizukidenshi.com/img/goods/L/I-02771.jpg)        | TD62064  |                                                              | 耐圧50V                                      |
| A/D 轉換器           | ![](http://akizukidenshi.com/img/goods/L/I-11987.jpg)        | MCP3004  | SPI                                                          | http://akizukidenshi.com/catalog/g/gI-11987/ |
| 2.2ｋΩ電阻           |                                                              |          |                                                              | http://akizukidenshi.com/catalog/g/gR-25222/ |
| 5.1ｋΩ電阻           |                                                              |          |                                                              | http://akizukidenshi.com/catalog/g/gR-25512/ |
| 恒流驅動             | -                                                            | -        | -                                                            | -                                            |
| 植物育成用LED        | -                                                            | -        | RED-　660nm　3W BLUE- 445nm　3W                              | -                                            |
| 澆水用的水泵         | -                                                            | -        | -                                                            | http://amzn.asia/iwOQDbv                     |
| 面包板               | ![](http://akizukidenshi.com/img/goods/C/P-09257.JPG)        | -        | -                                                            | -                                            |
| 面包板用DC接口       |                                                              |          |                                                              | http://akizukidenshi.com/catalog/g/gK-05148  |
| 跳線                 | ![](http://akizukidenshi.com/img/goods/L/C-05159.jpg)        | -        | -                                                            | -                                            |

※ Raspberry Pi 還需要、SD 卡和電源
※ 另外您也許需要鼠標, 鍵盤, 顯示屏和 HDMI 線

## 2. 組裝

您可以參考下面的電路圖, 通過跳線來連接各個零件

### fritzing 圖

![](https://i.imgur.com/OAxzC9N.png)

### 電路圖

![](https://i.imgur.com/OCPGo1u.png)

## 3. 寫入程式

### 3.1. Raspberry Pi 的初始化

```
pi@raspberrypi:~ $ sudo raspi-config
```

在 Interfacing Options > 
請把 Camera, I2C, 1-Wire 設定為 ON 的狀態。

### 3.2 Farmy 代碼的安裝

1. 先安裝需要使用到的 lib

```
pi@raspberrypi:~ $ sudo apt-get install git python-pip python-dev python-opencv python-scipy python-pygame libjpeg-dev
```

1. 通過 GitHub 下載 farmy 代碼

```
pi@raspberrypi:~ $ cd /home/pi
pi@raspberrypi:~ $ git clone https://github.com/farmy-maker/seed.git
pi@raspberrypi:~ $ cd seed
pi@raspberrypi:~/seed $
```

1. 通過 pip 來安裝

```
pi@raspberrypi:~ $ pip install -r requirements.txt
```

### 3.3 設置環境參數

Seed/config.ini を編集

```
[device]
camera_type = web       # 攝像頭模式, web 或者
dht_pin = 14        # 控制的 pin 口
led_pin = 23        # led 燈的 pin 口
pump_pin = 24       # 水泵的 pin 口
camera_light_threshold = 20   # 攝像頭光照的閾值 (當低於這個光照度時就停止拍照)

[sys]
image_path = static/images/snapshots/   # 攝像頭存儲位置
mode = demo # 運行模式 demo or debug                          
fetch_data_interval = 10  # 數據獲取間隔 (分)
fetch_image_interval = 10  # 照片獲取間隔 (分)
trigger_interval = 10  # 條件出發時間 (分)
chart_interval = 30  # data 曲線 x 軸單位 (分)
chart_before = 1440  # data 曲線圖範圍 (分)

[auth]
user = dev  # demo 用, 主頁 basic 認證用戶名
pass = pass  # demo 用, 主頁 basic 認證密碼
```

### 3.4 運行

```bash
pi@raspberrypi:~/seed $ python main.py
webcam Init.
Farmy device init.
Starting...
WebSocket transport not available. Install eventlet or gevent and gevent-websocket for improved performance.
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

這樣就可以通過瀏覽器打開樹莓派的 ip 的 5000 號端口來訪問主控制頁面. 後台的抓取數據與拍照的程式也已經啟動
