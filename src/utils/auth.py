# src/auth.py
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

def carregar_config():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def criar_autenticador():
    config = carregar_config()
    stauth.Hasher.hash_passwords(config['credentials'])
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']['emails']
    )
    return authenticator

def salvar_config(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
