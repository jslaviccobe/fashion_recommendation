# Fashion Recommendation Chatbot

## Introduction

This project implements a chatbot that provides fashion recommendations based on user the user input within the CLI, using Langchain and OpenAI under the hood. Based on the specific user request, the chatbot will return 3 items that best match their specific needs, providing the name of the product, its price, the image of the item, and a brief explanation for why it chose exactly that item. It will also refuse to talk anything non-fashion related.

## Setup

### Configuration

1. **OpenAI API Key**: You need an OpenAI API key to use this project. If you don't have one, you can obtain it by signing up at [OpenAI](https://openai.com/).

2. **Environment Variables**: Create a .env file in the project's root directory. This file should contain your OpenAI API key. You can use the provided .env.example as a template. Your .env file should look like this:

```
OPENAI_API_KEY=YOUR_API_KEY
```

### Installation

1. **Create a virtual environment:**

```
python3 -m venv .venv
```

2. **Activate the virtual environment:**

```
source .venv/bin/activate
```

3. **Install dependencies:**

```
pip3 install -r requirements.txt
```

## Running the Program

To run the program, navigate to the project's root directory in your terminal and execute:
```
python3 main.py
```
