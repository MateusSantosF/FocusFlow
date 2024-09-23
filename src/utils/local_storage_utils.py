from streamlit_javascript import st_javascript
import json

def get_from_local_storage(k):
    v = st_javascript(
        f"JSON.parse(localStorage.getItem('{k}'));"
    )
    # Retorna uma string vazia se o valor for um dicionário vazio
    return v if isinstance(v, str) else ""

def set_to_local_storage(k, v):
    jdata = json.dumps(v)
    st_javascript(
        f"localStorage.setItem('{k}', JSON.stringify({jdata}));"
    )
