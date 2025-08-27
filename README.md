# Method Finance MCP

Method Finance MCP is a project that leverages the [Method Finance API](https://docs.methodfi.com/) to interact with the platform using a Large Language Model (LLM). This enables users to perform tasks using natural language commands.

## Features

- Communicate with Method Finance via LLM or CLI.
- Expose Method Finance API tasks in natural language.
- Easily test API connectivity and create individuals.

## Available Tools

- `hello_world` — Test your API key.
- `create_individual` — Create a new individual with a description.

## Setup

1. **Clone the repository:**
    ```bash
    git clone <repo-url>
    cd method-fi-mcp
    ```

2. **Install dependencies:**
    ```bash
    uv sync
    ```

3. **Configure your environment:**
    - Go to [Method Finance](https://app.methodfi.com/) and create a dev/sandbox/prod environment.
    - Obtain your API key.
    - Create a `.env` file in the project root:

      ```env
      METHOD_API_KEY=your_api_key_here
      ```

4. **Start the server:**
    ```bash
    python -m server.main
    ```

## Usage

- **Connect with Claude MCP:**  
  Integrate with Claude for natural language task execution.

- **Use the CLI MCP client:**  
  ```bash
  python -m client.client
  ```

## Documentation

- [Method Finance Docs](https://docs.methodfi.com/)

## License

See [LICENSE](./LICENSE) for details.