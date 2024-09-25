from superlinked.framework.common.schema.schema import schema
from superlinked.framework.common.schema.schema_object import (
    String, Float
)
from superlinked.framework.common.schema.id_schema_object import IdField

from superlinked.framework.dsl.space.number_space import NumberSpace, Mode
from superlinked.framework.dsl.source.in_memory_source import InMemorySource
from superlinked.framework.common.parser.dataframe_parser import DataFrameParser
from superlinked.framework.dsl.index.index import Index
from superlinked.framework.dsl.query.param import Param
from superlinked.framework.dsl.query.query import Query
from superlinked.framework.dsl.executor.in_memory.in_memory_executor import (
    InMemoryExecutor,
)
from superlinked.framework.dsl.space.categorical_similarity_space import (
    CategoricalSimilaritySpace,
)
import os
import logging
import pandas as pd 
import os
data_path = os.path.abspath('.')+'/data/'

class SuperlinkedClient:
    def __init__(self):
        self.pokemon = self.create_schema()
        self.df_parser = DataFrameParser(schema=self.pokemon)

        self.source = InMemorySource(
            schema=self.pokemon,
            parser=self.df_parser
        )
        self.number_space = NumberSpace(self.pokemon.capture_chance, min_value=0.1, max_value=1, mode=Mode.SIMILAR)
        self.color_space = CategoricalSimilaritySpace(
            category_input=self.pokemon.color, categories=self.return_categories()['colors']
        )
        self.habitat_space = CategoricalSimilaritySpace(
            category_input=self.pokemon.habitat, categories=self.return_categories()['habitats']
        )
        self.type_space = CategoricalSimilaritySpace(
            category_input=self.pokemon.poke_type, categories=self.return_categories()['poke_types']
        )

        self.index = Index(spaces=[
            self.number_space,
            self.color_space,
            self.habitat_space,
            self.type_space
        ])

        self.executor = InMemoryExecutor(sources=[self.source], indices=[self.index])
        self.app = self.executor.run()

        self.source.put([self.get_data()])

    def create_schema(self):
        @schema
        class PokeSchema:
            name: IdField
            capture_chance: Float
            habitat: String
            color: String
            poke_type: String
        return PokeSchema()
    
    def get_data(self):
        pokedex_df = pd.read_csv(data_path+"pokedex_updated.csv").drop(columns=["Unnamed: 0"])
        pokedex_df['ability_1'].fillna('None', inplace=True)
        pokedex_df['ability_2'].fillna('None', inplace=True)
        return pokedex_df
    
    def return_categories(self):
        data = self.get_data()
        colors = data["color"].unique()
        habitats = data["habitat"].unique()
        poke_types = data["poke_type"].unique()
        categories = {"colors": colors.tolist(), "habitats": habitats.tolist(), "poke_types": poke_types.tolist()}
        return categories
    
    def search(self, color, color_weight, habitat, habitat_weight, poke_type, poke_type_weight, chance,  chance_weight):
        logging.basicConfig(level=logging.INFO)
        logging.info("Searching for: " + "color: " + color + ", color_weight: " + str(color_weight) + ", habitat: " + habitat + ", habitat_weight: " + 
                str(habitat_weight) + ", poke_type: " + poke_type + ", poke_type_weight: " + str(poke_type_weight))
        query = (
            Query(
                self.index,
                weights={
                    self.color_space: Param("color_weight"),
                    self.habitat_space: Param("habitat_weight"),
                    self.type_space: Param("poke_type_weight"),
                    self.number_space: Param("chance_weight"),
            },
        )
        .find(self.pokemon)
        .similar(self.color_space.category, Param("color"))
        .similar(self.habitat_space.category, Param("habitat"))
        .similar(self.type_space.category, Param("poke_type"))
        .similar(self.number_space.number, Param("chance")) 
        .limit(Param("limit"))
        )
        query_params = {
            "color_weight": float(color_weight),
            "habitat_weight": float(habitat_weight),
            "poke_type_weight": float(poke_type_weight),
            "chance_weight": float(chance_weight),

            "color":color,
            "habitat": habitat,
            "poke_type": poke_type,
            "chance": chance,
        }
        result = self.app.query(query, limit=5, **query_params)
        return result.to_pandas()[['name', 'color','poke_type','habitat','similarity_score']]