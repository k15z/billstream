import json
from sdk import AgentToolkit

if __name__ == "__main__":
    import openai

    tk = AgentToolkit(base_url="http://localhost:8000", wallet=None)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user.",
        },
        {"role": "user", "content": input("User: ")},
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tk.tools(),
    )

    if response.choices[0].message.tool_calls:
        id = response.choices[0].message.tool_calls[0].id
        func = response.choices[0].message.tool_calls[0].function
        print("=" * 100)
        print("Tool Call:")
        print(func)
        print()

        result = tk.call(func.name, func.arguments)
        print("=" * 100)
        print("Tool Output:")
        print(result)
        print()

        messages.append(
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": id,
                        "type": "function",
                        "function": {
                            "name": func.name,
                            "arguments": func.arguments,
                        },
                    }
                ],
            }
        )
        messages.append({"role": "tool", "content": json.dumps(result), "tool_call_id": id})

        response = openai.chat.completions.create(model="gpt-4o", messages=messages)
        print("=" * 100)
        print("Assistant:")
        print(response.choices[0].message.content)
        print()
