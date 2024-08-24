import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#private imports
from github_api_calls import clean_and_load_issues
from notes import note_tool

# load env variables
load_dotenv()

def connect_to_vector_db():
    """
    Creates embeddings ie., convert documents to vectors
    and connect to astra db and saves the embedded documents.
    """
    embeddings = OpenAIEmbeddings()
    ASTRA_DB_API_ENDPOINT = os.getenv('ASTRA_DB_API_ENDPOINT')
    ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
    DESIRED_NAMESPACE = os.getenv('ASTRA_DB_KEYSPACE')
    
    if DESIRED_NAMESPACE:
        ASTRA_DB_KEYSPACE = DESIRED_NAMESPACE
    else:
        ASTRA_DB_KEYSPACE = None
    
    vstore = AstraDBVectorStore(
        collection_name="github_issues",
        embedding=embeddings,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE   
    )
    return vstore

def update_vector_db():
    """ 
    # prompt user for input if the issues need to be updated

    Args:
        vstore (_type_): _description_
        owner (_type_): _description_
        repo (_type_): _description_
    """

    vstore = connect_to_vector_db()
    update_vstore = input("Do you want to update the issues? (y/N): ").lower() in [
        "yes",
        "y",
    ]
    
    if update_vstore:
    
        owner="techwithtim"
        repo="Flask-Web-App-Tutorial"
        vstore = connect_to_vector_db()
        issue_docs = clean_and_load_issues(owner, repo)
        
        try:
            vstore.delete_collection("github_issues")  # delete existing collection if it exists)  # delete existing collection if it exists
        except:
            pass
        
        vstore.add_documents(issue_docs)
        logging.info("Updated Issue Embeddings in Vector DB")
        
def fetch_docs_f_vstore(vstore, query):      
        #retreving docs from Vector DB for testing
        vstore = connect_to_vector_db()
        results = vstore.similarity_search("Flash messages", k=3)
        
        for res in results:
            print(f"{res.page_content}")


def agent_rag():
    # creating an agent that can use the vector db and retriever tool
    vstore = connect_to_vector_db()
    retriever = vstore.as_retriever(search_kwargs={"k": 3})
    retriever_tool = create_retriever_tool(retriever,
                                        "github_issue_search",
                                        "Search for information about github issued."\
                                        "For any related to github issues you must use this tool.")

    prompt = hub.pull("hwchase17/openai-functions-agent")
    # create an llm that can use these tools
    llm = ChatOpenAI()

    tools = [retriever_tool, note_tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # use the agent executor in a loop to ask questions
    while (question := input("Ask a question about github issues (q to quit): "))!= "q":
        result = agent_executor.invoke({"input":question})
        print(result["output"])
        

def update_issues_ask_agent():
    # prompt user for input if the issues need to be updated
    update_vector_db()
    # start the agent
    agent_rag()
    

if __name__ == "__main__":
     update_issues_ask_agent()
    
    
