import streamlit as st
import random
import time
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain import OpenAI, LLMMathChain
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
import os
st.set_page_config(
    page_title="GPT-4", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed"
)

os.environ['OPENAI_API_KEY'] = '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'

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


llm = OpenAI(temperature=0)
llm_math = LLMMathChain.from_llm(llm, verbose=True)

search = DuckDuckGoSearchRun()



llm = ChatOpenAI(temperature=0)


# Load the tool configs that are needed.
llm_math_chain = LLMMathChain(llm=llm, verbose=True)
tools = [
    Tool.from_function(
        func=llm_math.run,
        name="Calculator",
        description="useful for when you need to answer questions about math",
        # coroutine= ... <- you can specify an async method if desired as well
    ),

    Tool.from_function(
        func=search.run,
        name="Search",
        description="useful for when you need to the web to answer questions. Be very specific with your queries",
        # coroutine= ... <- you can specify an async method if desired as well
    ),

    Tool.from_function(
        func=wikipedia.run,
        name="WikiSearch",
        description="useful for when you need to answer questions that have a person or place of things in history. Good if you want to search wikipedia",
        # coroutine= ... <- you can specify an async method if desired as well
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history")

llm=OpenAI(temperature=0)
agent = initialize_agent(
    tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory,
    temperature=2,presence_penalty=1,max_tokens=16384, model='gpt-3.5-turbo-16k-0613'

)



st.title("GPT - 4")
st.markdown("### Created By Nishanth")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
xyz = st.chat_input("What is up?")
if prompt := xyz:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    if xyz == None:
        print("")
    else:
        yz = agent.run(str(xyz))

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = str(yz)
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
if xyz == None:
    xyz = "1"
else:
    xyz = xyz
print(xyz)
