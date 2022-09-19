Functions

```
GET  /workspaces/:id/notebooks
GET  /workspaces/:id/notebooks/:id
POST /workspaces/:id/notebooks/:id/execute
POST /workspaces/:id/notebooks/:id/parameterize

# Later
GET  /workspaces/:id/notebooks?id=$id
POST /workspaces/:id/notebooks/execute?id=$id
POST /workspaces/:id/notebooks/parameterize?id=$id
```

Notebook Instances

```
GET /workspaces/:id/notebook_executions/:id
GET /workspaces/:id/notebook_executions/:id/output
GET /workspaces/:id/notebook_executions/:id/html?report=true
GET /workspaces/:id/notebook_executions/:id/notebook
GET /workspaces/:id/notebook_executions/:id/editor
```

Instance metadata:

```json
{
    "id": "some-guid",
    "parent_id": null,
    "notebook_id": "io_contract_example",
    "attempts": [
        {
            "attempt_id": "",
            "start_time": "",
            "end_time": "",
            "failure": {
                "type": "",
                "details": ""
            }
        }
    ],
    "parameters": {
        "foo": "FOO",
        "bar": 500
    }
}
```