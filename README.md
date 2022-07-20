# Line Bot OA
## _Covid-19 Tracking_

A tracking of location and time for your travel in Covid-19 situation.

- Tracking Location and Datetime
- Covid 19 Statistics Thailand
- [Covid19 Dashboard Thailand](https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=no&:isGuestRedirectFromVizportal=y&:display_spinner=no&:loadOrderID=0)

## Features

- Tracking IN and OUT of place.
- Show Covid 19 statistics in thailand.
- History of tracking for 14 days.

> "การได้ประวัติของผู้ป่วยและผู้เกี่ยวข้อง ซึ่งนำมาเขียนเป็น “ไทม์ไลน์” จะเริ่มตั้งแต่วันที่ทราบว่ามีผู้ติดเชื้อและย้อนหลังกลับไป โดยทั่วไปจะย้อนไปถึงเวลาประมาณ 2-3 สัปดาห์ก่อนหน้าที่จะเริ่มป่วยหรือเริ่มตรวจพบ เพราะเป็นระยะเวลาที่มีความเสี่ยงสูงที่จะเป็นจุดที่ได้รับเชื้อ"([“ไทม์ไลน์” หนึ่งสิ่งสำคัญล็อคเป้าควบคุมโควิด-19, 2564](https://www.hfocus.org/content/2020/12/20587))

## Tech

- [Python](https://www.python.org/) - Backend requires python v3.9.5+
- [Google Sheet](https://www.google.com/sheets/about/) - Create and collaborate on online spreadsheets in real-time and from any device.
- [Line](https://line.me/th/) - Frontend line OA
- [TableauScraper](https://github.com/bertrandmartel/tableau-scraping) - Scrap covid-19 data in thailand

## Installation

requires [Python](https://www.python.org/) v3.9.5+ to run.

#### Git clone
```sh
git clone https://github.com/miracleexotic/LineBot-Covid19.git
cd LineBot-Covid19
```

#### Pre-Deploy and Pre-Run
First, Need to **create** `authentication` folder in `LineBot-Covid19` folder.
```sh
mkdir -p authentication
touch config.json
```
Write this below code in `config.json`
and replace your **key** in `<KEY>` and your **PATH** in `<PATH-JSON-FILE>`
```
{
    "line": {
        "CHANNEL_ACCESS_TOKEN": "<KEY>",
        "CHANNEL_SECRET": "<KEY>"
    },
    "gspread": {
        "path": "<PATH-JSON-FILE>",
        "key": "<KEY>"
    }
}
```

#### PIP
Install the dependencies and devDependencies.
```sh
pip install -r src/requirements.txt
```

#### run
```sh
python wsgi.py
```

## Deployment
Deploy with [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
> This tutorial will have you deploying a Python app (a simple Django app) in minutes.
but in this code implement with **Flask**. You could adjust on your own.

## License

MIT

**Free Software, Hell Yeah!**

