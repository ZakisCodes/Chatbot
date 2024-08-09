import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser


st.title("Chat")
st.sidebar.html(
    """
   <style>
   [data-testid="stStatusWidget"]{
         visibility: hidden;
         height: 0;
         position: fixed
          }
    </style>
"""
)
def get_response(user_query, chat_history):

    template = """
    You are a helpful assistant. Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {user_question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm  = ChatGroq(
    temperature=0,
    model="llama3-70b-8192",
    api_key=os.getenv("GROQ_API") )
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    }) 

# session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi, My name is Mick"),
    ]

#conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("ai", avatar='🎃'):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("human", avatar='👀'):
            st.write(message.content)


# chat
user_query = st.chat_input("Enter your prompt here")
if user_query is not None and user_query != " ":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message('ai'):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))
        

    st.session_state.chat_history = [AIMessage(content=response)]