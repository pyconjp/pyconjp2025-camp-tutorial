import json

import requests
import streamlit as st

st.title("Geminiに聞く")


q = st.text_input("質問")
models = st.multiselect(
    "models",
    options=["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash-preview-05-20"],
)
roles = st.text_area("roles").split()

data = {
    "key": "pyconjp2025",
    "q": q,
    "options": {"models": models, "roles": roles, "max_tokens": 1024},
}
if st.button("質問"):
    res = requests.post("http://localhost:8000/multi-async", json=data)
    st.write(res.status_code)
    # st.write(res.content)
    content = json.loads(res.content)
    for d in content.get("data", []):
        st.write(
            f"id:{d.get('id')} / model: {d.get('args', {}).get('model_name')}"
            f" / role:{d.get('args', {}).get('role')}"
        )
        st.write(d.get("result"))
        st.divider()
