import streamlit as st
from supabase import create_client, Client
from src.configs.appconfig import appConfig
from supabase.lib.client_options import ClientOptions

# Inicializar o cliente do Supabase
st.cache_resource()
def get_supabase_client():
    options = ClientOptions(
        schema="vecs"
    )
    url: str = appConfig.SUPABASE_URL
    key: str = appConfig.SUPABASE_KEY
    supabase: Client = create_client(url, key, options)
    supabase.postgrest.schema("vecs")

    return supabase


SUPABASE_CLIENT = get_supabase_client()

