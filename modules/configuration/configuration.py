from enum import Enum

class AvailableArchitectures(Enum):
    x86_64 = "x86_64"
    i586 = "i586"

class APIEmbeddingType(Enum):
    OPENAI_COMPATABLE = 'openai',
    SENTENCE_TRANSFORMERS = 'sentence_transformers',

class APILabelClassifierType(Enum):
    OPENAI_COMPATABLE = 'openai',
    TRANSFORMERS = 'transformers',


class Configuration:
    class GeneralSettings:
        branch: str = "sisyphus"
        verbose: bool = False
        output_path: str = "./log-analyzer.out"
        architecture: str = ""

    class EmbeddingSettings:
        model_name: str = "all-minilm"
        api_type: APIEmbeddingType = APIEmbeddingType.OPENAI_COMPATABLE
        api_base_url: str = ""
        api_key: str = ""

    class LabelModelSettings:
        model_name: str = "all-minilm"
        api_type: APILabelClassifierType = APILabelClassifierType.OPENAI_COMPATABLE
        api_base_url: str = ""
        api_key: str = ""
