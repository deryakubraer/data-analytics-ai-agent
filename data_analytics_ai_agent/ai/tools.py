from ai.schema import get_connection_string
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
# add plotly for advanced charts if needed
import plotly.express as px
import matplotlib.pyplot as plt



load_dotenv()

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
            "description": "Display a pandas charts in the Streamlit app",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string"},
                    "chart_type": {"type": "string"},
                    'explanation': {'type': 'string'}
                },
                "required": ["sql_query", "chart_type", 'explanation']
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

def display_chart(sql_query: str, chart_type: str = "line", explanation: str = "") -> str:
    print(f"Displaying {chart_type} chart with query:", sql_query)
    print( "Explanation:", explanation)
    try:
# Create SQL engine
        connection_string = get_connection_string()
        if not connection_string:
            print("No connection string found in session state.")
            return "❌ No database connection string found. Please enter it in the app."
        
        engine = create_engine(connection_string)
        
        # Execute query and create dataframe
        with engine.connect() as connection:    
            result = connection.execute(text(sql_query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
        # Show the SQL query
        # with st.expander("SQL Query"):
        #     st.code(sql_query, language="sql")

        if df.empty:
            st.warning("No data returned from the query.")
            return
            

         # --- Pick first column as X, second as Y ---
        x_col = df.columns[0]
        y_col = df.columns[1]

         # --- Force X to categorical if not numeric/datetime ---
        if not pd.api.types.is_numeric_dtype(df[x_col]) and not pd.api.types.is_datetime64_any_dtype(df[x_col]):
            df[x_col] = df[x_col].astype(str)
       
        # --- Plot line chart ---
        if chart_type == "line":
            fig = px.line(df, x=x_col, y=y_col)
        elif chart_type == "bar":
            fig = px.bar(df, x=x_col, y=y_col)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col)
        elif chart_type == "pie":
            fig = px.pie(df, names=x_col, values=y_col)
        else:
            return f"Chart type '{chart_type}' is not supported."
        
        # Force X-axis to show all category names
        fig.update_xaxes(type='category')
        fig.update_layout(template="plotly_white", height=500)
        # st.plotly_chart(fig, use_container_width=True)

        # return "Chart displayed successfully."
        return {'role': 'assistant', 'content': {'type': 'chart', 'chart': fig, 'sql_query': sql_query, 'explanation': explanation}}
    except Exception as e:
        st.error(f"Error creating line chart: {e}")
        return f"Error creating line chart: {e}"
    
    import plotly.graph_objects as go

# --- AXIS GRAPH COLOR PALETTE ---
# 1. Stardust Gold (Primary)
# 2. Hologram Cyan (Secondary Contrast)
# 3. Deep Orchid (Tertiary)
# 4. Ember Orange (Tertiary)



