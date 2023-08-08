import openai
import re
import streamlit as st
from prompts import get_system_prompt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

st.title("☃️ Frosty")

# Initialize the chat messages history
openai.api_key = st.secrets.OPENAI_API_KEY

# Initialize Supabase client
supabase_url = 'https://nxfgdavcafafaoyxxweh.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im54ZmdkYXZjYWZhZmFveXh4d2VoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODc3NzM2NzcsImV4cCI6MjAwMzM0OTY3N30.8pcPs50Vm0ysLIRi_BXMTh6tiP2tu5uEqrPSDHpTeec'

supabase = create_client(supabase_url, supabase_key)
            

if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        for delta in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            response += delta.choices[0].delta.get("content", "")
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1)

            message["results"] = supabase.from('lms_basemeta_table').select(sql)
            st.dataframe(message["results"])
        st.session_state.messages.append(message)
