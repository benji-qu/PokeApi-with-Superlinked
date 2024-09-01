import gradio as gr
import pandas as pd

def search(query: str):
    res: pd.DataFrame = get_data()
    print(query)
    return res

def get_data():
    df = pd.read_csv('data/pokedex.csv')
    return df.drop(columns=['Unnamed: 0'])

demo = gr.Interface(
    search,
    inputs=gr.Textbox(label="Query"),
    outputs=[
        gr.Dataframe(
            headers=list(get_data().columns),
            row_count=5,
            col_count=(len(list(get_data().columns)), "fixed"),

        ),
    ],
    description="Semantic search",
)

if __name__ == "__main__":
    demo.launch()
