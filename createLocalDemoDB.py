import sqlite3


def create_tables():
    conn = sqlite3.connect("GADB.db")
    cursor = conn.cursor()

    # List of table names
    topics = [
        "distributed_systems",
        "networking",
        "cloud_computing",
        "databases",
        "nsbm",
    ]

    # Drop tables if they exist
    for topic in topics:
        cursor.execute(f"DROP TABLE IF EXISTS {topic}")

    # Create tables
    for topic in topics:
        cursor.execute(
            f"""
        CREATE TABLE {topic} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contexts TEXT,
            about TEXT,
            overall TEXT
        )
        """
        )

    conn.commit()
    conn.close()
    print("Database and tables created successfully!")


def insert_data():
    # Data to be inserted into tables
    data = {
        "distributed_systems": [
            {
                "contexts": "Large-scale applications like cloud computing, data centers, and peer-to-peer systems",
                "about": "A distributed system is a network of independent computers that appear to the users as a single system.",
                "overall": "Distributed systems improve fault tolerance, scalability, and resource sharing but pose challenges in synchronization and consistency.",
            }
        ],
        "networking": [
            {
                "contexts": "Internet protocols, network infrastructure, and telecommunications",
                "about": "Networking refers to the practice of connecting computers and devices to share data and resources.",
                "overall": "Networking is fundamental to modern communication, enabling technologies like the Internet, IoT, and cloud services.",
            }
        ],
        "cloud_computing": [
            {
                "contexts": "Hosting platforms, software as a service (SaaS), and scalable infrastructure",
                "about": "Cloud computing provides on-demand access to computing resources over the Internet.",
                "overall": "Cloud computing reduces costs and enhances flexibility but raises concerns about security and data privacy.",
            }
        ],
        "databases": [
            {
                "contexts": "Data storage, retrieval, and management for applications and businesses",
                "about": "A database is an organized collection of data that is easily accessible, managed, and updated.",
                "overall": "Databases are critical for structured data management, enabling operations for businesses, research, and applications.",
            }
        ],
        "nsbm": [
            {
                "contexts": "Higher education institution and research facilities in Sri Lanka",
                "about": """About NSBM Computing Faculty - Faculty of Computing (FOC) provides world-class education and training in Computing and Information Technology, both at the undergraduate as well as postgraduate levels.
                            FOC offers University Grants Commission’s approved degree programmes in multiple disciplines. It has also partnered with the world top ranking universities, University of Plymouth in UK and Victoria University in Australia, to provide undergraduates with highly recognized International Degrees. The innovative teaching methods, along with the latest state-of-the-art equipment, form the perfect blend that motivates our students to do their best and reach their goals with ease.
                            The Faculty provides top-notch research, training and development services that will help students acquire new knowledge along with the best practices in their respective disciplines. The FOC aims to be among the foremost centre of excellence in Research and Development (R&D) and advance education in computing while taking into consideration national as well as regional requirements for Information and Communication Technology.
                            The FOC places equal emphasis on both theory and practice of all aspects of the computing field, enabling our students to have sufficient hands-on experience to take up any working assignment in their respective IT fields at the end of their degree programmes. So, look no further for that perfect computing degree; NSBM’s Faculty of Computing is the ideal choice!

                            Departments
                            Department of Computer and Data Science

                            Click here
                            Department of Computer Security and Network Systems

                            Click here
                            Department of  Software Engineering & Information Systems

                            Click here
                            Degree Programmes
                            The Faculty of Computing offers a plethora of pathways and specializations for its undergraduates. This vast choice ensures that the academic component of all interests and dream careers are fulfilled whilst also promising a holistic educational experience in any discipline of your choice.

                            Department of Computer and Data Science
                            BSc (Hons) Computer Science – (Plymouth University – United Kingdom)
                            BSc (Hons) in Computer Science – (UGC Approved – Offered By NSBM)
                            BSc (Honours) in Data Science – (UGC Approved – Offered By NSBM)
                            BSc (Hons) in Data Science – (Plymouth University – United Kingdom)
                            Department of Computer Security and Network Systems
                            BSc (Hons) Computer Networks – (Plymouth University – United Kingdom)
                            BSc (Hons) Computer Security – (Plymouth University – United Kingdom)
                            Bachelor of Information Technology (Major in Cyber Security) – (Victoria University – Australia)
                            BSc (Hons) in Computer Networks – (UGC Approved – Offered By NSBM)
                            Department of Software Engineering & Information Systems
                            BSc (Hons) Software Engineering – (Plymouth University – United Kingdom)
                            BSc (Hons) in Software Engineering – (UGC Approved – Offered By NSBM)
                            BSc (Hons) Technology Management – (Plymouth University – United Kingdom)
                            BSc in Management Information Systems (Special) – (UGC Approved – Offered By NSBM)
                            Foundation Programme for Bachelor’s Degree
                            
                            Dean's Message
                            Welcome to the Faculty of Computing of NSBM Green University. NSBM is a dynamic young organization offering innovative educational products to cater to the needs of the fast-developing business and industrial economies in the world. Your course of study will be up-to-date and relevant and will be delivered by well-qualified staff geared to prepare you for employment. The NSBM Graduate profile and student charter aim to develop the students to achieve what they expect in their chosen career paths. As students of NSBM, you are expected to work hard and set high standards. To help you achieve success, you are provided with excellent staff as well as student support services to help deal with your needs. Our academic (both local and foreign), administrative and technical staff with which you work will be ready to advise and facilitate you. It is your responsibility to take your course of studies very seriously and make full use of the diverse range of learning opportunities provided to you, managing your time effectively in class and in self-directed assignments. With the staunch belief in creating reliable and holistic individuals, our wish is to see you become successful in life and be a good ambassador for the university.
                            Prof. Chaminda Wijesinghe,
                            Dean – Faculty of Computing

                            Faculty News
                            NSBM’s faculties are always abuzz with excitement and vivacity, with students participating in immersive academic activities – outbound training sessions, workshops, guest lectures, field trips – and are even found promoted to celebrity status, as our students take on the stage – as singers, actors, musicians, dancers, orators and even magicians!

                            Testimonial
                            My journey began at the National School of Business Management (NSBM) in Sri Lanka, where I graduated with a BSc (Hons) in Computer Science in December 2016. NSBM provided a strong foundation that has propelled me forward in my academic and professional journeys.

                            dilan_jayasekara
                            Dilan Jayasekara
                            Branch Executive Committee Member
                            Australian Computer Society
                            I am a proud alumnus of NSBM, where I completed my Bachelor of Computer Science degree as a part of the 15.1 batch. NSBM Green University is an excellent institution that provides a comprehensive and rigorous education in many fields, as well as a supportive and inspiring environment for students.

                            kasun-alumni
                            Kasun Magedaragama
                            Principal Technology Solution Architect
                            Oracle ASEAN region
                            Faculty of Computing
                            NSBM Green University, Mahenwaththa,
                            Pitipana, Homagama,
                            Sri Lanka.

                            New Enrollments
                            Tel:+94 (11) 544 5000

                            Current Students
                            Tel+94 (11) 544 6000

                            New Enrollments
                            Email: inquiries@nsbm.ac.lk

                            Current Students
                            Email: ar.foc@nsbm.ac.lk""",
                "overall": """NSBM focuses on academic excellence, sustainability, and research-driven education to prepare future-ready graduates.""",
            }
        ],
    }

    conn = sqlite3.connect("GADB.db")
    cursor = conn.cursor()

    # Insert data into respective tables
    for topic, entries in data.items():
        for entry in entries:
            cursor.execute(
                f"""
            INSERT INTO {topic} (contexts, about, overall)
            VALUES (?, ?, ?)
            """,
                (entry["contexts"], entry["about"], entry["overall"]),
            )

    conn.commit()
    conn.close()
    print("Data inserted into the tables successfully!")


def query_data():
    conn = sqlite3.connect("GADB.db")
    cursor = conn.cursor()

    # List of table names
    topics = [
        "distributed_systems",
        "networking",
        "cloud_computing",
        "databases",
        "nsbm",
    ]

    # Query data from each table
    for topic in topics:
        print(f"\nData from {topic}:")
        cursor.execute(f"SELECT * FROM {topic}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    conn.close()


if __name__ == "__main__":
    create_tables()  # Step 1: Drop and recreate tables
    insert_data()  # Step 2: Insert data into tables
    query_data()  # Step 3: Query and display data
