from enum import Enum

class Configuration:
    architecture: str = ""
    branch: str = "sisyphus"
    model_type: str = ""
    remote_address: str = ""
    verbose: bool = False
    output_path: str = "./log-analyzer.out"

    class AvailableArchitectures(Enum):
        x86_64 = "x86_64"
        i586 = "i586"

    class ModelTypes(Enum):
        local = "local"
        remote = "remote"

