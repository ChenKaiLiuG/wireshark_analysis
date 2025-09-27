# wireshark_analysis
用 Python 建一個本地網頁應用，分析 .pcap 並生成漂亮圖表和紀錄檔
## 安裝依賴
 - 安裝 Python
   ```bash
   sudo apt install python3-pip
   ```
 - 安裝wireshark依賴庫
   ```bash
   pip3 install pyshark dash plotly --break-system-packages
   ```
 - 下載腳本
   ```bash
   git clone https://github.com/ChenKaiLiuG/wireshark_analysis.git
   ```
## 使用方式
 - 打開腳本，設定`.pcap`檔案路徑
   ```python
   PCAP_DIR = "/var/log/pcaps"  # 替換為你的 .pcap 儲存路徑
   ```
 - 執行腳本
   ```bash
   python3 pcap_analyzer.py
   ```
 - 本地開啟 `http://localhost:8060` (或用其他設備訪問 `http://本地IP:8060`)
## 頁面說明
### 給非專業用戶的易懂圖表 
 - 網頁顯示彩色餅圖（協議分佈），點擊可互動放大。
 - 簡單標題和圖例，適合新手理解。
### 給專業人士的詳細紀錄檔 
 - 網頁下半部分顯示文字日誌（時間、來源 IP、目的 IP）。
 - 點「Download Log」下載完整日誌檔案。
