from pydantic import BaseModel
from typing import Dict, Any

NotebookId = str

class ExecutionParameters(BaseModel):
    notebook_id: NotebookId
    parameters: Dict[str, Any]