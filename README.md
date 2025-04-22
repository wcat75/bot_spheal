# Discord Bot Spheal 

這是一個基於 [Python Discord Bot Template](https://github.com/kkrypt0nn (https://krypton.ninja)) 修改而來的 Discord 機器人，原始專案授權條款為 [Apache License 2.0](LICENSE)。  
本專案擴充了指令管理、角色權限控制、嵌入訊息發送與自動同步 slash commands 的功能。

---

## 🙏 致謝與原始來源

本專案基礎架構源自於：

- 原專案名稱：`Python Discord Bot Template`
- 原作者：[Krypton](https://github.com/kkrypt0nn)
- 原始專案連結：[https://github.com/kkrypt0nn/Python-Discord-Bot-Template/](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/)

原始程式碼遵循 Apache License 2.0，並保留授權聲明與重要標註。

---

## 🔧 本專案修改重點

...

---

## ⚙️ 開發環境與安裝方式

### ✅ 環境需求

- Python 3.12+
- `discord.py==2.3.2`
- `.env` 檔案存放機密資料（如 Bot Token）

### ✅ 安裝步驟

```bash
git clone https://github.com/你的帳號/你的專案名稱.git
cd 你的專案名稱
pip install -r requirements.txt
```

建立 .env 並填入以下內容：
``` bash
env
複製
編輯
DISCORD_TOKEN=你的機器人Token
```

## 🚀 啟動機器人

```bash
複製
編輯
python bot.py
機器人啟動後將自動載入所有 Cogs 並同步 slash 指令。
```

## 🤝 協作方式

...

## 📄 授權條款（License）

本專案遵循 Apache License 2.0。

根據授權條款：

您可自由使用、修改、發佈本程式碼

您應保留原始授權聲明與版權資訊

修改後請註明修改來源（可參考本 README 範例）

如需更多資訊，請參考官方授權條款： https://www.apache.org/licenses/LICENSE-2.0

---

## 📦 附帶檔案

你應該保留以下檔案一併放在 GitHub 專案根目錄：

1. ✅ `LICENSE`（維持原本 Apache 2.0 原文）