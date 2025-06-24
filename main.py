import os
from dotenv import load_dotenv
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.llms import ChatMessage

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

# Query the user response
user_response= "I have bleeding and it hurts a lot"

query_engine= index.as_query_engine()
#Convert the response into string (the response will be inserted into a prompt)
response= str(query_engine.query(user_response))
# print(response) SUCCESS

#Message
messages = [
    ChatMessage(role= "system", content="""You are a friendly and empathetic maternal health assistant trained on pregnancy
                 risk factors. When responding, use easy-to-understand, friendly, and empathetic language. The reponse should be 
                a risk insights or suggestions the patient should take."""),
    ChatMessage(role= "user", content=f"""The patient has reported the following: {user_response}. 
                Relevent knowledge base {response}.
                Based on the patient report and the knowledge base, respond with a risk assesment with suggestions the patient should 
                take. When responding with risk insights, categorise them as low, medium or high risk.
                Also provide an easy-to-understand explanation on why was this risk categorised as low, medium, or high. """)
]

#Specify the model
llm= Cohere("command-a-03-2025")

resp = llm.chat(messages)

print(resp)
