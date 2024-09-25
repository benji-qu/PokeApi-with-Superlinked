from superlinked.framework.dsl.query.param import Param
from superlinked.framework.dsl.query.query import Query

from index import color_space, habitat_space, type_space, number_space, pokemon, index

poke_query = (
    Query(
    index,
    weights={
        color_space: Param("color_weight"),
        habitat_space: Param("habitat_weight"),
        type_space: Param("poke_type_weight"),
        number_space: Param("chance_weight"),
    },)
        .find(pokemon)
        .similar(color_space.category, Param("color"))
        .similar(habitat_space.category, Param("habitat"))
        .similar(type_space.category, Param("poke_type"))
        .similar(number_space.number, Param("chance")) 
        .limit(Param("limit"))
)