# from decouple import config
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain_openai import ChatOpenAI
# from langchain_core.prompts.prompt
from langchain_core.prompts.prompt import PromptTemplate
# from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
# from pydantic import BaseModel
import os

app = FastAPI()

# define model

openai_api_key = os.environ.get("OPENAI_API_KEY")

model = ChatOpenAI(
    openai_api_key=openai_api_key, #config("OPENAI_API_KEY"),
    model='gpt-4o-mini',
    temperature=0.4)

# Define a prompt
template = """
What is the meaning of {input}?
Answer as if you are a {profession}.
Give short answer in {language}.
Firstly dublicate question and than answer as follows:

Q: only human question
A: AI assistant answer
"""

prompt = PromptTemplate(
    template=template,
    input_variables=['input', 'profession', 'language']
)

chain = prompt | model

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, chain, path='/ask_openai')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
