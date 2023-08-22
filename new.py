# Bring in deps
import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
os.environ['OPENAI_API_KEY'] = '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'
f = open('/Users/nishanthsadagopa/Desktop/LangChainNotebooks-UNZIP-ME/API_KEY.txt')
os.environ['OPENAI_API_KEY'] = f.read()
from langchain import OpenAI
from langchain.utilities import PythonREPL
from langchain.tools import DuckDuckGoSearchResults
# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.retrievers import WikipediaRetriever
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import load_tools
import os
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)
search = DuckDuckGoSearchResults()
wiki = WikipediaRetriever()
from langchain import OpenAI, LLMMathChain

llm = OpenAI(temperature=0)
llm_math = LLMMathChain.from_llm(llm, verbose=True)

python_repl = PythonREPL()

tools = [
    Tool(
        name="python repl",
        func=python_repl.run,
        description="useful for when you need to use python to answer a question. You should input python code"
    )
]

wiki_tool = Tool(
    name='wikipedia',
    func=wiki.run,
    description="Useful for when you need to look up a topic, country or person on wikipedia"
)

search_tool = Tool(
    name='duckduckgo',
    func=search.run,
    description="Useful for when you need to do a search on the internet to find information that another tool does no provide. Be specific in your search"
)

math_tool = Tool(
    name='LLMMATHCHAIN',
    func=llm_math.run,
    description="Useful for when you need to do math"
)
tools.append(wiki_tool)
tools.append(search_tool)
tools.append(math_tool)

# App framework
st.title('🤖🔗 GPT - 4 Text Generator')
st.write("""Embark on a journey into the future of artificial intelligence with GPT 4,
 a cutting-edge language model that pushes the boundaries of human-machine interaction.
  Developed by Nishanth Sadagopa, This code is a improved version of GPT 3.5""")
st.header("More Advanced Features")
st.write("""


Enhanced Accuracy: GPT-4 demonstrates significantly improved accuracy and content quality compared to GPT-3.5, thanks to advanced training techniques and expanded datasets.

Link Understanding: GPT-4 understands and interacts with links in text, following URLs and providing summaries of linked content for more informative responses.

Natural Conversations: With a more seamless conversational flow, GPT-4 maintains context across multiple turns, leading to coherent and engaging interactions.

Rich Vocabulary: GPT-4 boasts an even larger vocabulary, excelling in explaining complex topics and specialized domains.

Commonsense Reasoning: GPT-4's improved commonsense reasoning leads to more accurate responses that align better with human-like understanding.

""")
st.write("")
st.write("")
prompt = st.text_input('Plug in your prompt here')

# Check if the prompt contains a link
text_in_link = ""
if "http" in prompt:
    link_start = prompt.find("http")
    link_end = prompt.find(" ", link_start)
    if link_end == -1:
        link_end = len(prompt)
    text_in_link = prompt[link_start:link_end]
    prompt = prompt.replace(text_in_link, "")

# Process the prompt using the agent_executor
processed_prompt = str(prompt) + "Do not use the tools if it is a greeting" + text_in_link
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize the agent with modified prompt
agent_executor = initialize_agent(
    agent="conversational-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    memory=memory
)
x = agent_executor.run(processed_prompt)

# Display the output
st.write(str(x))
