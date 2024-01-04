# satchelone-to-google-calendar

## Setup

1. Create a new Google cloud desktop project and enable the google calendar api.
2. Put the credentials.json into the root of the repo
3. Create a calendar in your google account called `school` which is what the script will add the lessons to
4. Open up satchelone.com, open up the network tab of your browser. Load the timetable page and you should see an API request to `"/api/timetable/school/{school_id}/student/{student_id}?requestDate={some_date}"`
5. Add your school id and student id to the .env file
6. The request should also have an authorization header which you should also add to the .env file.
7. Run `pip install -r requirements.txt` to install the required modules
8. Run the `main.py` file to add the tasks to your google calendar.

## Customisation

- If you want to set custom colors for the events create an `COLORID` environment variable in the format of a python dictionary with the name of the event (from satchelone) and the colorid which ranges from 1-11
- If your lesson times vary from times that satchelone shows then you can create an `TIMEOFFSET` environment variable in the format of a python dictionary with the time in the format `hh,mm` as the key and the new time as the value in the same format and add the length of your lessons in the LESSONLENGTH environment variable
  
## Example .env file

``` python
AUTHORIZATION = 'Bearer ###############################################################################################################'
USER_ID = '########'
SCHOOL_ID = '#####'
COLORID = {"Supervised Study":"8","Physics":"7","Mathematic":"6","Computing":"2","PE":"11","Curriculum enriched":"3"}
TIMEOFFSET = {"10,00":"10,20","12,20":"13,00"}
LESSONLENGTH = 1
```
