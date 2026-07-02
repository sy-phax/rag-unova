#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:06:31 2026

@author: syphaxmedjkane
"""

import os
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from resources import model, collection


def supprimer_source(nom_fichier):
    collection.delete(where={"source": nom_fichier})
    print(f"{nom_fichier} retiré de l'index")


def get_sources_indexees():
    tous = collection.get(include=["metadatas"])

    sources = []
    for m in tous["metadatas"]:
        if m["source"] not in sources:
            sources.append(m["source"])

    return sources


def build_index(dossier_pdf):
    sources_existantes = get_sources_indexees()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    tous_les_chunks = []

    for nom_fichier in os.listdir(dossier_pdf):
        if nom_fichier.endswith(".pdf") and nom_fichier not in sources_existantes:
            chemin = os.path.join(dossier_pdf, nom_fichier)
            doc = fitz.open(chemin)

            texte_complet = ""
            for page in doc:
                texte_complet += page.get_text()

            chunks = splitter.split_text(texte_complet)

            for i, chunk in enumerate(chunks):
                tous_les_chunks.append({
                    "texte": chunk,
                    "source": nom_fichier,
                    "chunk_id": i
                })

    if not tous_les_chunks:
        print(f"Aucun nouveau document à indexer (base actuelle : {collection.count()} chunks)")
        return

    texts = []
    for c in tous_les_chunks:
        texts.append(c["texte"])

    embeddings = model.encode(texts).tolist()

    ids = []
    for c in tous_les_chunks:
        ids.append(f"{c['source']}_{c['chunk_id']}")

    metadatas = []
    for c in tous_les_chunks:
        metadatas.append({"source": c["source"], "chunk_id": c["chunk_id"]})

    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    print(f"{len(tous_les_chunks)} nouveaux chunks indexés (total : {collection.count()})")