# satchelone-to-google-calendar

## **Setup**

1. **Google Cloud Project**:
    - Create a new Google Cloud Desktop project.
    - Enable the Google Calendar API.
  
2. **Credentials**:
    - Place `credentials.json` (from your google cloud project) in the root of the repository.
  
3. **Google Calendar**:
    - Create a calendar in your Google account (e.g., 'school') and add it to your `.env` file.
  
4. **Network Tab**:
    - Open `satchelone.com`, navigate to the timetable page.
    - In the network tab, load the timetable page to capture the API request.
    - Add the authorization header to the `.env` file.

5. **Install Dependencies**:
    - Run `pip install -r requirements.txt` to install necessary modules.
  
6. **Run Script**:
    - Execute `main.py` to populate your Google Calendar with lessons.
  
## Customization

- **Event Colors**:

  - Set custom colors using the `COLORID` environment variable in the format: `{"EventName":"ColorID"}` (1-11).
- **Time Adjustments**:

  - Modify lesson times with `TIMEOFFSET` in the format: `{"OldTime":"NewTime"}`.
  - Set lesson length with `LESSONLENGTH` in hours.
- **Calendar Name**:

  - Change the calendar name with `CALENDARNAME` in the `.env` file (ensure it exists in your Google account).

## Possible Colors For The Events

```text
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
AUTHORIZATION = 'Bearer <YourToken>'
COLORID = {"Supervised Study":"8","Physics":"7","Mathematic":"6","Computing":"2","PE":"11","Curriculum enriched":"3"}
TIMEOFFSET = {"10:00":"10:20","12:20":"13:00"}
LESSONLENGTH = 1 #hours
CALENDARNAME = "School Timetable"
```

## Limitations

- The SatchelOne calendar displays approximately 3 weeks of lessons; set the script to run periodically (e.g., weekly).
- Auth token is valid for ~1 month, manually replace after expiration.

## Warnings

- **Authorization Token**:
  - Never share your authorization token to prevent potential misuse on SatchelOne.
