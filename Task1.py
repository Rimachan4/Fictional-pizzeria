import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Streamlit setup
st.title("Pizza Planet")
st.write("Welcome to the virtual pizza world! How can I help you?")

# Initialize the language model (llm)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

if "messages" not in st.session_state:
    st.session_state.messages = []
    

# Context
context = '''
You are a Pizza shop owner that can take orders from the customers based on the menu you have. Show the formatted menu to the user when they ask.
Act like a real owner and suggest customers items and interact respectfully.Calculate total cost after every item is ordered and display it.
Based on the order from the customer, you need to sum the total amount and communicate it to the customer. If the item is not available, you need to tell 
the customer that the 'Item is not available' and ask the user to pick from the options you have. You don't need to 
set up any payment method, you only need to show the final amount.
'''

# Menu
menu = '''
pepperoni pizza, price= large(12.95), medium(10.00), small(7.00) 
cheese pizza large (10.95), medium(9.25), small(6.50) 
eggplant pizza large (11.95), medium(9.75), small(6.75) 
fries large (4.50), small (3.50) 
greek salad (7.25) 
Toppings: 
extra cheese (2.00) 
mushrooms (1.50) 
sausage (3.00) 
canadian bacon (3.50) 
AI sauce (1.50) 
peppers (1.00) 
Drinks: 
coke large (3.00), medium (2.00), small (1.00) 
sprite large (3.00), medium (2.00), small (1.00) 
bottled water (5.00)
'''

# Prompt template
template = """
You are a helpful AI assistant. You have access to the following documents: {context}. 
Answer only from the context.
You also have access to chat history : {chat_history}.
If you don't know the answer, say you do not know.
Menu options: {menu}
User question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

# Output parser
output_parser = StrOutputParser()

def get_response(question):
    chain = prompt | llm | output_parser 
    formatted_prompt = {
        "context": context,
        "menu": menu,
        "question": question,
        "chat_history": st.session_state.messages}
    
    result = chain.invoke(formatted_prompt)
    return result


# Getting user input
question = st.chat_input("Input text here")
if question:
    st.session_state.messages.append(HumanMessage(content=question))
    ai_response = get_response(question)
    st.session_state.messages.append(AIMessage(content=ai_response))
    
    
# Formatting each chat in history 
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        st.markdown(f"<p style='color:orange;'>You:</p> {message.content}", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True) 
    elif isinstance(message, AIMessage):
        st.markdown(f"<p style='color:red;'>Pizza Planet:</p> {message.content}", unsafe_allow_html=True) 
        st.markdown("<br>", unsafe_allow_html=True) 
