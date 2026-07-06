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


def lister_fichiers_pdf(dossier_pdf):
    fichiers = []
    for racine, dossiers, noms_fichiers in os.walk(dossier_pdf):
        for nom_fichier in noms_fichiers:
            if nom_fichier.endswith(".pdf"):
                categorie = os.path.basename(racine)
                chemin = os.path.join(racine, nom_fichier)
                fichiers.append({
                    "nom_fichier": nom_fichier,
                    "chemin": chemin,
                    "categorie": categorie
                })

    return fichiers


def nettoyer_sources_orphelines(sources_indexees, fichiers):
    noms_presents = []
    for f in fichiers:
        noms_presents.append(f["nom_fichier"])

    for source in sources_indexees:
        if source not in noms_presents:
            supprimer_source(source)


def build_index(dossier_pdf):
    fichiers = lister_fichiers_pdf(dossier_pdf)
    sources_existantes = get_sources_indexees()

    nettoyer_sources_orphelines(sources_existantes, fichiers)

    sources_existantes = get_sources_indexees()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    tous_les_chunks = []

    for f in fichiers:
        if f["nom_fichier"] not in sources_existantes:
            doc = fitz.open(f["chemin"])
            compteur_chunk = 0

            for numero_page, page in enumerate(doc, start=1):
                texte_page = page.get_text()
                chunks = splitter.split_text(texte_page)

                for chunk in chunks:
                    tous_les_chunks.append({
                        "texte": chunk,
                        "source": f["nom_fichier"],
                        "categorie": f["categorie"],
                        "page": numero_page,
                        "chunk_id": compteur_chunk
                    })
                    compteur_chunk += 1

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
        metadatas.append({
            "source": c["source"],
            "categorie": c["categorie"],
            "page": c["page"],
            "chunk_id": c["chunk_id"]
        })

    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    print(f"{len(tous_les_chunks)} nouveaux chunks indexés (total : {collection.count()})")
