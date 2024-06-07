import json

from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_qa_with_sources_chain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

import gradio

load_dotenv()

db = Chroma(
    persist_directory="./chroma",
    embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"),
)

llm = ChatOpenAI(temperature=0, model="gpt-4")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

condense_question_prompt = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.\
Make sure to avoid using any unclear pronouns.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
condense_question_prompt = PromptTemplate.from_template(condense_question_prompt)
condense_question_chain = LLMChain(
    llm=llm,
    prompt=condense_question_prompt,
)

qa_chain = create_qa_with_sources_chain(llm)

doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain,
    document_variable_name="context",
    document_prompt=doc_prompt,
)

retrieval_qa = ConversationalRetrievalChain(
    question_generator=condense_question_chain,
    retriever=db.as_retriever(),
    memory=memory,
    combine_docs_chain=final_qa_chain,
)


def predict(message, history):
    response = retrieval_qa.run({"question": message})
    print(response)

    responseDict = json.loads(response)
    answer = responseDict["answer"]
    sources = responseDict["sources"]

    print(answer)
    print(sources)

    if type(sources) == list:
        sources = "\n".join(sources)

    if sources:
        return answer + "\n\nSee more:\n" + sources
    return answer


gradio.ChatInterface(predict).launch()

# python Scrape.py --site https://spring.io/projects/spring-framework --depth 10
# python Embed.py
# python main.py