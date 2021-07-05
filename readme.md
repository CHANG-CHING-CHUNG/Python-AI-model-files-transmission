# AI 檔案傳輸程式 readme
###### tags: `鉅芯科技筆記`

# 使用步驟

## 傳輸方
1. 匯入 AiAiFIlesTransmission 類
```=python
from ai_files_transmission import AiFIlesTransmission
```
2. 將 AiFIlesTransmission 實例化，呼叫 start_sending_AI_files 傳入檔案路徑及 socket，成功回傳 True 失敗回傳 False
```=python
# AI 模型檔案所在路徑
DIRECTORY_PATH = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-06-23_z/1"
# 實例化
ai_files_transmission = AiFIlesTransmission()
# 將檔案路徑及 socket 傳進 start_sending_AI_files 方法執行
# 執行完畢後，傳輸成功的話回傳 True, 失敗回傳 False
# result = True/False
result = ai_files_transmission.start_sending_AI_files(DIRECTORY_PATH,socket)
```

## 接收方
1. 匯入 AiAiFIlesTransmission 類
```=python
from ai_files_transmission import AiFIlesTransmission
```
2. 將 AiFIlesTransmission 實例化，呼叫 start_sending_AI_files 傳入檔案路徑及 socket，成功回傳 True 失敗回傳 False
```=python
# 要接收 AI 檔案的路徑
target_dir_path = "/home/john/桌面/工作/測試/AI_model_transmission/dist"
# 實例化
ai_files_transmission = AiFIlesTransmission()
# 將要接收 AI 檔案的路徑及 socket 傳進 receive_AI_files 方法執行
# 執行完畢後，接收成功的話回傳 True, 失敗回傳 False
# result = True/False
result = ai_files_transmission.receive_AI_files(target_dir_path,socket)
```

## 示意圖

### 來源路徑
```=python
DIRECTORY_PATH = "/home/john/桌面/工作/測試/AI_model_transmission/AI_model_files/z_2021-06-23_z/1"
```
![](https://i.imgur.com/QtU011O.png)

### 接收路徑
```=python
target_dir_path = "/home/john/桌面/工作/測試/AI_model_transmission/dist"
```
會自動依照來源路徑的最後一個資料夾名稱建立同名資料夾，以上面為例，會建立名為 "1" 的資料夾，並在裡面存放檔案。

接收檔案完成的示意圖
![](https://i.imgur.com/CMQkjUN.png)
