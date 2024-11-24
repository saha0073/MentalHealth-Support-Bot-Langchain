from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_pinecone import PineconeVectorStore
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


class Tools:
    @staticmethod
    def setup_tools():
        tavily_tool = TavilySearchResults(max_results=5)
        tools = [tavily_tool]
        return tools
    
def GetRetriever(index_name):
    embeddings=OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


