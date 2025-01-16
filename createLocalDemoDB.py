import sqlite3

def create_tables():
    conn = sqlite3.connect('GADB.db')
    cursor = conn.cursor()

    # List of table names
    topics = ['distributed_systems', 'networking', 'cloud_computing', 'databases', 'nsbm']

    # Drop tables if they exist
    for topic in topics:
        cursor.execute(f"DROP TABLE IF EXISTS {topic}")

    # Create tables
    for topic in topics:
        cursor.execute(f'''
        CREATE TABLE {topic} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contexts TEXT,
            about TEXT,
            overall TEXT
        )
        ''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully!")

def insert_data():
    # Data to be inserted into tables
    data = {
        'distributed_systems': [
            {
                'contexts': 'Large-scale applications like cloud computing, data centers, and peer-to-peer systems',
                'about': 'A distributed system is a network of independent computers that appear to the users as a single system.',
                'overall': 'Distributed systems improve fault tolerance, scalability, and resource sharing but pose challenges in synchronization and consistency.'
            }
        ],
        'networking': [
            {
                'contexts': 'Internet protocols, network infrastructure, and telecommunications',
                'about': 'Networking refers to the practice of connecting computers and devices to share data and resources.',
                'overall': 'Networking is fundamental to modern communication, enabling technologies like the Internet, IoT, and cloud services.'
            }
        ],
        'cloud_computing': [
            {
                'contexts': 'Hosting platforms, software as a service (SaaS), and scalable infrastructure',
                'about': 'Cloud computing provides on-demand access to computing resources over the Internet.',
                'overall': 'Cloud computing reduces costs and enhances flexibility but raises concerns about security and data privacy.'
            }
        ],
        'databases': [
            {
                'contexts': 'Data storage, retrieval, and management for applications and businesses',
                'about': 'A database is an organized collection of data that is easily accessible, managed, and updated.',
                'overall': 'Databases are critical for structured data management, enabling operations for businesses, research, and applications.'
            }
        ],
        'nsbm': [
            {
                'contexts': 'Higher education institution and research facilities in Sri Lanka',
                'about': 'NSBM Green University is a leading university in Sri Lanka offering degree programs in diverse disciplines. Dean of computing Faculty is Dr.Chaminda and There are around 500 staff members',
                'overall': 'NSBM focuses on academic excellence, sustainability, and research-driven education to prepare future-ready graduates.'
            }
        ]
    }

    conn = sqlite3.connect('GADB.db')
    cursor = conn.cursor()

    # Insert data into respective tables
    for topic, entries in data.items():
        for entry in entries:
            cursor.execute(f'''
            INSERT INTO {topic} (contexts, about, overall)
            VALUES (?, ?, ?)
            ''', (entry['contexts'], entry['about'], entry['overall']))

    conn.commit()
    conn.close()
    print("Data inserted into the tables successfully!")

def query_data():
    conn = sqlite3.connect('GADB.db')
    cursor = conn.cursor()

    # List of table names
    topics = ['distributed_systems', 'networking', 'cloud_computing', 'databases', 'nsbm']

    # Query data from each table
    for topic in topics:
        print(f"\nData from {topic}:")
        cursor.execute(f"SELECT * FROM {topic}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    create_tables()    # Step 1: Drop and recreate tables
    insert_data()      # Step 2: Insert data into tables
    query_data()       # Step 3: Query and display data
