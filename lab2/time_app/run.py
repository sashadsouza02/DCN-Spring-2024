from flask import Flask
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/time')
def time():
    # Set the timezone to Eastern Time
    eastern = pytz.timezone('US/Eastern')
    # Get the current time in UTC and convert it to Eastern Time
    time_now = datetime.now(pytz.utc).astimezone(eastern)
    # Format the time as a string
    formatted_time = time_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    return formatted_time

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

