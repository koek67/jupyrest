from nbformat import NotebookNode
from typing import Tuple, Optional, Any, Dict
from pydantic import BaseModel, Json
from abc import ABC, abstractmethod
from jsonschema import validate, ValidationError
from papermill.parameterize import parameterize_notebook

ValidationResult = Tuple[bool, Optional[str]]
NotebookId = str

class ExecutionParameters(BaseModel):
    notebook_id: NotebookId
    parameters: Dict[str, Any]

class NotebookConfig(BaseModel):
    input: Dict
    output: Dict

class NotebookResolver(ABC):

    @abstractmethod
    def has_notebook(self, notebook_id: NotebookId) -> bool:
        raise NotImplemented

    @abstractmethod
    def get_notebook(self, notebook_id: NotebookId) -> NotebookNode:
        raise NotImplemented

    @abstractmethod
    def has_config(self, notebook_id: NotebookId) -> bool:
        raise NotImplemented

    @abstractmethod
    def get_config(self, notebook_id: NotebookId) -> NotebookConfig:
        raise NotImplemented

def get_resolver() -> NotebookResolver:
    raise NotImplemented

def validate_input(self, params: ExecutionParameters) -> ValidationResult:
    # 1. get config
    input_schema = get_resolver().get_config(notebook_id=params.notebook_id).input
    # 2. TODO: resolve the nbschema://s
    # 3. validate json
    try:
        validate(instance=params.parameters, schema=input_schema)
    except ValidationError as ve:
        return (False, str(ve))
    return (True, None)

def parameterize(self, params: ExecutionParameters) -> NotebookNode:
    # 1. TODO: inject model refs
    # 2. create parameter cell
    #   - we don't want to call resolve_notebook if we don't have to
    raise NotImplemented

def execute(self, notebook: NotebookNode):
    raise NotImplemented
