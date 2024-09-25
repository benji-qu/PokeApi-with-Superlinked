import gradio as gr
import warnings
from superlinked_client import SuperlinkedClient
warnings.filterwarnings("ignore")



s = SuperlinkedClient()

demo = gr.Interface(
    s.search,
    inputs=[
        gr.Dropdown(s.return_categories()['colors'], label="Color"),
        gr.Number(value=1, label="Color weight"),

        gr.Dropdown(s.return_categories()['habitats'], label="Habitat"),
        gr.Number(value=1, label="Habitat weight"),

        gr.Dropdown(s.return_categories()['poke_types'], label="Type"),
        gr.Number(value=1, label="Type weight"),

        gr.Slider(minimum=0.1, maximum=1, step=0.01, value=0.5, label="Chance to catch"),
        gr.Number(value=1, label="Chance weight")
    ],
    outputs=[
        gr.Dataframe(
            headers=['name', 'color','poke_type','habitat','similarity score'],
            row_count=5,
            col_count=5,

        ),
    ],
    description="Poke search",
)



if __name__ == "__main__":
    demo.launch()
