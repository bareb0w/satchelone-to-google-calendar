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
- If your lesson times vary from times that satchelone shows then you can create an `TIMEOFFSET` environment variable in the format of a python dictionary with the time in the format `hh,mm` as the key and the new time as the value in the same format and add the length of your lessons in the `LESSONLENGTH` environment variable
- If you want to change the name of the calendar that the events are added to then change the `CALENDARNAME` environment variable. Make sure the calendar exists in your google account first.

- ColorID can be set to any of the following:
  The colors Google will show for each of the first 11 integers you can set colorId to.

``` text
1 blue
2 green
3 purple
4 red
5 yellow
6 orange
7 turquoise
8 gray
9 bold blue
10 bold green
11 bold red
```

## Example .env file

``` python
AUTHORIZATION = 'Bearer ###########################################################################################################################################################################################################################################################'
USER_ID = '########'
SCHOOL_ID = '#####'
COLORID = {"Supervised Study":"8","Physics":"7","Mathematic":"6","Computing":"2","PE":"11","Curriculum enriched":"3"}
TIMEOFFSET = {"10,00":"10,20","12,20":"13,00"}
LESSONLENGTH = 1
CALENDARNAME = "school"
```

## Limitations

- The satchelone calendar only shows about 3 weeks worth of lessons you will need to set the script to run periodically (about once a week)

## Warnings

- **Do not** share your authorization token with anyone as it is possible to control most of satchelone's function using it like managing todos and possibly even submitting work to teachers.
