# satchelone-to-google-calendar

## Setup

1. Create a new Google cloud desktop project and enable the google calendar api.
2. Put the credentials.json into the root of the repo
3. Create a calendar in your google account called `school` which is what the script will add the lessons to
4. Open up satchelone.com, open up the network tab of your browser. Load the timetable page and you should see an API request to `"/api/timetable/school/{school_id}/student/{student_id}?requestDate=2023-12-25"`
5. Add your school id and student id to the .env file
6. The request should also have an authorization header which you should also add to the .env file.
7. Run `pip install -r requirements.txt` to install the required modules
8. Run the `main.py` file to add the tasks to your google calendar.
