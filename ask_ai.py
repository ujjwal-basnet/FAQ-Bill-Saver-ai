### if cache does help we will rag , to search on internet , mcp 

### but for now gona do only simple ai query 
from pydantic import BaseModel, Field
from langchain_core.exceptions import OutputParserException
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from langchain_core.prompts import ChatPromptTemplate

class AIResponse(BaseModel):
    """ search web  , Analysis and  Answer User query realated to Amazon_sagemaker_Faq  """ 
    response: str = Field(...  , 
                          description="donot response anyother thing asked other than , Aws and Aws SageMaker"
    ) 

def ask(query:str) -> str:
    try : 
        llm  = ChatGoogleGenerativeAI(
            model= settings.GEMINAI_DEFULT_MODEL_NAME,
            temperature= 0 ,
            api_key=settings.GEMINAI_API_KEY
        )
    except Exception as e :
        raise "error on chatgooglegenerativeai"

    structure_llm= llm.with_structured_output(AIResponse)

    system_prompt = """Your name is [Aws sage maker FAQ bot, your task is to help/ guide  user to  solve query  related to 
    ' amozone sagemaker' , do not greet or start with introduction ,your response should be to the point , no bluff , you are only here to hlep querry related to asws sage maker
    for example 

    {{user query}} : what is aws sagemaker ? 
    {{your response}} :AWS SageMaker is a cloud service for building, training, and deploying machine learning models at scale. """ # <--- FIX IS HERE

    prompt=  ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ('human' , "{query}"),
        ]
    )

    llm_chain= prompt | structure_llm  
    response= llm_chain.invoke({"query": query})
    return response


system_prompt = """Your name is [Aws sage maker FAQ bot, your task is to help/ guide  user to  solve query  related to 
' amozone sagemaker' , do not greet or start with introduction ,your response should be to the point , no bluff , you are only here to hlep querry related to asws sage maker
for example 

{{user query}} : what is aws sagemaker ? 
{{your response}} :AWS SageMaker is a cloud service for building, training, and deploying machine learning models at scale. """ # <--- FIX IS HERE

prompt=  ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ('human' , "{query}"),
    ]
)

if __name__ == "__main__":
    #test
    query = "how to login into aws sagemaker"
    print(ask(query=query))