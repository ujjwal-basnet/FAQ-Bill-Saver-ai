from pydantic import BaseModel 
from typing import List 
import json 
from config import settings
from chromadb import Client
import logging 
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
from helper import normalize_query as n 
from chromadb_handeler import ChromaDBHandler
import hashlib 
from ask_ai import ask 


try : 
    from config import APPConfig, settings

except : 
    print("coud't not import settigns config.py so using dummy settings")

    class APPConfig:
        CHROMA_PERSIST_DIR = "./chroma_db_dummy"
        COLLECTION_NAME = "semantic_cache_dummy"
        EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"


    settings= APPConfig()


class AiOutput(BaseModel):
    """ FAQ Bot  """

class Semantic_Cache:
    def __init__(self, config: APPConfig):

        self.config= config 
        ## initilized ChromaDBHandler 
        try : 
            self.db_handler= ChromaDBHandler(
                persist_dir=self.config.CHROMA_PERSIST_DIR , 
                collection_name=self.config.COLLECTION_NAME , 
                model_name=self.config.EMBEDDING_MODEL_NAME
            )

            self.cliet= self.db_handler.client 
            self.index= self.db_handler.collection 

        except Exception as e :
            raise "chromaDBhander not initilized"
        
        ## initilized sentence transformer
        self.model= SentenceTransformer(self.config.EMBEDDING_MODEL_NAME)

    def _get_id(self, query):
        normalized_query= n(query) 
        return hashlib.sha256(normalized_query.encode('utf-8')).hexdigest()
    
    def add_entry(self, entry_id:str , response_text:str , embeddings: List[float]):

        try : 
            """ we add cache i.e query embeddings , and response with query id(hash) in this 
            using UPSERT which is (update if already exist) else insert  """

            self.index.upsert(
                ids=[self.entry_id],
                embeddings=[embeddings],
                metadatas=[{'response':response_text}])
            
            print("update sucessfull")

        except Exception  as e : 
            raise "error on add_entry"
        
    def reset_cache(self):
        self.db_handler.reset_collection()

    def _get_by_id(self,entry_id):
        try :
            ## direct search 
            direct_search= self.index.get(ids=[entry_id], include=['metadatas'])
            if direct_search:
                print("Cache fould though direct  lookup")
                return direct_search 
        
        except Exception as e : 
            print("error on get_by_id")
            return None 
                
    
    def _search_by_embedding(self, query:str, query_embedding:List[float],  threshold:float = 0.92):
        self.query_embedding= self.model.encode(query).tolist()

        ## search the index 
        results= self.index.query(query_embeddings=[query_embedding], n_results=1 , 
                                 include=['metadatas', 'distances'])
        
        ## check distance against the threeshold 
        if (results and 
            results['distances']and 
            results['distances'][0] and 
            results['distances'][0][0] <= (1- threshold)): ## lower the distance more the similiraty

                    response= results['metadata'[0][0]]['response']
                    distance= results['distance'][0][0]

                    print(f"Semantic Cachhe Hit")
                    return response 
        
        return None 
    

    def cache_check(self, query:str):

        """ Perform two step cache look up
          1) exact ID match 
          2) semantic similarity search 
          if answer is not found on both then , ask to ai and store embeddings and answers for next time"""
        
        self.entry_id= self._get_id(query= query)
        exact_match= self._get_by_id(self.entry_id) ## exact match 
        if exact_match:
            return exact_match 
        
        embedded_query=self.model.encode(query).tolist()

        semantic_response= self._search_by_embedding(query , query_embedding= embedded_query ,  threshold= 0.92)
        if semantic_response: 
            return semantic_response
        
        ## Cache miss , ask llm 
        response= ask(query=query)
        

        ### save to entry point
        self.add_entry(entry_id= self.entry_id , response_text=response , embeddings=embedded_query )
        return response
        
