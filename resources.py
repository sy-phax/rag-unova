#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:05:20 2026

@author: syphaxmedjkane
"""

import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL_NAME

model = SentenceTransformer(EMBEDDING_MODEL_NAME)
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)