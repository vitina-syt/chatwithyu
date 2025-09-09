import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.base_o365 import CHUNK_SIZE
from langchain_community.vectorstores import Chroma
from langchain_core import retrievers, vectorstores
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def load_pdf_split(pdf_path):
    """加载PDF文件并分割成文本块"""
    print(f"加载PDF文件: {pdf_path}")
    loader=PyPDFLoader(pdf_path)
    documents=loader.load()

    #1. split init
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    #2. split documents
    docs=text_splitter.split_documents(documents)
    print(f"已将文档分割成 {len(docs)} 个文本片段")
    return docs

def creatt_chroma_vectorstore(docs,model_name):
    """创建Chroma向量存储"""
    print("创建Chroma向量存储ing")

    #1. use ollama embeddingd
    embedding=OllamaEmbeddings(
        model=model_name,
        base_url="http://localhost:11434",
        )

    #2. new chroma vectorstore
    vectorstores=Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory="./pdf",
    )

    #3. create retriever
    retrievers=vectorstores.as_retriever(
        search_type="similarity",
        search_kwargs={"k":5}
    )
    return retrievers

def setup_ollama_llm(model_name="llama3"):
    """设置Ollama语言模型"""
    print(f"正在初始化 {model_name} 模型...")
    
    llm = Ollama(
        model=model_name,
        base_url="http://localhost:11434",
        temperature=0.1,     # 降低随机性，让答案更确定
        num_predict=512,     # 限制生成长度
    )
    
    return llm

def create_qa_chain(llm,retriever):
    """创建问答链"""
    template="""你是个专业的助手，熟练从文本提炼用户想知道的信息，并给出答案。
    请使用中文回答问题，如果遇到不会的，会直接说我无法回答你的问题，抱歉啦～
    以下是用户的问题：{question}
    以下是文本：{context}
    请给出答案：
    """

    prompt=ChatPromptTemplate.from_template(template)

    # 1. create rag chain
    rag_chain=(
        {"context":retriever , "question": RunnablePassthrough()
        | StrOutputParser()} 
        | prompt 
        | llm 
        | StrOutputParser()
    )

    return rag_chain

def main():
    PDF_PATH="./pdf/mechainLearn.pdf"
    EMBEDDING_MODEL="bge-m3"
    LLM_MODEL="llama3"

    #1. load pdf and split
    docs=load_pdf_split(PDF_PATH)

    #2. create chroma vectorstore
    retriever=creatt_chroma_vectorstore(docs,EMBEDDING_MODEL)
    
    try:

        docs=load_pdf_split(PDF_PATH)

        retriever=creatt_chroma_vectorstore(docs,EMBEDDING_MODEL)

        llm=setup_ollama_llm(LLM_MODEL)

        qa_chain=create_qa_chain(llm,retriever)

        while True:
            question=input("请输入问题: ")
            if question.lower() in ['quit', 'exit', '退出']:
                print("感谢使用，再见！")
                break
                
            if not question:
                continue
                
            print("正在思考...")
            try:
                answer = qa_chain.invoke(question)
                print(f"\n答案: {answer}\n")
                print("-" * 50)
            except Exception as e:
                print(f"出错: {e}")
    except Exception as e:
        print(f"程序初始化失败: {e}")
        print("请确保: 1. PDF文件路径正确 2. Ollama服务正在运行")
if __name__ == "__main__":
    main()