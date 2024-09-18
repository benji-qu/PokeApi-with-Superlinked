import gradio as gr
import warnings
from superlinked_client import SuperlinkedClient
warnings.filterwarnings("ignore")



s = SuperlinkedClient()


demo = gr.Interface(
    s.search,
    inputs=[
        gr.Textbox(label="Description"),
        gr.Textbox(label="Chance to catch")
    ],
    outputs=[
        gr.Dataframe(
            headers=['name', 'chance_to_catch', 'description', 'similarity score'],
            row_count=5,
            col_count=4,

        ),
    ],
    description="Semantic search",
)



if __name__ == "__main__":
    demo.launch()
