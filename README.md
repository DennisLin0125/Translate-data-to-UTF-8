# LabVIEW data 轉換多國語言

## 使用方式:

## 編寫`config.json`
```json
{
  "config":{
    "language": ["cn","jp","kr","tw"],
    "file_list": ["main.txt"]
  }
}
```
### 產生依賴
```bash
pip freeze > requirements.txt
```
### 安裝依賴
```bash
pip install -r requirements.txt
```
### build exe檔
```bash
pyinstaller --onefile mainTran.py
```
### 產生的`dist`資料夾內的`exe`檔就是整個專案的執行檔
