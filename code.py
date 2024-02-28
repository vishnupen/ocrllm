from sentence_transformers import SentenceTransformer
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import openai
import numpy as np
import re
import pandas as pd
import os
# from dotenv import load_dotenv, find_dotenv
# load_dotenv()
 
openai_key="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"
api_key = openai_key
openai.api_key = api_key
 
# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = openai_key
openai.api_key = os.getenv("OPENAI_API_KEY")

# openai.api_key  = "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"

# csv_file_path=r"D:\aiAURA_DCAP\ocr-llm\csv_filtered_encode_df.csv"
csv_file_path = r"D:\aiAURA_DCAP\ocr-llm\csv_filtered_encode_df_insurance_payment.csv"
df=pd.read_csv(csv_file_path)
excel_file = os.path.basename(csv_file_path)
model = SentenceTransformer("all-MiniLM-L6-v2")
df_data=df['Para'].tolist()
# print(df_data[0])
text_embeddings = model.encode(df_data)

# Assuming doc_ids is a list of document IDs corresponding to text_embeddings
embeddings_dict = {'text': df_data, 'embeddings': text_embeddings.tolist()}
np.save('text_embeddings.npy', embeddings_dict)

loaded_embeddings = np.load('text_embeddings.npy', allow_pickle=True).item()
text = loaded_embeddings['text']
# print(text[0])
text_embeddings = np.array(loaded_embeddings['embeddings'])
# print(text_embeddings[0])
result = []
for para, embeddings in zip(text, text_embeddings):
    docs = Document(text=para, page_content=para, embeddings=embeddings)
    openai_model = OpenAI(temperature=0)
    chain = load_qa_chain(openai_model, chain_type="stuff")
    Condition = {
        "search_value":["Insurance", "payment"],
        "conditions":[">=", "<="],
        "expt_value":["1 Million", "30 Days"],
        "category":["Insurance", "Payment Terms"]
    }
    for i in range(len(Condition["search_value"])):
        search_value = Condition["search_value"][i]
        condition = Condition["conditions"][i]
        expt_value = Condition["expt_value"][i]
        category = Condition["category"][i]
        prompt = f"""Can you give me Numerical values where the {search_value} has a {condition} {expt_value} respectively?
        """
        print(prompt)
#     response = chain.run(input_documents=[Document(text=para, page_content=para, embeddings=embeddings)], question=prompt)
#     Ai_response = [value for value in response.split('\n') if value != '']
#     insurance_values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?!\d)\b', response)
#     Numeric_values = [int(value.replace(',', '')) for value in insurance_values]
#     if Ai_response != 'NA' or Ai_response != "[' NA']":
#         res = {
#             "Paragraph": para,
#             "Ai_response": Ai_response,
#             "Value": Numeric_values
#         }
#         # print(docs)
#         result.append(res)
# # print(result)
# filtered_data = [item for item in result if item['Value']]
# print(filtered_data)
# print(len(text_embeddings))
# print(len(text))

# docs = [Document(text=para, page_content=para, embeddings=embeddings) for para, embeddings in zip(text, text_embeddings)]

# Initialize OpenAI model
# openai_model = OpenAI(temperature=0)
# chain = load_qa_chain(openai_model, chain_type="stuff")
# Condition = {
#         'Category': 'Insurance',
#         'Search Value': 'Insurance',
#         'Expected Value': '1 Million',
#         'Condition': '>='
#     }

# prompt = f"""Can you give me Numerical values where the {Condition['Search Value']} has a {Condition['Condition']} {Condition['Expected Value']}?"""

# for i in docs:
#     print(i)

# response = chain.run(input_documents=docs, question=prompt)
# Ai_response = [value for value in response.split('\n') if value != '']
# print(Ai_response)

# insurance_values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?!\d)\b', response)
# print("Insurance values in documents are",insurance_values)

# Numeric_values = [int(value.replace(',', '')) for value in insurance_values]
# Sum=sum(Numeric_values)
# print("Sum of all insurance values are",Sum)