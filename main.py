from dotenv import load_dotenv
from src import create_interface

if __name__ == "__main__":
    load_dotenv()
    
    interface = create_interface()
    interface.launch(share=False, server_name="0.0.0.0", server_port=7860)
