from streamlit_agraph import Config

def Gui(directed: bool):
    return Config(width='100%',
                height=700,
                directed=directed,
                physics=False,
                )
