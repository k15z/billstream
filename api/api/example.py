import requests
import jsonref
from pprint import pprint as pp

def openapi_to_functions(openapi_spec):
    functions = []

    api_spec = jsonref.replace_refs(openapi_spec)

    for path, methods in api_spec["paths"].items():
        for method, spec in methods.items():
            # 2. Extract a name for the functions.
            function_name = spec.get("operationId")
            if not path.endswith("/spec"):
                continue

            # 3. Extract a description and parameters.
            desc = spec.get("description") or spec.get("summary", "")

            schema = {"type": "object", "properties": {}}

            req_body = (
                spec.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if req_body:
                schema["properties"]["requestBody"] = req_body

            params = spec.get("parameters", [])
            if params:
                param_properties = {
                    param["name"]: param["schema"]
                    for param in params
                    if "schema" in param
                }
                schema["properties"]["parameters"] = {
                    "type": "object",
                    "properties": param_properties,
                }

            functions.append(
                {"type": "function", "function": {"name": function_name, "description": desc, "parameters": schema}}
            )

    return functions


if __name__ == "__main__":
    openapi_spec = requests.get("http://localhost:8000/openapi.json").json()
    functions = openapi_to_functions(openapi_spec)

    for function in functions:
        pp(function)
        print()
        print()
        print()
        