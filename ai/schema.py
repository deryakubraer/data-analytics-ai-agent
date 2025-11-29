from sqlalchemy import create_engine, inspect, text
import streamlit as st


def get_connection_string() -> str:
    if "connection_string" not in st.session_state or not st.session_state["connection_string"]:
        return None
    return st.session_state["connection_string"]

def get_schema() -> str:
    print("Getting database schema...")

    connection_string = get_connection_string()

    if not connection_string:
        print("No connection string found in session state.")
        return "❌ No database connection string found. Please enter it in the app."

    print("Extracting schema from the database...")

    # Create the engine
    engine = create_engine(connection_string)

    # Initialize inspector
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Initialize output string
    schema_output = ""
    schema_output += "="*50 + "\n"
    schema_output += "TABLES IN DATABASE\n"
    schema_output += "="*50 + "\n"
    for table in tables:
        schema_output += f"- {table}\n"

    schema_output += "\n" + "="*50 + "\n"
    schema_output += "TABLE COLUMNS AND THEIR PROPERTIES\n"
    schema_output += "="*50 + "\n"

    table_count = 0
    for table in tables:
        table_count += 1
        schema_output += f"\n{table_count}. Table: {table}\n"
        schema_output += "-"*12 + "\n"

        # Columns
        columns = inspector.get_columns(table)
        for col in columns:
            schema_output += f"  {col['name']}:\n"
            schema_output += f"    Type: {col['type']}\n"
            schema_output += f"    Nullable: {'YES' if col['nullable'] else 'NO'}\n"
            if col.get('primary_key', False):
                schema_output += f"    Key: PRI\n"

        # Foreign Keys
        fks = inspector.get_foreign_keys(table)
        if fks:
            schema_output += f"  Foreign Keys:\n"
            for fk in fks:
                schema_output += f"    {fk['constrained_columns']} -> {fk['referred_table']}({fk['referred_columns']})\n"

        # Indexes
        indexes = inspector.get_indexes(table)
        if indexes:
            schema_output += f"  Indexes:\n"
            for idx in indexes:
                schema_output += f"    {idx['name']} - columns: {idx['column_names']} - unique: {idx['unique']}\n"

        # Sample row safely
        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM `{table}` LIMIT 1"))
                row = result.mappings().first()  # safer mapping
                if row:
                    schema_output += f"  Sample row:\n"
                    for col_name in row.keys():
                        schema_output += f"    {col_name}: {row[col_name]}\n"
        except Exception as e:
            schema_output += f"  Could not fetch sample row: {e}\n"

    schema_output += f"\nThere are {table_count} tables\n"
    return schema_output

