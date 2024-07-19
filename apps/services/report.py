

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import json
import subprocess

class Report:
    def __init__(self):
        # Create a simple line plot
        x = [1, 2, 3, 4, 5]
        y = [10, 15, 13, 17, 20]

        fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name='Line Plot'))
        plot_html = pio.to_html(fig, full_html=False)

        # Read the HTML template
        with open("template.html", "r") as file:
            html_template = file.read()

        # Execute the CLI command and capture its output
        cli_command = ["echo", "This is the output of my CLI command."]
        cli_output = subprocess.check_output(cli_command).decode("utf-8")

        # Replace the placeholders with the Plotly plot and CLI output
        html_report = html_template.replace("PLOT_PLACEHOLDER", plot_html)
        html_report = html_report.replace("CLI_OUTPUT_PLACEHOLDER", cli_output)

        # Save the final HTML report
        with open("report.html", "w") as file:
            file.write(html_report)

        print("Report saved as report.html")