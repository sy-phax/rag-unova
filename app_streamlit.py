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

st.title("Assistant UNOVA: CVC — Chauffage, Ventilation, Qualité de l'air")

question = st.text_input("question:")

if st.button("send"):
    if question:
        reponse = requests.post(
            f"{BACKEND_URL}/ask",
            json={"texte": question}
        )
        resultat = reponse.json()

        st.write(resultat["reponse"])

        st.write("**sources :**")
        for source in resultat["sources"]:
            st.write("-", source)