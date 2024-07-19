

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import json


class Report:
    def __init__(self):

        # Create a simple line plot
        x = [1, 2, 3, 4, 5]
        y = [10, 15, 13, 17, 20]

        fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name='Line Plot'))
        plot_html = pio.to_html(fig, full_html=False)

        # HTML template with placeholders for text and plot
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>HTML Report with Plotly</title>
            <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
            <h1>My HTML Report</h1>
            <p>This is a sample report that includes text and a Plotly plot.</p>
            <p>Here is some LaTeX: \( E = mc^2 \)</p>
            <div id="plotly-div">{plot_html}</div>
        </body>
        </html>
        """

        # Save the final HTML report
        with open("report.html", "w") as file:
            file.write(html_template)

        print("Report saved as report.html")