import os
import streamlit as st
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import AgentType,initialize_agent,load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

def create_agent_chain():
    chat = ChatOpenAI(
        model = "gpt-4o-mini",
        streaming = True,
    )
    
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    
    tools = load_tools(["ddg-search","wikipedia"])
    return initialize_agent(
        tools,
        chat,
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs=agent_kwargs,
        memory=memory,
    )
    # return initialize_agent(tools,chat,agent=AgentType.OPENAI_FUNCTIONS)

if "agent_chain" not in st.session_state:
    st.session_state.agent_chain = create_agent_chain()
    
st.write("OPENAI_API_KEY:", st.secrets["OpenAI API Key"])
# openai_api_key = st.secrets["OpenAI API Key"]
# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.", icon="🗝️")
# else:

#     # Create an OpenAI client.
os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key
    
st.title("🎈 langchain-streamlit-app")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up")
if prompt:

    st.session_state.messages.append({"role": "user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        callback = StreamlitCallbackHandler(st.container())
        response = st.session_state.agent_chain.run(prompt, callbacks=[callback])
        # agent_chain = create_agent_chain()
        # response = agent_chain.run(prompt,callbacks=[callback])
        # chat_model = ChatOpenAI(
        #     model = "gpt-3.5-turbo"
        # )
        # messages = [HumanMessage(content=prompt)]
        # response = chat_model.invoke(messages)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant","content":response})
