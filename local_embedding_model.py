from pydantic import PrivateAttr
import torch
import numpy as np
from llama_index.core.embeddings import BaseEmbedding
from typing import Any, List
from transformers import BertModel, BertTokenizer

class LocalBertEmbedding(BaseEmbedding):

    def __init__(self,  **kwargs: Any):
        super().__init__(**kwargs)

    @classmethod
    def class_name(cls) -> str:
        return "bert-large-portuguese-cased"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        embedding = self.embed_text(query)
        return embedding.tolist()

    def _get_text_embedding(self, text: str) -> List[float]:
        embedding = self.embed_text(text)
        return embedding.tolist() 

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = [self.embed_text(text).tolist() for text in texts]
        return embeddings

    def embed_text(self, text):
        model_name = 'neuralmind/bert-large-portuguese-cased'
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertModel.from_pretrained(model_name)
        # Tokenizar o texto
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        
        # Passar os tokens pelo modelo BERT
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Extrair o embedding da última camada (ou pode usar a média das camadas)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        
        return embeddings
