import openai, os, requests
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"

# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version

openai.api_version = "2023-08-01-preview"

# Azure OpenAI setup

openai.api_base = "https://azureservices.openai.azure.com/" # Add your endpoint here

openai.api_key = os.getenv("OPENAI_API_KEY") # Add your OpenAI API key here

deployment_id = "gpt-35-turbo-16k" # Add your deployment ID here

# Azure Cognitive Search setup
search_endpoint = "https://cgsearch-document.search.windows.net"; # Add your Azure Cognitive Search endpoint here

search_key = os.getenv("SEARCH_KEY") # Add your Azure Cognitive Search admin key here

search_index_name = os.getenv("search_index_name") # Add your Azure Cognitive Search index name here


def setup_byod(deployment_id: str) -> None:

    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
    :param deployment_id: The deployment ID for the model to use with your own data.
    To remove this configuration, simply set openai.requestssession to None.
    """
    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):
        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)
    session = requests.Session()
    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )
    openai.requestssession = session

setup_byod(deployment_id)

system_message=[{'role': 'system', 'content': 'You are an AI assistant that helps people find information '}]

def ChatCompletion(usermessage):
    system_message.append({'role': 'user', 'content': f"{usermessage}"})

    completion = openai.ChatCompletion.create(
        messages= system_message,
        deployment_id=deployment_id,
        
        dataSources=[  # camelCase is intentional, as this is the format the API expects
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": search_endpoint,
                    "key": search_key,
                    "indexName": search_index_name,
                    "queryType": "vectorSimpleHybrid",
                    "roleInformation":"You are an AI assistant that helps people find information in the documents and give data in detail,",
                    "embeddingEndpoint":"https://azureservices.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-03-15-preview",
                    "embeddingKey":"f0561845028c4508a40b515e5316d0d2",
                    "strictness":3,
                    "topNDocuments":5,
                    
                }
            }
        ]    
    )

    print(completion)
    system_message.append({'role': 'assistant', 'content': completion.choices[0].message["content"]})
    return completion.choices[0].message["content"]






            
