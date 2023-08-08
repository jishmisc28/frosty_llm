import streamlit as st
import openai
from supabase_py import create_client, Client
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

## Validate Supabase connection ##
supabase_url = 'https://nxfgdavcafafaoyxxweh.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im54ZmdkYXZjYWZhZmFveXh4d2VoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODc3NzM2NzcsImV4cCI6MjAwMzM0OTY3N30.8pcPs50Vm0ysLIRi_BXMTh6tiP2tu5uEqrPSDHpTeec'

supabase = create_client(supabase_url, supabase_key)

#conn = st.experimental_connection("snowpark")
#df = conn.query("select current_warehouse()")
df = supabase.table("lms_basemeta_table").select("*").execute()
st.write(df)

## Validate OpenAI connection ##
openai.api_key = st.secrets["OPENAI_API_KEY"]

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "What is Streamlit?"}
  ]
)

st.write(completion.choices[0].message.content)
