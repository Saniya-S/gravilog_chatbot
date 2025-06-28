import os
from dotenv import load_dotenv
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.llms import ChatMessage

#Import the schema
from schema import RiskLevelOutput

load_dotenv()

cohere_api_key=os.getenv("COHERE_API_KEY")

#Changing the default embed model to Cohere's embed model
Settings.embed_model = CohereEmbedding(
    model= "embed-v4.0",
    api_key= cohere_api_key
)
#Change the default llm model
Settings.llm = Cohere(model= "command-a-03-2025", temperature=0.3, api_key= cohere_api_key)

# Ingestting data into documents
documents = SimpleDirectoryReader("./data").load_data()

# print(len(documents)) SUCCESS

storage_dir= "storage"
if os.path.exists(storage_dir):
    # Load the stored indexed
    print("Dir Exist")
    storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
    index= load_index_from_storage(storage_context)
else:
    print("Dir does not exist")
    os.makedirs(storage_dir, exist_ok=True)
    #Chunking and Indexing
    index= VectorStoreIndex.from_documents(documents, transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=20)])
    index.storage_context.persist(persist_dir=storage_dir)




# user_input: the query by the user (string)
# use_structure: True if you want the LLM to provide the response in pydantic structure, False if not
# context: provide additonal information to the llm to generate its answer
def get_structured_response(user_input, use_structure= False, context= ""):
    
    # Get the relevant information from the knowledge base
    query_engine= index.as_query_engine()
    #Convert the response into string (the response will be inserted into a prompt)
    response= str(query_engine.query(user_input))

    # The persona of the chatbot
    system_message= ChatMessage(role= "system", content="""You are a friendly and empathetic maternal health assistant trained on pregnancy
                 risk factors. When responding, use easy-to-understand, friendly, and empathetic language. The reponse should be 
                a risk insights or suggestions the patient should take.""")
    
    # Risk analysis prompt
    # Here, user_input are the questions and their answers by the user
    risk_analysis_message= ChatMessage(role= "assistant", content=f"""The patient has reported the following: {user_input}. 
                Relevent knowledge base {response}.
                Based on the patient report and the knowledge base, respond with a risk assesment with suggestions the patient should 
                take. When responding with risk insights, categorise them as low, medium or high risk.
                Also provide an easy-to-understand explanation on why was this risk categorised as low, medium, or high. """)
    
    # Follow-up prompt
    follow_up_user= ChatMessage(role= "assistant", content=f"""
        This is the patients risk analysis report: {context}.
        Upon reading this, the patient has asked the question: {user_input}.
        As a friendly and empathetic maternal health assistant, provide them answer to their query with easy-to-understand, friendly language,
        Ensure that you use, natural conversational tone when responding.""")

    #Specify the model
    llm= Cohere("command-r-plus-08-2024")

    #Provide the pydantic class to the llm
    sllm=  llm.as_structured_llm(RiskLevelOutput)

    if use_structure:
        resp = sllm.chat([system_message, risk_analysis_message])
        print(type(resp.raw)) # Check if it is pydantic object, you have defined in your schema
        print(resp.raw) # Access the data

        # Convert into dict using .model_dump function from pydantic
        resp_dict= resp.raw.model_dump()
        # print(resp_dict)

        return resp_dict
    else:
        resp= llm.chat([system_message, follow_up_user])
        # Access the data
        resp_str= resp.raw["text"]
        return resp_str







