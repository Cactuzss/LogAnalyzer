import json
import click
import asyncio
import platform

# for testing
import time

import regex as re

from modules import CachingJSON
from modules.api import get_failed_builds
from modules import Embedder, LabelClassifier
from modules import Configuration, AvailableArchitectures, APILabelClassifierType, APIEmbeddingType 
from modules import parser as Parser
from modules import collect_data

def generate_cluster(labels, texts):
    res: dict[int, list[dict]] = {}
    for i, label in enumerate(labels):
        if label not in res:
            res[label] = []
        res[label].append(texts[i])
    return res

async def main():

    failed_builds = get_failed_builds(Configuration.GeneralSettings.branch, Configuration.GeneralSettings.architecture.value)

    # LOG URLS
    failed_builds = [el.url for el in failed_builds]

    files = await Parser.get_log_by_links_array(failed_builds)
    #print(f"Got {len(files)} logs")

    embedder = Embedder(
        Configuration.EmbeddingSettings.model_name,
        Configuration.EmbeddingSettings.api_type,
        Configuration.EmbeddingSettings.api_base_url,
        Configuration.EmbeddingSettings.api_key
    )
    
    embeddings = embedder.create_embedding(failed_builds)
    labels = embedder.generate_labels(embeddings)
    
    clusters = generate_cluster(labels, files)
    for k in clusters:
        clusters[k] = clusters[k][:3]

    # Display clusters
    print()
    for k in clusters:
        print(f"Cluster {k}")
        for link in clusters[k]:
            print(f"\t {link["url"]}")
        print()

    labelClassifier = LabelClassifier(
        Configuration.LabelModelSettings.model_name,
        Configuration.LabelModelSettings.api_type,
        Configuration.LabelModelSettings.api_base_url,
        Configuration.LabelModelSettings.api_key
    )

    if Configuration.GeneralSettings.verbose:
        for k in clusters:
            el = collect_data(
                cluster_id=k,
                data=files,
                classifier=labelClassifier
            )           

            print(el)

            exit()

    return 

       



# Startup and configuration stuff
def is_x86_64() -> bool:
    return platform.machine().endswith('64')

def is_endpoint_valid(address: str) -> bool:
    # TODO: Check if url
    return re.match(pattern=r"^(?:\d{1,3}(?:\.|\:)){4}\d{1,5}$", string=address) is not None

@click.command()
@click.option("--arch", "-a",
              default=AvailableArchitectures.x86_64 if is_x86_64() else AvailableArchitectures.i586, 
              type=click.Choice(AvailableArchitectures),
              help=f"Sets branch architecture. Available options are: 'x86_64' and 'i586'")
@click.option("--branch", "-b", default=Configuration.GeneralSettings.branch, help="Sets beehive branch")
@click.option("--verbose", "-v", is_flag=True, 
              help="Set to true to more logs")
@click.option("--output", "-o", type=click.Path(writable=True, dir_okay=False),
              help="Set to true to more logs")

@click.option("--embedding_model_name", default=Configuration.EmbeddingSettings.model_name, type=click.STRING)
@click.option("--embedding_model_type", default=Configuration.EmbeddingSettings.api_type, type=click.Choice(APIEmbeddingType))
@click.option("--embedding_api_url", default="", type=click.STRING)
@click.option("--embedding_api_key", default="", type=click.STRING)

@click.option("--label_model_name", default=Configuration.LabelModelSettings.model_name, type=click.STRING)
@click.option("--label_model_type", default=Configuration.LabelModelSettings.api_type, type=click.Choice(APILabelClassifierType))
@click.option("--label_api_url", default="", type=click.STRING)
@click.option("--label_api_key", default="", type=click.STRING)

def startup(arch, branch, verbose, output, embedding_model_name, embedding_model_type, embedding_api_url, embedding_api_key,
            label_model_name, label_model_type, label_api_url, label_api_key):
    Configuration.GeneralSettings.architecture = arch
    Configuration.GeneralSettings.branch = branch
    Configuration.GeneralSettings.verbose = verbose
    Configuration.GeneralSettings.output_path = output


    Configuration.EmbeddingSettings.model_name = embedding_model_name
    Configuration.EmbeddingSettings.api_type = embedding_model_type
    Configuration.EmbeddingSettings.api_base_url = embedding_api_url
    Configuration.EmbeddingSettings.api_key = embedding_api_key

    if Configuration.EmbeddingSettings.api_type != APIEmbeddingType.SENTENCE_TRANSFORMERS:
        assert len(Configuration.EmbeddingSettings.api_base_url) > 0, "[ERROR]: You must specify embedding model api url if you using OPENAI_COMPATABLE api type"
        assert len(Configuration.EmbeddingSettings.api_key) > 0, "[ERROR]: You must specify embedding model api key if you using OPENAI_COMPATABLE api type"


    Configuration.LabelModelSettings.model_name = label_model_name
    Configuration.LabelModelSettings.api_type = label_model_type
    Configuration.LabelModelSettings.api_base_url = label_api_url
    Configuration.LabelModelSettings.api_key = label_api_key

    if Configuration.LabelModelSettings.api_type != APILabelClassifierType.TRANSFORMERS:
        assert len(Configuration.LabelModelSettings.api_base_url) > 0, "[ERROR]: You must specify label model api url if you are using OPENAI_COMPATABLE api type"
        assert len(Configuration.LabelModelSettings.api_key) > 0, "[ERROR]: You must specify label model api key if you are using OPENAI_COMPATABLE api type"

    
    #time_start = time.time()
    
    asyncio.run(main())
    
    #time_end = time.time()
    #print((time_end - time_start ))



if __name__ == '__main__':
    startup()
