# project-pegasus

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Project Pegasus a **framework for building agentic commerce experiences** using the **Agentic Commerce Protocol (ACP)**.

## Features

- **Pluggable architecture**: Configure stores, embeddings, prompts, and LLM providers of your choice.
- **Agentic commerce tools**: Define tools with runtime context.
- **Configuration-first**: YAML + `.env` approach for secure, environment-driven settings.

## Project Structure

```text
project-pegasus/
├─ libs/
│ ├─ core/ # Core abstractions (Stores, Agents, Context)
│ ├─ providers/ # Implementations and registry
├─ services/ # Domain-specific business logic
│ ├─ responses/ # Agent tools and response orchestration
│ ├─ products/ # Products management
│ ├─ orders/ # Order lifecycle management
│ ├─ checkout/ # Instant checkout
│ ├─ payments/ # Delegated payments
├─ settings.yaml # Static configuration
├─ config.py # Loads .env and settings.yaml

```

## Installation / Environment Setup

1. **Install dependencies**

```bash
# Create a virtual environment and install dependencies
uv sync
```

2. **Configure environment**

```ini
# Create a .env file for secrets:

MONGO_URI=<your-mongodb-uri>
EMBEDDINGS_MODEL_API_KEY=<your-embeddings-model-api-key>
CHAT_MODEL_API_KEY=<your-chat-model-api-key>
```
