import torch
from typing import Any, List
from transformers import BertModel, BertTokenizer
from llama_index.core.embeddings import BaseEmbedding
from pydantic import PrivateAttr

class LocalBertEmbedding(BaseEmbedding):
    # Definindo atributos privados que não são considerados como campos pela Pydantic
    _tokenizer: BertTokenizer = PrivateAttr()
    _model: BertModel = PrivateAttr()

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        model_name = 'neuralmind/bert-large-portuguese-cased'
        self._tokenizer = BertTokenizer.from_pretrained(model_name)
        self._model = BertModel.from_pretrained(model_name)

    @classmethod
    def class_name(cls) -> str:
        return "bert-large-portuguese-cased"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)
    
    def _get_query_embedding(self, query: str) -> List[float]:
        embedding = self.embed_text(query)
        return embedding.tolist()

    def _get_text_embedding(self, text: str) -> List[float]:
        embedding = self.embed_text(text)
        return embedding.tolist()

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.embed_texts(texts)
        return [embedding.tolist() for embedding in embeddings]

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Função que aceita uma lista de textos e retorna uma lista de embeddings.
        Esta função será passada como 'embedding_function' para o Vector Store.
        """
        return self._get_text_embeddings(texts)

    def embed_text(self, text: str):
        # Tokenizar o texto 
        inputs = self._tokenizer(
            text,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=512
        )

        # Passar os tokens pelo modelo BERT
        with torch.no_grad():
            outputs = self._model(**inputs)

        # Extrair o embedding da última camada
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()

        return embeddings

    def embed_texts(self, texts: List[str]) -> List[torch.Tensor]:
        # Tokenizar os textos
        inputs = self._tokenizer(
            texts,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=512
        )

        # Passar os tokens pelo modelo BERT
        with torch.no_grad():
            outputs = self._model(**inputs)

        # Extrair os embeddings da última camada
        embeddings = outputs.last_hidden_state.mean(dim=1)

        return embeddings
