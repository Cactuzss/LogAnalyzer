class cli_params:
    base_repo: str = "sisyphus"

    def __init__(self, params: list[str]) -> None:
        if ("-r" in params):
            ind: int = int(params.index("-r") + 1)
            self.repo = params[ind]
        else:
            self.repo = cli_params.base_repo

    def help(self) -> str:
        pass
