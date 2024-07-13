import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
import string

load_dotenv()

llm = OpenAI(openai_api_key='')

# Define prompt templates
prompt = PromptTemplate(
    template="""system
    You are a helpful assistant aiding users in finding their dream property.
    Your current task is to decide whether the user input has sufficient details mentioned, such as the name of the city.
    Make sure the name of the city is mentioned in the prompt.
    If it is, then respond with 'yes', else 'no'.

    YOUR RESPONSE MUST BE BINARY.

    ONLY RESPOND WITH 'yes' or 'no'.

    User prompt :\n\n {user_input} \n\n
    
    assistant
    """,
    input_variables=["user_input"],
)

chain1 = prompt | llm | StrOutputParser()

details_needed_prompt = PromptTemplate(
    template="""system
    You are a helpful assistant aiding users in finding their dream property.
    Currently, the user has not mentioned sufficient details about their needed property and is ambiguous.
    We need at least the name of the city where the apartment is needed.

    Read the user prompt below, identify if the city name is missing and if it is, ask the user to mention more details, i.e., the name of the city.

    User prompt :\n\n {user_input} \n\n
    
    assistant
    """,
    input_variables=["user_input"],
)

chain2 = details_needed_prompt | llm | StrOutputParser()

def initial_decider(user_input):
    return chain1.invoke({"user_input": user_input})

def details_asker(user_input):
    return chain2.invoke({"user_input": user_input})

# Setting up StateGraph
class GraphState(TypedDict):
    user_input: str
    needs_details: str = ""
workflow = StateGraph(GraphState)

# Define nodes
def identify_type(state):
    user_content = state['user_input']
    decision = initial_decider(user_content)
    state['needs_details'] = decision
    
    # print(decision)

def does_not_need_details(state):
    print("Proceeding with user request")


def new_promp(state):
    new = string(input("ebter new prompt"))
def ask_for_details(state):
    res = details_asker(state['user_input'])
    print(res)

def rout(state):
    user_content = state['user_input']
    decision = initial_decider(user_content)
    output_string = decision.replace(" ", "")
    print(output_string)
    if output_string == "yes" or output_string=="Yes":
        # print("in yes branch")
        return "proceed"
        
    else:
        # print("in no branch")
        return "ask_for_details"
        
        
    

workflow.add_node("make_decision", identify_type)
workflow.add_node("proceed", does_not_need_details)
workflow.add_node("ask_for_details", ask_for_details)
workflow.add_node("enter_new_prompt", new_promp)
# workflow.add_node("check", rout)


workflow.add_edge("ask_for_details", "enter_new_prompt")
workflow.add_edge( "enter_new_prompt" , "make_decision")
workflow.add_edge("proceed", END)

workflow.add_conditional_edges(
    "make_decision",
    rout,
    {
        "ask_for_details": "ask_for_details",
        "proceed": "proceed",
    },
)

workflow.set_entry_point("make_decision")


app = workflow.compile()

# Initial state and invoke the app
input_text = "looking for an apartment with a budget of 20million in lahore"
initial_state = {"user_input": input_text}
out = app.invoke(initial_state)


