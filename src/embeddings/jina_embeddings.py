from langchain.embeddings.base import Embeddings
from transformers import AutoTokenizer, AutoModel
import torch

class JinaEmbeddings(Embeddings):
    def __init__(self, model_name="jinaai/jina-embeddings-v2-base-en", batch_size=16):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.batch_size = batch_size

    def embed_documents(self, texts):
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            inputs = self.tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
            all_embeddings.extend(embeddings.tolist())
        return all_embeddings

    def embed_query(self, text):
        inputs = self.tokenizer(
            [text],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
        return embeddings[0].tolist()