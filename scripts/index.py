from superlinked.framework.common.schema.schema import schema
from superlinked.framework.common.schema.schema_object import (
    String, Float
)
from superlinked.framework.common.schema.id_schema_object import IdField

from superlinked.framework.dsl.space.number_space import NumberSpace, Mode
from superlinked.framework.dsl.index.index import Index
from superlinked.framework.dsl.space.categorical_similarity_space import (
    CategoricalSimilaritySpace,
)
import pandas as pd
import os
data_path = os.path.abspath('.')+'/data/'
pokedex_df = pd.read_csv(data_path+"pokedex.csv").drop(columns=["Unnamed: 0"])


@schema
class PokeSchema:
    name: IdField
    capture_chance: Float
    habitat: String
    color: String
    poke_type: String

pokemon = PokeSchema()



number_space = NumberSpace(pokemon.capture_chance, min_value=0.1, max_value=1, mode=Mode.SIMILAR)
color_space = CategoricalSimilaritySpace(
    category_input=pokemon.color, categories=pokedex_df['color'].unique()
)
habitat_space = CategoricalSimilaritySpace(
    category_input=pokemon.habitat, categories=pokedex_df['habitat'].unique()
)
type_space = CategoricalSimilaritySpace(
    category_input=pokemon.poke_type, categories=pokedex_df['poke_type'].unique()
)

index = Index(spaces=[
    number_space,
    color_space,
    habitat_space,
    type_space
])