import streamlit as st
import time

def extractQuestion(topicType):
    question = '我是不是都不能吃豆製品？'
    return question


def checkAnswer(question, answer):
    comparison = 'Not yet'
    return comparison




st.title("CKD 腎臟衛教問答系統")
topicType = st.sidebar.selectbox(
    '是否需要詢問特定主題？',
    ['腎臟病各期衛教指引', '腎臟功能與常見檢查項目', '腎臟疾病分類與說明', '飲食建議與禁忌', '常用藥物與腎臟影響', '健保與資源資訊', '透析與腎臟移植資訊', '全選'])
st.sidebar.text(f'選擇類別：{topicType}')

if st.button('開始測驗!'):
    st.text("測驗開始!")
    nextQ = False
    question = extractQuestion(topicType)
    answer = st.text_area(f"問題:{question}")

    while nextQ == False:
        if st.button(f'提交 第0題!') == True:
            st.write("回答:", answer)
            #comparison = checkAnswer(question, answer)
            #st.text(f"比較: {comparison}")

            nextQ = True


print('9999')












