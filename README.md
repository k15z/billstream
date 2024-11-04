# billstream
AgentToolkit enables agents to discover and pay for tools, anywhere. By dynamically sourcing the services an agent needs to accomplish its mission, we’ve built a global payment fabric where agents can stream micro-payments for any service, with or without an API.

New "tools" can be added easily through straightforward configuration, enabling use cases like trip planning and automated outreach on LinkedIn and other platforms and any combination of services imaginable.

## Components

 - [js] Website
    - List tools
    - Click on tools to see a code snippet

 - [api] Backend for website + host all the API's
    - List tools
    - Implement tools; for each tool:
        - returns 402 status code response with payment info
        - validate the payment
        - return the response with the real data and stuff

 - [sdk] SDK with examples
    - An SDK with an example.py that does cool stuff!
