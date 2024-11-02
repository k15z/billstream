import json
import openai
import colorama
from colorama import Fore, Style, Back
from sdk import AgentToolkit
from sdk.wallets import PrivyWallet
from sdk.spinner import Spinner
colorama.init()


if __name__ == "__main__":
    tk = AgentToolkit(
        wallet=PrivyWallet(
            secret_key="sk_test_51O8332JQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQ"
        )
    )

    messages = [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user.",
        },
        {"role": "user", "content": input(Fore.YELLOW + "User: " + Style.RESET_ALL)},
    ]

    with Spinner():
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tk.tools(),
        )

    while True:
        if response.choices[0].message.tool_calls:
            id = response.choices[0].message.tool_calls[0].id
            func = response.choices[0].message.tool_calls[0].function
            print("=" * 100)
            print(Fore.GREEN + "Tool Call:" + Style.RESET_ALL)
            print(func)
            print()

            result = tk.call(func.name, func.arguments)
            print("=" * 100)
            print(Fore.GREEN + "Tool Output:" + Style.RESET_ALL)
            print(str(result)[:100] + ("..." if len(str(result)) > 100 else ""))
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
            messages.append(
                {"role": "tool", "content": json.dumps(result), "tool_call_id": id}
            )

            with Spinner():
                response = openai.chat.completions.create(
                    model="gpt-4o", messages=messages, tools=tk.tools()
                )

        else:
            print("=" * 100)
            print(Fore.BLUE + "Assistant:" + Style.RESET_ALL)
            print(response.choices[0].message.content)
            print()

            messages.append(response.choices[0].message)
            print("=" * 100)
            messages.append(
                {
                    "role": "user",
                    "content": input(Fore.YELLOW + "User: " + Style.RESET_ALL),
                }
            )
            print()

            with Spinner():
                response = openai.chat.completions.create(
                    model="gpt-4o", messages=messages, tools=tk.tools()
                )
