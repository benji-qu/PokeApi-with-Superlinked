from superlinked.framework.common.schema.schema import schema
from superlinked.framework.common.schema.schema_object import (
    String, Float
)
from superlinked.framework.common.schema.id_schema_object import IdField

from superlinked.framework.dsl.space.text_similarity_space import TextSimilaritySpace
from superlinked.framework.dsl.space.number_space import NumberSpace, Mode
from superlinked.framework.dsl.source.in_memory_source import InMemorySource
from superlinked.framework.common.parser.dataframe_parser import DataFrameParser
from superlinked.framework.dsl.index.index import Index
from superlinked.framework.dsl.query.param import Param
from superlinked.framework.dsl.query.query import Query
from superlinked.framework.dsl.executor.in_memory.in_memory_executor import (
    InMemoryExecutor,
    InMemoryApp,
)
import os
import pandas as pd 


class SuperlinkedClient:
    def __init__(self):
        self.pokemon = self.create_schema()
        self.df_parser = DataFrameParser(schema=self.pokemon)

        self.source = InMemorySource(
            schema=self.pokemon,
            parser=self.df_parser
        )

        self.number_space = NumberSpace(self.pokemon.capture_chance, min_value=0.1, max_value=1, mode=Mode.SIMILAR)
        self.desc_space = TextSimilaritySpace(self.pokemon.description, model="sentence-transformers/all-mpnet-base-v2")

        self.index = Index(spaces=[
            self.number_space,
            self.desc_space
        ])

        self.executor = InMemoryExecutor(sources=[self.source], indices=[self.index])
        self.app = self.executor.run()

        self.source.put([self.get_data()])

    def create_schema(self):
        @schema
        class PokeSchema:
            name: IdField
            capture_chance: Float
            description: String
        return PokeSchema()
    
    def get_data(self):
        data_path = '/Users/benjibred/Projects/Python/PokeApi-with-Superlinked/data/pokedex_updated.csv'
        pokedex_df = pd.read_csv(data_path).drop(columns=["Unnamed: 0"])
        pokedex_df['ability_1'].fillna('None', inplace=True)
        pokedex_df['ability_2'].fillna('None', inplace=True)
        return pokedex_df


    def search(self, query_text, number):
        query = (
            Query(
                self.index,
                weights={
                    self.desc_space: Param("desc_weight"),
                    self.number_space: Param("chance_weight"),
            },
        )
        .find(self.pokemon)
        .similar(self.desc_space.text, Param("desc")) 
        .similar(self.number_space.number, Param("chance")) 
        .limit(Param("limit"))
        )
        query_params = {
            "desc_weight": 1,
            "chance_weight": 1,
            "desc": query_text,
            "chance": float(number),
        }
        result = self.app.query(query, limit=5, **query_params)
        return result.to_pandas()[['name', 'capture_chance', 'description', 'similarity_score']]