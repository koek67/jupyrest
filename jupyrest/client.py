"""Helper methods for interacting with Jupyrest's
REST API."""
from typing import Dict, Optional, Union, List
import requests
import urllib.parse
from dataclasses import dataclass
from pydantic import BaseModel
BASE_URL = "http://localhost:5050/api/NotebookExecutions"
from jupyrest.plugin import JupyrestPlugin, PluginManager
from jupyrest.errors import InputSchemaValidationError, BaseError
from jupyrest.resolvers import LocalDirectoryResolver
from jupyrest.executors import IPythonNotebookExecutor
from jupyrest.nbschema import NotebookSchemaProcessor, ModelCollection
from pathlib import Path
from IPython.display import HTML, JSON, display
from jupyrest.workers.http import notebook_to_html
import asyncio
import warnings
from jupyrest.workers.base import Worker
import json
from nbclient.util import just_run, run_sync
from pprint import pprint
warnings.filterwarnings("ignore")
model_collection = ModelCollection()
notebooks_dir = Path(__file__).parent.parent / "sample_notebooks"
plugin = JupyrestPlugin(resolver=LocalDirectoryResolver(notebooks_dir=notebooks_dir), executor=IPythonNotebookExecutor(), nbschema=NotebookSchemaProcessor(model_collection))
resolver = plugin.get_resolver()
nbschema = plugin.get_nbschema()
plugin_manager = PluginManager()
plugin_manager.register("default", plugin)
worker = Worker(plugin_manager)

class NotebookResponse(BaseModel):
    id: str
    status: str
    notebook: str
    parameters: Dict
    ipynb: str
    html: str
    output: Optional[Union[Dict, List]] = None

    def __repr__(self) -> str:
        return f"<NotebookResponse executionId={self.id}, notebook={self.notebook}>"

def display_notebook(nb, report=False):
    return display(HTML(notebook_to_html(nb, report)))

def get_notebook(notebook: str, report=False):
    return resolver.resolve_notebook(notebook)

def get_config(notebook: str):
    return json.loads(json.dumps(resolver.resolve_config(notebook), indent=4))

async def parameterize_notebook(notebook: str, parameters: Dict):
    res = await worker.execute_notebook_async("default", notebook, parameters, parameterize_only=True)
    if isinstance(res, InputSchemaValidationError):
        raise Exception(res.validation.error)
    return res


async def execute_notebook(notebook: str, parameters: Dict):
    res = await worker.execute_notebook_async("default", notebook, parameters, parameterize_only=False)
    if isinstance(res, BaseError):
        raise Exception(repr(BaseError))
    return res