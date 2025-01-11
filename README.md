# AI Musician Agent

A specialized AI agent built using Coinbase's AgentKit, designed to assist musicians with their album release campaigns.

## Overview

This project implements an AI agent that helps musicians manage and execute their album release campaigns. The agent is built on top of Coinbase's AgentKit framework, leveraging blockchain technology for music distribution and campaign management.

## Features

- Campaign Planning and Management
- Album Release Strategy
- Web3 Integration for Music Distribution
- Fan Engagement Tools
- Smart Contract Management for Music Rights

## Prerequisites

- Python 3.11+
- [CDP API Key](https://portal.cdp.coinbase.com/access/api)
- [OpenAI API Key](https://platform.openai.com/docs/quickstart#create-and-export-an-api-key)

## Installation

1. Create and activate a virtual environment:
```bash
python3.11 -m venv venv_py311
source venv_py311/bin/activate
```

2. Install required packages:
```bash
pip install cdp-langchain
```

3. Set up environment variables:
```bash
export CDP_API_KEY_NAME="your_cdp_key_name"
export CDP_API_KEY_PRIVATE_KEY="your_cdp_private_key"
export OPENAI_API_KEY="your_openai_api_key"
```

## Usage

Run the agent:
```bash
python chatbot.py
```

Choose between:
1. Chat Mode - Interactive conversation with the agent
2. Auto Mode - Autonomous campaign management

## License

This project is licensed under the MIT License - see the LICENSE file for details. 