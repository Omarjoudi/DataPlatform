import dash
from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import requests

# Define our FastAPI backend URL
API_URL = "http://127.0.0.1:8000/"

def fetch_data(endpoint):
    try:
        return requests.get(str(API_URL) + str(endpoint), timeout=5)
    except:
        return None
    
def create_data(endpoint, data):
    try:
        return requests.post(str(API_URL) + str(endpoint), json=data, timeout=5)
    except:
        return None

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# --- LAYOUT ---
app.layout = dbc.Container([
    html.Br(),
    html.H1("🚀 My Task Manager", className="text-center text-primary mb-4"),
    # Form to create a new task
    dbc.Card([
        dbc.CardHeader("Add a New Project"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Input(id="project-title", placeholder="Project Title", type="text"), width=2),
                dbc.Col(dbc.Input(id="project-desc", placeholder="Description (optional)", type="text"), width=3),
                dbc.Col(dcc.Dropdown(id="project-status", placeholder="Status", options=[{"label": "Is Active", "value": True}, {"label": "Is Inactive", "value": False}], value=None), width=3),
                dbc.Col(dbc.Button("Add Project", id="add-project-btn", color="success", n_clicks=0), width=2),
            ]),
            html.Div(id="form-alert", className="mt-2") # For showing success/error messages
        ])
    ], className="mb-4 shadow-sm"),
    
    # Form to create a new task
    dbc.Card([
        dbc.CardHeader("Add a New Task"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Input(id="task-title", placeholder="Task Title", type="text"), width=2),
                dbc.Col(dbc.Input(id="task-desc", placeholder="Description (optional)", type="text"), width=3),
                dbc.Col(dcc.Dropdown(id="task-status", placeholder="Status", options=[{"label": "Completed", "value": True}, {"label": "Pending", "value": False}], value=None), width=3),
                dbc.Col(dbc.Button("Add Task", id="add-btn", color="success", n_clicks=0), width=2),
            ]),
            html.Div(id="form-alert", className="mt-2") # For showing success/error messages
        ])
    ], className="mb-4 shadow-sm"),

    # Area to display tasks
    html.H3("Current Tasks"),
    dbc.Button("Refresh List", id="refresh-btn", color="secondary", size="sm", className="mb-3", n_clicks=0),
    html.Div(id="task-list", className="mb-5")

], fluid=False)

# --- CALLBACKS ---

@app.callback(
    [Output("task-list", "children"),
     Output("form-alert", "children"),
     Output("task-title", "value"),
     Output("task-desc", "value")],
    [Input("add-btn", "n_clicks"),
     Input("refresh-btn", "n_clicks")],
    [State("task-title", "value"),
     State("task-desc", "value")]
)
def update_tasks(add_clicks, refresh_clicks, title, desc):

    # Figure out which button triggered the callback
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "refresh-btn"

    alert_msg = ""
    new_title = title
    new_desc = desc

    # If the user clicked "Add Task"
    if trigger_id == "add-btn" and title:
        payload = {"title": title, "description": desc, "completed": False}
        try:
            res = create_data("tasks", payload)
            if res and res.status_code == 200:
                alert_msg = dbc.Alert("Task added successfully!", color="success", duration=3000)
                new_title = "" # Clear the form
                new_desc = ""  # Clear the form
            else:
                alert_msg = dbc.Alert(f"Error: {res.text}", color="danger")
        except Exception as e:
            alert_msg = dbc.Alert(f"Connection Error: Is the API running? ({e})", color="danger")

    # Fetch all tasks to display (happens on load, on refresh, and after adding)
    task_cards = []
    try:
        res = fetch_data("tasks")
        if res and res.status_code == 200:
            tasks = res.json()
            if not tasks:
                task_cards = [html.P("No tasks yet. Add one above!")]
            else:
                for t in tasks:
                    task_cards.append(
                        dbc.Card(
                            dbc.CardBody([
                                html.H5(t["title"], className="card-title"),
                                html.P(t["description"] or "No description", className="card-text text-muted"),
                            ]),
                            className="mb-2 shadow-sm border-start border-primary border-4"
                        )
                    )
        else:
            task_cards = [html.P("Failed to fetch tasks from API.")]
    except:
        task_cards = [html.P("Could not connect to the backend API. Make sure Uvicorn is running!")]

    return task_cards, alert_msg, new_title, new_desc



if __name__ == "__main__":
    # Run the Dash app on port 8050
    app.run(debug=True, port=8050)