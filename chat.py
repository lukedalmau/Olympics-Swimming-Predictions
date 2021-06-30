import streamlit as st

#create cache object for the "chat"


@st.cache(allow_output_mutation=True)
def Chat():
    return []


chat = Chat()
name = st.sidebar.text_input("Name")
message = st.sidebar.text_area("Message")
if st.sidebar.button("Post chat message"):
    chat.append((name, message))

if len(chat) > 10:
    del(chat[0])

try:
    names, messages = zip(*chat)
    chat1 = dict(Name=names, Message=messages)
    st.table(chat1)
except ValueError:
    st.title("Enter your name and message into the sidebar, and post!")
