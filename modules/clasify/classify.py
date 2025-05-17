import io
from enum import Enum

from modules.configuration.configuration import Configuration, APIEmbeddingType, APILabelClassifierType
from sklearn.cluster import AgglomerativeClustering as ClusterDetector
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

from pydantic import BaseModel

import numpy as np
from PIL import Image


PCA_COMPONENTS = 50

class Embedder:
    def __init__(
            self, 
            model_name: str = Configuration.EmbeddingSettings.model_name,
            api_type: APIEmbeddingType = Configuration.EmbeddingSettings.api_type,
            api_base_url: str | None = None,
            api_key: str | None = None,
        ):
        self.model_name = model_name
        self.api_type = api_type

        match self.api_type:
            case APIEmbeddingType.OPENAI_COMPATABLE:
                import openai
                self.api_base_url = api_base_url
                self.api_key = api_key
                self.api_client = openai.Client(
                    api_key=self.api_key,
                    base_url=self.api_base_url
                )

            case APIEmbeddingType.SENTENCE_TRANSFORMERS:
                try:
                    from sentence_transformers import SentenceTransformer
                except:
                    raise ImportError("Failed to import sentence_transformers! Install sentence_transformers to inference localy")
                
                import torch
                self.device = 'cpu' if not torch.cuda.is_available() else 'cuda'

                self.model = SentenceTransformer(self.model_name)
                
            case _:
                raise ValueError("Unknown API")

    def create_embedding(self, texts: str | list[str], show_progress_bar: bool = Configuration.GeneralSettings.verbose) -> np.ndarray:
        match self.api_type:
            case APIEmbeddingType.OPENAI_COMPATABLE:
                data = self.api_client.embeddings.create(input=texts, model=self.model_name).data
                embeddings = [data_package.embedding for data_package in data]
                embeddings = np.asarray(embeddings, dtype=np.float32)

            case APIEmbeddingType.SENTENCE_TRANSFORMERS:
                self.model = self.model.to(self.device)
                embeddings = self.model.encode(texts, show_progress_bar=show_progress_bar)
                self.model = self.model.to('cpu')

            case _:
                raise ValueError("Unknown API")
        
        return embeddings

    @staticmethod
    def generate_labels(embeddings: np.ndarray, embeddings_components: int = PCA_COMPONENTS) -> np.ndarray:
        return ClusterDetector(n_clusters=None, distance_threshold=2, compute_full_tree=True).fit(embeddings).labels_

    @staticmethod
    def generate_plot(embeddings: np.ndarray, labels: np.ndarray | None = None, alpha: float = 0.7) -> Image.Image:
        reduced = PCA(n_components=3).fit_transform(embeddings)
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        scatter = ax.scatter(
            reduced[:, 0], 
            reduced[:, 1], 
            reduced[:, 2], 
            c=labels, 
            cmap='Spectral',
            # s=40,
            alpha=alpha,
            edgecolor='w',
            depthshade=False
        )
        
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_zlabel('Component 3')
        plt.title(f'3D PCA Cluster Visualization')
        
        legend = fig.colorbar(scatter, ax=ax, pad=0.1)
        legend.set_label('Cluster ID')
        
        ax.view_init(elev=25, azim=45)
        
        filedata = io.BytesIO()
        plt.savefig(filedata)
        filedata.seek(0)

        return Image.open(filedata)



class Response(BaseModel):
    text: str


class LabelClassifier:
    def __init__(
            self, 
            model_name: str = Configuration.LabelModelSettings.model_name,
            api_type: APILabelClassifierType = APILabelClassifierType.OPENAI_COMPATABLE, 
            api_base_url: str | None = None,
            api_key: str | None = None,
        ):
        self.model_name = model_name
        self.api_type = api_type

        match self.api_type:
            case APILabelClassifierType.OPENAI_COMPATABLE:
                import openai
                self.api_base_url = api_base_url
                self.api_key = api_key
                self.api_client = openai.Client(
                    api_key=self.api_key,
                    base_url=self.api_base_url
                )

            case APILabelClassifierType.TRANSFORMERS:
                try:
                    from transformers import utils
                    from transformers import pipeline
                    utils.logging.set_verbosity_error()
                except:
                    raise ImportError("Failed to import transformers! Install transformers to inference localy")
                
                import torch
                self.device = 'cpu' if not torch.cuda.is_available() else 'cuda'

                self.pipe = pipeline("text-generation", model=self.model_name, device=self.device, torch_dtype=torch.bfloat16)
                
            case _:
                raise ValueError("Unknown API")

    def generate_log_description(self, text: str, label: int) -> str:
        messages = [
            {"role": "system", "content": "Extract information from log file according to JSON schema."},
            {
                "role": "user",
                "content": f"```\n{text}\n```",
            },
        ],

        match self.api_type:
            case APILabelClassifierType.OPENAI_COMPATABLE:
                result = self.api_client.responses.parse(
                    input=messages,
                    model=self.model_name,
                    text_format=Response
                ).output_parsed
                

            case APILabelClassifierType.TRANSFORMERS:
                result = self.pipe(messages)

            case _:
                raise ValueError("Unknown API")
