# python-kiwoom: Automated Kiwoom REST API Wrapper

This project aims to demonstrate and facilitate the automated creation of a Python wrapper class for the Kiwoom REST API, leveraging the capabilities of Cline for streamlined development. The primary goal is to provide a convenient and automated way to interact with Kiwoom's trading functionalities.

## Current Features

The wrapper currently supports the following functionalities:

*   **Environment Variable Configuration:** Automatically loads API `appkey` and `secretkey` from a `.env` file, ensuring secure and flexible configuration.
*   **Dynamic API Server Selection:** Configures the API endpoint (real or mock) based on the `KIWOOM_API_SERVER_TYPE` environment variable, allowing for easy switching between development and production environments.
*   **Authentication:** Includes a robust authentication mechanism to fetch and manage access tokens required for API calls.
*   **Basic Stock Information Retrieval:** Provides a function (`ka10001`) to request fundamental information for a given stock code (e.g., Samsung Electronics - `005930`).
*   **Pydantic Models for API Responses:** Utilizes Pydantic for strict data validation and clear modeling of API request and response structures, ensuring data integrity and ease of use.

## How to Run

To run the example demonstrating authentication and stock information retrieval:

1.  Ensure you have `uv` installed for dependency management.
2.  Install project dependencies:
    ```bash
    uv pip install -e .
    ```
3.  Make sure your `.env` file in the root directory contains your `KIWOOM_APP_KEY`, `KIWOOM_SECRET_KEY`, and `KIWOOM_API_SERVER_TYPE` (e.g., `real` or `mock`).
4.  Execute the main client script:
    ```bash
    python -m kiwoom.client
    ```

## Kiwoom REST API Documentation

This project is designed to automate interactions based on the official Kiwoom REST API documentation. The `키움 REST API 문서.pdf` file, which can be downloaded from the Kiwoom website, is placed in the root directory of this project. This document serves as the primary reference for automating various API functionalities through this wrapper.

## Cline MCP Servers

Cline is configured with several Model Context Protocol (MCP) servers to extend its capabilities and facilitate various development tasks. Below is a list of the installed MCP servers, their installation methods, and their primary purposes:

### 1. `github.com/AgentDeskAI/browser-tools-mcp`

*   **Installation Method:** `npx @agentdeskai/browser-tools-mcp@latest`
*   **Purpose:** Provides tools for browser interaction, including taking screenshots, retrieving console logs, and running various audits (accessibility, performance, SEO, best practices). This server enables automated browser testing and web application analysis.

### 2. `github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking`

*   **Installation Method:** `npx -y @modelcontextprotocol/server-sequential-thinking`
*   **Purpose:** Offers a `sequentialthinking` tool designed for dynamic and reflective problem-solving. It helps in breaking down complex problems, planning solutions, and adapting strategies through a structured thought process.

### 3. `github.com/zcaceres/fetch-mcp`

*   **Installation Method:** `node /home/postgres/devel/python-kiwoom/fetch-mcp/dist/index.js`
*   **Purpose:** Provides tools to fetch content from URLs in various formats (HTML, Markdown, plain text, JSON). This is useful for retrieving and processing web content for analysis or integration.

### 4. `github`

*   **Installation Method:** `docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN -e GITHUB_TOOLSETS=repos,issues,pull_requests,actions,code_security,experiments ghcr.io/github/github-mcp-server`
*   **Purpose:** Enables comprehensive interaction with GitHub repositories. It provides tools for managing issues, pull requests, branches, commits, and workflows, allowing for automated Git operations and repository management.
