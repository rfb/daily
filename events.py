import requests, csv, sqlite3, os

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE events (start, end, message, attribution)")

def fetch_events():
    response = requests.get(os.environ.get("EVENTS_URL"), stream=True)
    csv_stream = csv.StringIO(response.text)
    csv_reader = csv.reader(csv_stream)
    header = next(csv_reader)

    for row in csv_reader:
        row = [x if x != "" else None for x in row]
        cur.execute("INSERT INTO events (start, end, message, attribution) VALUES (?, ?, ?, ?)", row)

    cur.execute("""
      SELECT message, attribution FROM events
        WHERE start IS NULL and end IS NULL
        OR start IS NULL AND DATE(end) >= date()
        OR DATE(start) <= date() AND DATE(end) >= date()
        """)

    return cur.fetchall()


