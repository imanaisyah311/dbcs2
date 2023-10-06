import mysql.connector

# Replace these with your RDS instance details
host = "DESKTOP-A91QDH7"
port = 3306  # Replace with your RDS port (usually 3306)
user = "SalesSystem"
password = "Shawn25@"
database_name = "SalesSystem"  # Replace with your database name

try:
    # Create a connection to the RDS instance
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database_name  # Specify the database to use
    )

    if conn.is_connected():
        print("Connected to the database!")

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Define your SQL CREATE TABLE statement
        create_table_sql = """
        CREATE TABLE sample_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT
        )
        """

        # Execute the SQL statement to create the table
        cursor.execute(create_table_sql)
        print("Sample table created successfully!")

        # Close the cursor and the connection
        cursor.close()
        conn.close()

except Exception as e:
    print("Error:", e)
