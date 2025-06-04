import streamlit as st
from streamlit_chat import message
from timeit import default_timer as timer
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_community.chat_models import ChatOllama
from timeit import default_timer as timer




llm = ChatOllama(model="llama3")
# Neo4j configuration
neo4j_url = 'bolt://localhost:7687'
neo4j_user = 'neo4j'
neo4j_password = '12345678'

# Cypher generation prompt
cypher_generation_template = """
你是一位專精於 Neo4j 的專家，負責將使用者的中文問題轉換成簡單明確的 Cypher 查詢語法。請依照以下原則產生查詢語句：

1. 使用的語法必須相容 Neo4j 第 5 版。
2. 不要使用 EXISTS、SIZE、HAVING 等進階語法。
3. 查詢只使用在提供的「知識圖譜結構」中出現的節點與關係。
4. 所有與屬性有關的搜尋都請進行模糊比對，使用  `CONTAINS`
5. 在搜尋的時候可以使用'包含'關係進行搜尋，不需要搜尋特定節點，搜尋特定類別的節點，例如當詢問關於飲食建議時，搜尋Diet類別底下的所有節點，而不是搜尋Diet底下的特定節點，例如不要搜尋MATCH (c:Category)-[r:包含]-(d:Diet) WHERE d.name CONTAINS "豆製品"。
6. 搜尋時已能夠搜尋到結果為主，不需一定要搜尋到特定節點，改為搜尋特定類別的節點。
7. 善用Category底下的節點進行延伸，Category底下的節點皆為大範圍分類，包含腎臟病各期衛教指引, 腎臟功能與常見檢查項目, 腎臟疾病分類與說明, 飲食建議與禁忌, 常用藥物與腎臟影響, 健保與資源資訊, 透析與腎臟移植資訊。
8. 所有搜尋條件皆為「中文」，請確保產出的 Cypher 使用中文屬性與標籤。
9. 產出的查詢要盡量簡單易讀，適合用在腎臟疾病教育的場景。
10. Node type有以下種類:Answer、Category、Concept、Diet、Diseases、Drug、Education、Question、Question_type、Resource、Test、Treatment
11. Relation type有以下種類:Relation、包含、回答

知識圖譜結構（schema）：
{schema}

範例：
問題：有哪些飲食方式適合慢性腎臟病患者？
回答：```MATCH (c:Category)-[包含]-(p:Diet)
WHERE c.name contains "飲食建議與禁忌"
RETURN c, p;```

問題：哪些藥物會影響腎功能？
回答：```MATCH (c:Category)-[包含]-(p:Drug)
WHERE c.name contains "常用藥物與腎臟影響"
RETURN c, p;```

問題：{question}
"""

cypher_prompt = PromptTemplate(
    template=cypher_generation_template,
    input_variables=["schema", "question"]
)

CYPHER_QA_TEMPLATE = """你是一位腎臟健康衛教助理，根據提供的資訊，協助使用者以簡單、清楚的方式理解與腎臟健康有關的問題。
請以溫和、有條理的語氣進行回答，就像是在與人自然對話。
請不要提到「根據提供的資訊」這類語句，也避免重複問題本身。
請保持專業性，說話可以溫和易懂，但是也需保持專業性。
請務必使用繁體中文作答。

提供的資訊：
{context}

使用者問題：{question}
有幫助的回答：
"""

qa_prompt = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)
def connectNeo4j():
    try:
        graph = Neo4jGraph(url=neo4j_url, username=neo4j_user, password=neo4j_password)
        print("Successful Connect")
        #print(graph.schema)
    except:
        print("Connect fail")
        graph = ''
    return graph




def query_graph(user_input):
    graph = connectNeo4j()
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        allow_dangerous_requests=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt
    )
    result = chain(user_input)
    return result

def conclusionAnswer(firstResult, question):
    answer_prompt = PromptTemplate(
        input_variables=["firstResult", "question"],
        template="""你是一位腎臟健康衛教醫生，請將系統提供的腎臟衛教回應進行整合，確認回應語句流暢度，是否有不合邏輯的地方，
            回應皆須保持專業性以及語句清楚明瞭。
            請不要給使用者稱呼
            請務必使用繁體中文作答。

            提供的資訊：
            {firstResult}

            使用者問題：{question}
            有幫助的回答：
            """)
    formatted_prompt = answer_prompt.format(firstResult=firstResult, question=question)
    answer = llm.invoke(formatted_prompt)
    return answer.content



st.set_page_config(layout="wide")

if "user_msgs" not in st.session_state:
    st.session_state.user_msgs = []
if "system_msgs" not in st.session_state:
    st.session_state.system_msgs = []
title_col, empty_col, img_col = st.columns([2, 1, 2])

with title_col:
    st.title("CKD 腎臟衛教問答系統")
with img_col:
    st.image("https://dist.neo4j.com/wp-content/uploads/20210423062553/neo4j-social-share-21.png", width=200)

user_input = st.text_input("輸入問題   (輸入完成後請按下ENTER鍵)", key="input")
if user_input:
    if st.button("開始詢問"):
        with st.spinner("Processing your question..."):
            st.session_state.user_msgs.append(user_input)
            start = timer()
            try:
                result = query_graph(user_input)
                if 'result' not in result or not result['result']:
                    firstResult = "目前找不到相關資訊，請嘗試用不同的方式再次提問。"
                    cypher_query = ""
                    database_results = ""
                else:
                    firstResult = result['result']
                    print('result',result)
                    intermediate_steps = result["intermediate_steps"]
                    cypher_query = intermediate_steps[0]["query"]
                    database_results = intermediate_steps[1]["context"]
            except Exception as e:
                st.write("Failed to process question. Please try again.")
                print(e)
            print('firstResult',firstResult)
            answer = conclusionAnswer(firstResult,user_input)
            print('answer',answer)
            st.session_state.system_msgs.append(answer)
        st.write(f"花費時間: {timer() - start:.2f}s")

        if st.session_state["system_msgs"]:
            for i in range(len(st.session_state["system_msgs"]) - 1, -1, -1):
                message(st.session_state["system_msgs"][i], key=str(i) + "_assistant")
                message(st.session_state["user_msgs"][i], is_user=True, key=str(i) + "_user")

