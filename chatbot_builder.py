from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain


class ChatbotBuilder:
    def __init__(self):
        self.memory = None
        self.chatbot_chain = None

    def with_memory(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        return self

    def build(self, file_path):
        template = """You are a chatbot that provides fashion recommendations based on what the user 
        has requested and the context you were given. You should only talk about fashion-related 
        topics and refuse to talk about anything else. Provide up to 3 clothing recommendations per
        query, including the product name, price (in €), and image link, along with a brief 
        explanation why you"ve recommended exactly that item for each recommendation.\n
        Context: {context}\n\n"""
        template_input_variables = ["question", "context"]

        if self.memory != None:
            template += "Chat history: {chat_history}\n\n"
            template_input_variables.append("chat_history")

        template += "User input: {question}"

        loader = CSVLoader(file_path=file_path)
        documents = loader.load()
        vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings())

        prompt_template = PromptTemplate(
            input_variables=template_input_variables, template=template
        )

        self.chatbot_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(),
            retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": prompt_template},
        )

        return self.chatbot_chain
