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



def display_chart(sql_query: str, chart_type: str = "line", explanation: str = "") -> dict:
    print(f"Displaying {chart_type} chart with query: {sql_query}")
    try:
        # 1. Database Connection and Query Execution
        connection_string = get_connection_string()
        if not connection_string:
            return {'role': 'assistant', 'content': {'type': 'text', 'text': "❌ No database connection found in session state."}}
        
        engine = create_engine(connection_string)
        
        with engine.connect() as connection:    
            result = connection.execute(text(sql_query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
        if df.empty:
            return {'role': 'assistant', 'content': {'type': 'text', 'text': "⚠️ The query returned no data."}}

        # 2. ROBUST COLUMN MAPPING & RESHAPING LOGIC

        # Identify numerical and non-numerical columns
        numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        non_numeric_cols = [col for col in df.columns if not pd.api.types.is_numeric_dtype(df[col])]
        
        if len(numeric_cols) == 0:
             return {'role': 'assistant', 'content': {'type': 'text', 'text': "❌ Query returned no numerical data column to plot on the Y-axis."}}
        
        # Helper to check if a column looks like a date/time
        def is_date_like(series):
            try:
                # Use errors='coerce' here temporarily for date detection
                df_temp = pd.to_datetime(series, errors='coerce') 
                # Must be at least 50% valid dates to be considered a time axis
                return df_temp.notna().sum() > len(series) * 0.5 
            except Exception:
                return False
        
        x_col, y_col, color_col = None, None, None

        # Prioritize finding the X-axis (Time/Month)
        x_candidate_cols = [col for col in non_numeric_cols if is_date_like(df[col])]
        
        if len(x_candidate_cols) == 1:
            x_col = x_candidate_cols[0]
            
            # --- WIDE DATA SCENARIO (Multiple lines requested) ---
            # If we have a clear X-axis and multiple numerical columns, melt the data.
            if len(numeric_cols) > 1:
                print("Detected wide data (1 time column, >1 numeric columns). Melting for multi-series plot.")
                
                # Identify columns to keep as IDs (non-numeric, excluding the X-col we just found)
                id_vars = [col for col in df.columns if col not in numeric_cols]
                
                # Melt all numerical columns into 'Metric' (line name) and 'Value' (Y-axis)
                df_melted = pd.melt(df, id_vars=id_vars, var_name='Metric', value_name='Value')
                
                # Re-map axes for the melted dataframe
                y_col = 'Value'       # The new single value column
                color_col = 'Metric'  # The new column representing the old column names (the groups/lines)
                df = df_melted        # Use the melted dataframe for plotting
            
            # --- LONG DATA SCENARIO (One line or grouped plot) ---
            else:
                # 2.1 Y-AXIS PRIORITY: Find the best value column (e.g., 'payment' over 'id')
                y_col_priority = ['amount', 'payment', 'value', 'total', 'sum', 'count']
                found_y_col = None
                for name in y_col_priority:
                    candidates = [col for col in numeric_cols if name in col.lower()]
                    if candidates:
                        found_y_col = candidates[0]
                        break
                y_col = found_y_col if found_y_col else numeric_cols[0]

                # 2.2 COLOR/GROUP: Use the next available non-numeric column if available
                other_non_numeric = [col for col in non_numeric_cols if col != x_col]
                color_col = other_non_numeric[0] if other_non_numeric else None

        else:
            # Fallback for simple data (No clear time axis, just 2-3 columns)
            # Y-Axis takes the first numeric column
            y_col_priority = ['amount', 'payment', 'value', 'total', 'sum', 'count']
            found_y_col = None
            for name in y_col_priority:
                candidates = [col for col in numeric_cols if name in col.lower()]
                if candidates:
                    found_y_col = candidates[0]
                    break
            y_col = found_y_col if found_y_col else numeric_cols[0]
            
            # X-Axis takes the first non-numeric column
            x_col = non_numeric_cols[0] if non_numeric_cols else numeric_cols[1] if len(numeric_cols) > 1 else None
            
            # Color takes the second non-numeric column (if available)
            color_col = non_numeric_cols[1] if len(non_numeric_cols) >= 2 else None


        if not x_col or not y_col:
             return {'role': 'assistant', 'content': {'type': 'text', 'text': "❌ Could not map X and Y columns correctly for plotting."}}

        print(f"Final Mapped Axes: X='{x_col}', Y='{y_col}', Color='{color_col}'")


        # 3. Data Type Coercion 
        
        # Try to convert the determined X-column to datetime, inferring the format
        try:
            df[x_col] = pd.to_datetime(df[x_col], infer_datetime_format=True)
        except Exception:
            # If conversion fails, ensure the X-column is treated as a string category
            if not pd.api.types.is_numeric_dtype(df[x_col]):
                df[x_col] = df[x_col].astype(str)

        
        # 4. Plot Generation
        if chart_type == "line":
            fig = px.line(df, x=x_col, y=y_col, color=color_col, markers=True)
        
        elif chart_type == "bar":
            # Use 'group' barmode to show bars side-by-side for each month/category
            fig = px.bar(df, x=x_col, y=y_col, color=color_col, barmode='group')
        
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
        
        elif chart_type == "pie":
            # Pie charts only use 2 columns: Name and Value. Uses the X and Y columns determined above.
            fig = px.pie(df, names=x_col, values=y_col)
        
        else:
            return {'role': 'assistant', 'content': {'type': 'text', 'text': f"Chart type '{chart_type}' is not supported."}}
        
        # 5. Final Layout Polish
        fig.update_layout(template="plotly_white", height=450, margin=dict(l=20, r=20, t=40, b=20))
        
        # If the X-axis is not a date type, force it to be categorical to show all labels
        if not pd.api.types.is_datetime64_any_dtype(df[x_col]):
            fig.update_xaxes(type='category')

        # Return structured response
        return {
            'role': 'assistant', 
            'content': {
                'type': 'chart', 
                'chart': fig, 
                'sql_query': sql_query, 
                'explanation': explanation,
                'dataframe': df
            }
        }

    except Exception as e:
        print(f"Chart Error: {e}")
        return {'role': 'assistant', 'content': {'type': 'text', 'text': f"❌ Error generating chart: {type(e).__name__}: {str(e)}"}}