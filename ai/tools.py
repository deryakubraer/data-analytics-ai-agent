from ai.schema import get_connection_string
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
# add plotly for advanced charts if needed
import plotly.express as px
import matplotlib.pyplot as plt



# Define the tools
TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_data_df",
            "description": "Get data from the database and return a pandas dataframe",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string"}
                },
                "required": ["sql_query"]
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "display_chart",
            "description": """Display a plotly chart. Supported chart types are line, bar, scatter, and pie. 
            Always provide a concise technical explanation of the chart generated.
            State which columns should be used for X and Y axes, and color.
            Color can be an empty string if not applicable.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string"},
                    "chart_type": {"type": "string"},
                    "explanation": {"type": "string"},
                    "x": {"type": "string"},
                    "y": {"type": "string"},
                    "color": {"type": "string"}
                },
                "required": ["sql_query", "chart_type", "explanation", "x", "y", "color"]
            },
        },
    }
]



# Define the get_data_df tool python function

def get_data_df(sql_query):
    # Create SQL engine
    connection_string = get_connection_string()
    if not connection_string:
        print("No connection string found in session state.")
        return "❌ No database connection string found. Please enter it in the app."
    engine = create_engine(connection_string)
    # Execute query and create dataframe
    with engine.connect() as connection:    
        sql_query = text(sql_query)
        result = connection.execute(sql_query)
        df = pd.DataFrame(result.all())
        # # Show the SQL query
        # expander = st.expander("SQL Query")
        # expander.write(sql_query)
        # Show the dataframe
        # st.dataframe(df)
        return {'role': 'assistant', 'content': {'type': 'dataframe', 'dataframe': df, 'sql_query': sql_query}}
    



#  Define a graphic tool for displaying dataframes in Streamlit

def display_chart(sql_query: str, chart_type: str = "line", explanation: str = "", x_col: str = None, y_col: str = None, color_col: str = None) -> dict:
    try:
        connection_string = get_connection_string()
        if not connection_string:
            return {
                'role': 'assistant',
                'content': {'type': 'text', 'text': "❌ No database connection string found. Please enter it in the app."}
            }

        engine = create_engine(connection_string)
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        print("DataFrame for chart:")
        print(df.head())
        print("Chart type:", chart_type)
        print("Explanation:", explanation)
        print("SQL Query:", sql_query)
        print("X column:", x_col)
        print("Y column:", y_col)
        print("Color column:", color_col)

        if df.empty:
            return {
                'role': 'assistant',
                'content': {'type': 'text', 'text': "⚠️ Query returned no results."}
            }


        # ----------------------
        # 1. Select X column (always first)
        # ----------------------
        if x_col == '' or x_col is None: 
            x_col = df.columns[0]

        # Convert to string if not numeric/datetime
        if not pd.api.types.is_numeric_dtype(df[x_col]) and not pd.api.types.is_datetime64_any_dtype(df[x_col]):
            df[x_col] = df[x_col].astype(str)


        # ----------------------
        # 2. Select Y column
        #    Prefer first numeric column after X
        # ----------------------
        if not y_col or y_col == '':
            
            for col in df.columns[1:]:
                if pd.api.types.is_numeric_dtype(df[col]):
                    y_col = col
                    break
            # If no numeric column found, use column 1
            if y_col is None:
                y_col = df.columns[1]

        # ----------------------
        # 3. Select color column (only if exists)
        # ----------------------
        if color_col == '' or color_col is None:
            if len(df.columns) > 2:
                color_col = df.columns[2]
            else:
                color_col = None  
 

        if chart_type == "line":
            fig = px.line(df, x=x_col, y=y_col, color=color_col)
        elif chart_type == "bar":
            fig = px.bar(df, x=x_col, y=y_col, color=color_col, barmode="group")
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
        elif chart_type == "pie":
            fig = px.pie(df, names=color_col, values=y_col)
        else:
            return {
                'role': 'assistant',
                'content': {'type': 'text', 'text': f"❌ Chart type '{chart_type}' is not supported."}
            }

        fig.update_xaxes(type='category')
        fig.update_layout(template="simple_white", height=500)

        return {
            'role': 'assistant',
            'content': {
                'type': 'chart',
                'chart': fig,
                'sql_query': sql_query,
                'explanation': explanation
            }
        }

    except Exception as e:
        print("Error creating chart:", e)
        return {
            'role': 'assistant',
            'content': {'type': 'text', 'text': f"❌ Error creating chart: {e}"}
        }
