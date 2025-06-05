# 腎臟衛教機器人（CKD Chatbot）

這是一個腎臟衛教聊天機器人，目的是協助病人或民眾了解慢性腎臟病（CKD）相關的知識與照護資訊。

## Features

-  回答常見症狀、飲食建議、治療選項（如血液透析、腹膜透析、腎移植）
-  根據使用者輸入的關鍵字進行互動式回覆
-  具備簡易網頁介面，方便操作與查詢

## Architecture

- Python 3.9
- Streamlit — 前端介面
- Neo4j — 用於知識圖譜儲存與查詢
- Git — 版本控制

## Installation

### Prerequirements
  - Python 3.9
  - Ollama llama3 8B

### Dependencies
  Install all required dependencies using the provided requirements.txt file:
  ```bash
  pip install -r requirements.txt
  ```

### Set up
  Clone this repository:
  
   ```bash
   git clone [repository-url]
   cd CKD_chatbot
   ```

    Note: Replace [repository-url] with the actual URL of this repository.

###  Running the Application:
  To run the Streamlit app:
  ```
  streamlit run CKD_chatbot.py
  ```
  This will start the application and open it in your default web browser (typically at http://localhost:8501).

## Usage
  - 使用修改後請上傳github，並加上commit註明修改內容
  - 資料集會放在Notion (https://www.notion.so/CKD-208577f3294880b089dcc22e31702ff2?source=copy_link)



  
