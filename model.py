from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
import os

# os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"
chat = ChatOpenAI()


def get_usable_area(user_input_string):
    llm_output = chat([HumanMessage(content=f"You are a helpful AI assistant. User has provided a textual description of usable area for installing a solar panel. {user_input}. Extract the usable area in sq ft from the description: ")])
    #return float(llm_output)
    return 100

def get_total_area(user_input_string):
    llm_output = chat([HumanMessage(content=f"You are a helpful AI assistant. User has provided a textual description of usable area for installing a solar panel. {user_input}. Extract the total area in sq ft from the description: ")])
    #return float(llm_output)
    return 100
