import json
import requests
import jsonref


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


def call_function(path, func_args):
    response = requests.post(path, json=func_args)
    payment_instructions = response.json()

    # TODO: Pay it!

    response = requests.get(path + "?id=" + payment_instructions["id"])
    print(response.text)
    return response.json()


if __name__ == "__main__":
    import openai

    BASE_URL = "http://localhost:8000"

    openapi_spec = requests.get(f"{BASE_URL}/openapi.json").json()
    functions = openapi_to_functions(openapi_spec)

    tools = []
    func_name_to_path = {}
    for path, function in functions:
        print(path)
        tools.append(function)
        func_name_to_path[function["function"]["name"]] = BASE_URL + path.replace(
            "/spec", "/"
        )
        print(json.dumps(function, indent=2))
        print()
        print()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user.",
        },
        {"role": "user", "content": "Hi, what's the weather like in Tokyo?"},
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    print(response)
    if response.choices[0].message.tool_calls:
        func = response.choices[0].message.tool_calls[0].function
        call_function(func_name_to_path[func.name], json.loads(func.arguments))
