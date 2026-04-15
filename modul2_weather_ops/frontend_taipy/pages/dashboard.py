from taipy.gui import Markdown

# We assemble the markdown GUI for Taipy
# Using <|var|type|> syntax bindings to link to global variables in state_manager

dashboard_md = Markdown("""
<|container|
# Modul 2 Spatial Weather Platform
<span class="lead">System Beta - Taipy UI Engine</span><br/>
<|{status_text}|text|class_name=badge bg-primary mt-2 fs-6|>

<br/>
<br/>

<|layout|columns=1 1|
<|part|class_name=glass-panel text-center|
<span class="kpi-label">Highest Temp</span><br/>
<|{kpi_temp}|text|class_name=kpi-value mt-2|>
|>

<|part|class_name=glass-panel text-center|
<span class="kpi-label">Highest Wind Speed</span><br/>
<|{kpi_wind}|text|class_name=kpi-value mt-2|>
|>
|>

<|part|class_name=glass-panel p-2 mt-4|
<|chart|figure={fig}|height=65vh|width=100%|>
|>
|>
""")
