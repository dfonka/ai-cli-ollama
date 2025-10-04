# AI CLI (Ollama)

A Python-based CLI that talks to your **local Ollama** instance.

**Author:** Derick Fonka  
**Repository:** https://github.com/dfonka/ai-cli-ollama

[![Python](https://img.shields.io/badge/python-%3E%3D3.9-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://github.com/dfonka/ai-cli-ollama/actions/workflows/ci.yml/badge.svg)](https://github.com/dfonka/ai-cli-ollama/actions)

---

## Features

- `ai-cli list` — List all models currently installed in your local Ollama.
- `ai-cli run -m <model> "your prompt"` — Send a prompt to a model and view the response.
- Supports `--stream` (stream tokens), `--system` (system prompt), and `--options` (JSON model parameters).
- Accept prompt via file (`-f prompt.txt`) or via piped stdin.
- Specify alternate Ollama host and request timeouts.

---

## Quick Start

1. **Install Ollama** and run it locally: <https://ollama.com/>

2. Clone your repo and set up your dev environment:

    ```bash
    git clone https://github.com/dfonka/ai-cli-ollama.git
    cd ai-cli-ollama
    python -m venv .venv
    source .venv/bin/activate      # On Windows: .venv\Scripts\activate
    pip install -e .
    ```

3. Verify the CLI helps:

    ```bash
    ai-cli --help
    ```

4. List your models:

    ```bash
    ai-cli list
    # If it's empty, you can pull a model, e.g.:
    #   ollama pull llama3:latest
    ```

5. Run a prompt:

    ```bash
    ai-cli run -m llama3 "Write a short poem about collaboration."
    ```

6. Use streaming, file, or JSON options:

    ```bash
    ai-cli run -m llama3 --stream "Count to 5."
    ai-cli run -m llama3 -f prompt.txt
    echo "Explain blue/green deployment." | ai-cli run -m llama3
    ai-cli run -m llama3 --options '{"temperature":0.2}' "Be succinct."
    ```

7. Override host or timeout:

    ```bash
    ai-cli --host http://127.0.0.1:11434 --timeout 120 list
    # Or export:
    export OLLAMA_HOST=http://127.0.0.1:11434
    ai-cli list
    ```

---

## Error Handling

- Notifies if Ollama isn’t reachable or the host is wrong.
- Suggests using `ai-cli list` when a model isn't found.
- Validates the JSON passed to `--options`.
- Disallows empty prompts.

---

## Development & Tests

- Organized under `ai_cli/`:  
  - `ollama_client.py`: wrapper for Ollama HTTP APIs  
  - `cli.py`: the `click` command definitions  
- Tests (via `pytest`) included in `tests/test_cli.py`
- To run tests:

    ```bash
    pytest -q
    ```

---

## BONUS: Kubernetes Diagnostics (Optional)

See [BONUS.md](BONUS.md) for how this CLI could be extended to assist with Kubernetes issue diagnosis, with a simulated workflow.

---

## License

This project is licensed under the [MIT License](LICENSE).  

---

## About the Author

**Derick Fonka** is a software engineer with interest in AI tooling, DevOps automation, and clean CLI/UX experiences.  
Feel free to browse more of his projects at https://github.com/dfonka.

---# ai-cli-ollama
