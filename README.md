# FAQ-Bill-Saver-ai

### Probelm : Most of Customer chatbot  questions are  repetative calling llm apis for each time on similar  question from different user is not ideal 
 if user1 ask : what is capital city of nepal 
 
 llm will save this response on  database,  store question on vector database   and then  show to user 1


now later if user 2, user 3 , ... any user ask

same related queestion like

[ capital nepal , capital city of nepal ? , what  capital city nepal ]

any thing which is higly similar  to question user 1 asked



then  ai will replay from its cache , insted of calling llm 

hence its saves money 


if question are not similar (cache miss condition) then it calls llm 

and then store answer again



its highly usefull on , projects like customer care chatbox 

since most of customer question are almost similar



tech
FAQ-Bill-Saver-ai is a small local prototype that caches AI responses (semantic + exact) for AWS SageMaker–related questions. It uses ChromaDB for persistent vector storage, SentenceTransformers for embeddings, and a Google Gemini based LLM connector for on-demand answers.
the above code useses cache insted of calling llm everytime

