import os
import logging
import pandas as pd 


from superlinked.framework.dsl.executor.rest.rest_configuration import RestQuery

from superlinked.framework.dsl.executor.rest.rest_descriptor import RestDescriptor
from superlinked.framework.dsl.executor.rest.rest_executor import RestExecutor
from superlinked.framework.dsl.registry.superlinked_registry import SuperlinkedRegistry
from superlinked.framework.dsl.source.rest_source import RestSource
from superlinked.framework.dsl.source.data_loader_source import DataFormat, DataLoaderConfig, DataLoaderSource
from superlinked.framework.dsl.storage.mongo_db_vector_database import MongoDBVectorDatabase

from index import pokemon, index
from query import poke_query

class SuperlinkedClient:
    def __init__(self):
        self.source: RestSource = RestSource(pokemon)
        self.pokedex_db = MongoDBVectorDatabase(
            "benjaminquartiermeister:MTFlTzPWbNEEdiCJ@cluster0.bf8xk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            "Pokedex",
            "Cluster0",
            "66f33c95571be83d1b80c582",
            "cdjhkeej",
            "e507a5eb-3431-463e-81b6-9e6393847f18",
        )
        self.executor = RestExecutor(
            sources=[self.source],
            indices=[index],
            queries=[RestQuery(RestDescriptor("query"), poke_query)],
            vector_database=self.pokedex_db
        )        
        SuperlinkedRegistry.register(self.executor)