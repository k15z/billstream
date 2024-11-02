import json
import requests
import jsonref
from typing import Any

def openapi_to_functions(openapi_spec):
    functions = []

    api_spec = jsonref.replace_refs(openapi_spec)

    for path, methods in api_spec["paths"].items():
        for method, spec in methods.items():
            function_name = spec.get("operationId")
            if not path.endswith("/spec"):
                continue

            desc = spec.get("description") or spec.get("summary", "")

            schema = {"type": "object", "properties": {}}

            req_body = (
                spec.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if req_body:
                schema["properties"] = req_body["properties"]

            functions.append(
                (
                    path,
                    {
                        "type": "function",
                        "function": {
                            "name": function_name,
                            "description": desc,
                            "parameters": schema,
                        },
                    },
                )
            )

    return functions

class AgentToolkit:

    def __init__(self, base_url: str, wallet: Any):
        self.wallet = wallet
        self.base_url = base_url

        response = requests.get(self.base_url + "/openapi.json")
        self._tools = []
        self._name_to_path = {}
        for path, func in openapi_to_functions(response.json()):
            self._tools.append(func)
            self._name_to_path[func["function"]["name"]] = self.base_url + path.replace(
            "/spec", "/"
        )

    def tools(self, query: str=""):
        # TODO: Vector embedding or something?
        return self._tools
    
    def call(self, tool_name: str, tool_args: dict):
        payment_instructions = self.initiate(tool_name, tool_args)
        if self.wallet:
            # TODO: Actually do this :p
            self.wallet.pay(payment_instructions)
        print(payment_instructions)
        return self.fetch(tool_name, payment_instructions["id"])
    
    def initiate(self, tool_name: str, tool_args: dict):
        path = self._name_to_path[tool_name]
        print(path, tool_args)
        response = requests.post(path, json=json.loads(tool_args))
        payment_instructions = response.json()
        return payment_instructions
    
    def fetch(self, tool_name: str, id: str):
        path = self._name_to_path[tool_name]
        response = requests.get(path + "?id=" + id)
        return response.json()
