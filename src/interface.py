import gradio as gr
from .chatbot import ChatBot


def create_interface():
    chatbot = ChatBot()
    
    def chat_fn(message, history):
        if not message.strip():
            return history, ""
        
        try:
            response = chatbot.chat(message)
            history.append((message, response))
            return history, ""
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            history.append((message, error_msg))
            return history, ""

    with gr.Blocks(title="LangGraph PostgreSQL Chatbot") as interface:
        gr.Markdown("# LangGraph PostgreSQL Chatbot")
        gr.Markdown("Chat with an AI that remembers context using PostgreSQL persistence")
        
        chatbot_ui = gr.Chatbot(label="Conversation", height=400)
        msg = gr.Textbox(label="Message", placeholder="Type your message here...")
        
        msg.submit(chat_fn, [msg, chatbot_ui], [chatbot_ui, msg])
    
    return interface
