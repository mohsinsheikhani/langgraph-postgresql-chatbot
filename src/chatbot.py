from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from typing_extensions import Literal
from .database import DatabaseManager


class ChatBot:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        self.db_manager = DatabaseManager()
        self.graph = self._build_graph()

    def _build_graph(self):
        def call_model(state: MessagesState):
            response = self.llm.invoke(state["messages"])
            return {"messages": [response]}

        def summarize_conversation(state: MessagesState):
            summary = self.llm.invoke([
                SystemMessage("Create a concise summary of the conversation so far. Focus on key topics and user preferences."),
                *state["messages"]
            ])
            
            delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
            return {"messages": delete_messages + [summary]}

        def should_continue(state: MessagesState) -> Literal["summarize_conversation", "__end__"]:
            return "summarize_conversation" if len(state["messages"]) > 6 else "__end__"

        workflow = StateGraph(MessagesState)
        workflow.add_node("call_model", call_model)
        workflow.add_node("summarize_conversation", summarize_conversation)
        
        workflow.add_edge(START, "call_model")
        workflow.add_conditional_edges("call_model", should_continue)
        workflow.add_edge("summarize_conversation", END)

        return workflow.compile(checkpointer=self.db_manager.get_checkpointer())

    def chat(self, message: str, thread_id: str = "1"):
        config = {"configurable": {"thread_id": thread_id}}
        input_message = {"messages": [HumanMessage(content=message)]}
        
        result = self.graph.invoke(input_message, config)
        return result["messages"][-1].content
