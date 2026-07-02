#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:08:53 2026

@author: syphaxmedjkane
"""

from fastapi import FastAPI
from pydantic import BaseModel

from config import DOSSIER_PDF
from ingestion import build_index
from rag import retrieve, build_prompt, generate


build_index(DOSSIER_PDF)


app = FastAPI()


class Question(BaseModel):
    texte: str


@app.post("/ask")
def ask(question: Question):
    resultats = retrieve(question.texte)
    prompt = build_prompt(question.texte, resultats)
    reponse = generate(prompt)

    sources = []
    for m in resultats["metadatas"][0]:
        if m["source"] not in sources:
            sources.append(m["source"])

    return {"reponse": reponse, "sources": sources}