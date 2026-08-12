import plotly.io as pio

def apply_theme():

    pio.templates["mocha"] = {
        "layout": {
            "paper_bgcolor": "#151515",
            "plot_bgcolor": "#151515",

            "font": {
                "family": "Inter",
                "color": "#F8F8F8",
                "size": 14
            },

            "title": {
                "font": {
                    "size": 22,
                    "color": "#FFFFFF"
                },
                "x": 0.02
            },

            "xaxis": {
                "gridcolor": "#2A2A2A",
                "zerolinecolor": "#2A2A2A",
                "linecolor": "#2A2A2A",
                "tickfont": {"color": "#BDBDBD"}
            },

            "yaxis": {
                "gridcolor": "#2A2A2A",
                "zerolinecolor": "#2A2A2A",
                "linecolor": "#2A2A2A",
                "tickfont": {"color": "#BDBDBD"}
            },

            "colorway": [
                "#D47E30",
                "#6F4E37",
                "#F39A46",
                "#A05A2C",
                "#8C6239",
                "#C68642"
            ]
        }
    }

    pio.templates.default = "mocha"