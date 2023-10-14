from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI()


<<<<<<< Updated upstream
def get_area(user_input_string):
    llm_output = chat(
        [
            HumanMessage(
                content=f"You are a helpful AI assistant. User has provided a textual description of usable area for installing a solar panel. {user_input}. Extract the area in sq ft from the description: "
            )
        ]
    )
    return float(llm_output)
=======
def get_usable_area(user_input_string):
    llm_output = chat([HumanMessage(content=f"You are a helpful AI assistant. User has provided a textual description of usable area for installing a solar panel. {user_input}. Extract the usable area in sq ft from the description: ")])
    return float(llm_output)

def get_total_area(user_input_string):
    llm_output = chat([HumanMessage(content=f"You are a helpful AI assistant. User has provided a textual description of usable area for installing a solar panel. {user_input}. Extract the total area in sq ft from the description: ")])
    return float(llm_output)
>>>>>>> Stashed changes
