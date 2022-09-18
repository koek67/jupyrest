Notebooks

```
GET /api/v1/notebooks/:id -> get config.json
POST /api/v1/notebooks/:id/execute
POST /api/v1/notebooks/:id/parameterize
```

Notebook Instances

```
GET /api/v1/notebook_instances/:id
GET /api/v1/notebook_instances/:id/output
GET /api/v1/notebook_instances/:id/html?report=true
GET /api/v1/notebook_instances/:id/ipynb


GET /api/v1/notebook_instances/:id/status
GET /api/v1/notebook_instances/:id/editor
```

Instance metadata:

```json
{
    "notebook": "io_contract_example",
    "executed": false,
    "parameters": {
        "foo": "FOO",
        "bar": 500
    },
    "exception": "str"
}
```