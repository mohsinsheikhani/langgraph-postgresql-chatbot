# LangGraph PostgreSQL Chatbot

A conversational AI chatbot built with LangGraph that maintains context through intelligent conversation summarization and PostgreSQL database persistence.

## Features

- **Smart Memory Management**: Automatically summarizes long conversations while preserving recent messages
- **PostgreSQL Persistence**: Stores conversation state in PostgreSQL database for durability
- **LangGraph Integration**: Uses StateGraph for conversation flow control
- **Multiple LLM Support**: Compatible with Google Gemini and OpenAI models
- **Gradio Interface**: Simple web UI for chatbot interaction
- **External Database**: PostgreSQL-backed conversation state with PostgresSaver

## Setup

1. Clone the repository
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Set up PostgreSQL database
4. Create `.env` file:
   ```
   GOOGLE_API_KEY=
   LANGSMITH_PROJECT=
   LANGSMITH_TRACING=
   DB_URI=
   ```

## Usage

Run the application:

```bash
python main.py
```

This will:
- Initialize the chatbot with Google Gemini
- Connect to PostgreSQL database using singleton pattern
- Launch the Gradio interface at http://localhost:7860
- Start conversing with persistent memory management

## How It Works

The chatbot uses a two-node graph:

- **call_model**: Processes user input with conversation summary context
- **summarize_conversation**: Creates/updates conversation summary when message history grows

When conversations exceed a threshold a length of 6 messages, older messages are summarized while keeping the last 2 messages for short-term context. All conversation state is persisted in PostgreSQL for durability across sessions.
