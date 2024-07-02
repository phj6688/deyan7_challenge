from typing_extensions import override
from openai import OpenAI
import pickle
from dotenv import load_dotenv

load_dotenv()

QUESTION = input("Enter your question: ")
client = OpenAI()

# Load the vector store ID and file paths from the pickle file
with open('vector_store.pkl', 'rb') as f:
    data = pickle.load(f)
vector_store_id = data['vector_store_id']

assistant = client.beta.assistants.create(
    name="Product Documentation Assistant",
    instructions="""You are a knowledgeable product support assistant for specific lighting products. 
    Use the provided documents to answer user queries about product specifications, usage guidelines, 
    and other relevant details ONLY for the products mentioned in these documents.
    Make sure you answet in the language of the provided query. 
    If a question is about any topic or product not covered in the provided documents, 
    including other companies products, respond with "I don't have information about that." 
    I can only provide details about the specific lighting products in my documentation.'""",
    model="gpt-4o",    
    tools=[{"type": "file_search"}],
)

# Update the assistant to use the new vector store
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
)

# Create a thread and attach the question
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": f"{QUESTION}",
        }
    ]
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
message_content = messages[0].content[0].text
annotations = message_content.annotations
citations = []
for index, annotation in enumerate(annotations):
    message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
    if file_citation := getattr(annotation, "file_citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}] {cited_file.filename}")

if "I don't have information about that" in message_content.value:
    print("Assistant: I don't have information about that. I can only provide details about the specific lighting products in my documentation.")
else:
    print(f"Assistant: \n{message_content.value}")
    print("\nSource:\n","\n".join(citations),"\n")