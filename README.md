# PokeApi-with-Superlinked
## Description

This project is an example of how to use the Superlinked framework. It is designed for efficient multi-modal search across different data types, including text, images, and structured data. The framework is flexible, scalable, and optimized for use in real-world applications where search needs to be performed on diverse data modalities.
Given the user query, or the existing pokemon, system should return N relevant pokemons from the library.
There is a possibility to use this project for image search in database. The result of the project is ranged slice of original DB sorted by similarity score. 

This project aims to give better understanding of capabilities of Superlinked and Semantic Search in general.

- The whole data was scrapped from https://pokeapi.co/
- There were some missing data points in the collected dataset. The problem was solved with CatBoostClassifier.

## Features 
- Gradio for UI.
- Superlinked as gears for search.
- CLIP for image and texgt embeddings.

## Usage
- Find how to run basic queries in notebook folder. 
- Or simlply run app.py in scripts folder for Gradio UI.
- Also see data analisys in corresponding notebook. 
- Data retrival script is in scripts folder.

## TODO
- Compare Superlinked to alternatives
- 
- Use MongoDB for storring images and embeddings
