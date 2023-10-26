import requests
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import json

from dotenv import load_dotenv

load_dotenv()


# # Replace these with your Azure Storage account information
connection_string_blob = os.getenv("connection_string_blob")
container_name = os.getenv("container_name")

## Confluence Credentials 
api_url = os.getenv("api_url")

api_key_confluence = os.getenv("api_key_confluence")





# Define headers with the API key
headers = {
    'api-key': api_key_confluence,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# Define query parameters to expand the space, body, and version fields
params = {
    'expand': 'space,body.view,version,container',
}

## Function to Convert Html data into plain text
def converthtml2response(x):
        
        
    # Your HTML content
    html_content = x

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the text within the HTML document
    plain_text = soup.get_text()

    # Print or use the extracted plain text
    return plain_text


### Get the data from Cosmos db through rest API
# Define your Confluence API endpoint URL

# Request to get data

def get_data_from_confluence():
    response = requests.get(api_url, headers=headers, params=params)
    response
    confluence_data = response.json()

    if response.status_code == 200:
        try:
            documents = []
            for item in confluence_data.get('results', []):
            
                document = {

                        '@search.action': 'upload',  # Specify the action as 'upload' for indexing
                        
                        'page_id' : str(item.get('id', '')),

                        'space_key': str(item.get('space', {}).get('key', '')),
                        
                        'title': item.get('title', ''),
                        
                        'content': converthtml2response(item.get('body', {}).get('view',{}).get('value',{}))
                                                

                    }
                documents.append(document)
                
        except json.JSONDecodeError as e:
                print(f"JSON Decoding Error: {e}")
                
    else:
        print("There was a problem in getting request")
                
    return documents

    
    



def Uplod_data_to_blob(documents):
    
    try:
        # Create a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string_blob)

        # Create a ContainerClient to interact with the container
        container_client = blob_service_client.get_container_client(container_name)

        # Upload each item in the data_list to the container
        for item in documents:
            # To upload data as a docx FIle into the blob container
            file_name =  '{}.docx'.format(item['title'])
            content = item['content']
            
            # Create a BlobClient for the file
            blob_client = container_client.get_blob_client(file_name)
            
            # Upload the content to the blob
            blob_client.upload_blob(content, overwrite=True)
            
            print(f"Uploaded {file_name} to {container_name}")

        return "Uploaded {} files to the Blob".format(len(documents))
    except Exception as e:
        return e




data = get_data_from_confluence()

result = Uplod_data_to_blob(data)

print(result)









