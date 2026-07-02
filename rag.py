#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:07:31 2026

@author: syphaxmedjkane
"""

import requests
from resources import model, collection
from config import OLLAMA_URL, OLLAMA_MODEL_NAME


def retrieve(question, n=3):
    question_embedding = model.encode([question]).tolist()
    resultats = collection.query(query_embeddings=question_embedding, n_results=n)
    return resultats


def build_prompt(question, resultats):
    contexte = "\n\n".join(resultats["documents"][0])
    prompt = f"""Tu es un assistant technique spécialisé en chauffage, ventilation et qualité de l'air intérieur (à partir d'une base documentaire limitée à ces sujets).
Réponds à la question uniquement à partir du contexte fourni ci-dessous.
Si le contexte ne contient pas la réponse, ou si la question sort de ton domaine, dis-le clairement plutôt que d'inventer une réponse.

Contexte :
{contexte}

Question : {question}

Réponse :"""
    return prompt


def generate(prompt, model_name=OLLAMA_MODEL_NAME):
    reponse = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": model_name, "prompt": prompt, "stream": False}
    )
    return reponse.json()["response"]