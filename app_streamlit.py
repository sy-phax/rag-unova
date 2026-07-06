#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:28:14 2026

@author: syphaxmedjkane
"""

import streamlit as st
import requests

try:
    BACKEND_URL = st.secrets["BACKEND_URL"]
except (KeyError, FileNotFoundError):
    BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="assistant unova")

st.markdown(
    """
    <div style="text-align: center;">
        <h1>assistant unova</h1>
        <p style="color: gray; font-size: 1.1em;">
            chauffage, ventilation, isolation, performance énergétique
        </p>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("ask something...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("searching for an answer..."):
            try:
                reponse = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={"texte": question},
                    timeout=30
                )
                resultat = reponse.json()
                texte_reponse = resultat["reponse"]

                sources_texte = "\n\n**sources :**\n"
                for s in resultat["sources"]:
                    sources_texte += f"- [{s['fichier']} (page {s['page']})]({s['url']}#page={s['page']})\n"

                st.write(texte_reponse + sources_texte)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": texte_reponse + sources_texte
                })
            except requests.exceptions.RequestException:
                message_erreur = "impossible to connect with backend"
                st.error(message_erreur)
                st.session_state.messages.append({"role": "assistant", "content": message_erreur})
