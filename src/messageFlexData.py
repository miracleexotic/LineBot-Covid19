from linebot.models import FlexSendMessage

from tableauscraper import TableauScraper as TS

import gspread
import json

def create_template():
    template = {
        "type": "carousel",
        "contents": [] # template['contents'].append(bubble)
    }

    return template

def create_bubble():
    bubble = {
        "type": "bubble",
        "size": "giga",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Day",
                            "color": "#ffffff66",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": "01-01-1990", # bubble['header']['contents'][0]['contents'][1]['text'] = row[1]
                            "color": "#ffffff",
                            "size": "xl",
                            "flex": 4,
                            "weight": "bold"
                        }
                    ]
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#FF66B2",
            "spacing": "md",
            "height": "80px",
            "paddingTop": "22px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "เวลาเข้า - เวลาออก",
                    "color": "#b7b7b7",
                    "size": "xs",
                    "offsetBottom": "md"
                } # bubble['body']['contents'].append(bodyContent)
            ]
        }
    }

    return bubble

def create_bodyContent():
    bodyContent = {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": "23:44 - 23:45", # bodyContent['contents'][0]['text'] = row[2] - row[3]
                "size": "sm",
                "gravity": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "cornerRadius": "30px",
                        "height": "12px",
                        "width": "12px",
                        "borderColor": "#00CCCC",
                        "borderWidth": "2px"
                    },
                    {
                        "type": "filler"
                    }
                ],
                "flex": 0,
                "spacing": "none"
            },
            {
                "type": "text",
                "text": "ตำแหน่งที่ตั้ง", # bodyContent['contents'][2]['text'] = row[4]
                "gravity": "center",
                "size": "sm"
            }
        ],
        "spacing": "lg",
        "cornerRadius": "30px"
    }

    return bodyContent

class myFlexDate:
    """Create Flex Message for Date.

    Attributes:
        client (gspread.Client): Authenticate using a service account.
        sheet (gspread.Spreadsheet): Opens a spreadsheet specified by key (a.k.a Spreadsheet ID).
        nameWorksheet (str): Name of worksheet.
        wks (gspread.Worksheet): Worksheet with specified title.
    
    """

    def __init__(self, nameWorksheet):
        """Create Flex Message for Date.

        Args:
            nameWorksheet (str): Name of worksheet.
        
        """

        with open('../authentication/config.json') as fh:
            config = json.load(fh)

        self.client = gspread.service_account(filename=config['gspread']['path'])
        self.sheet = self.client.open_by_key(config['gspread']['key'])
        self.nameWorksheet = nameWorksheet
        try:
            self.wks = self.sheet.worksheet(nameWorksheet)
        except:
            self.wks = self.sheet.add_worksheet(title=nameWorksheet, rows="1", cols="20")

    @property
    def listDay(self):
        """Get All day and row list."""
        rows = self.wks.get_all_values()
        days = []
        for row in rows:
            if row[1] in days:
                continue
            days.append(row[1])

        return [days, rows]

    def createFlex(self):
        """Create Flex message."""
        days, rows = self.listDay

        template = create_template()
        for day in days:
            print(day)
            bubble = create_bubble()
            bubble['header']['contents'][0]['contents'][1]['text'] = day
            for row in rows:
                if row[1] == day:
                    print(row)
                    bodyContent = create_bodyContent()
                    bodyContent['contents'][0]['text'] = f"{row[2][:-3] if row[2] != '' else 'None'} - {row[3][:-3] if row[3] != '' else 'None'}"
                    bodyContent['contents'][2]['text'] = row[4]
                    bubble['body']['contents'].append(bodyContent)
            template['contents'].append(bubble)

        return FlexSendMessage(alt_text='Timeline', contents=template)
           
class myFlexCovid:
    """Create Flex Message for Covid-19 data.

    Attributes:
        template (Dict): Template for Flex message Covid-19 data.
    
    """

    def __init__(self) -> None:
        self.template = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "ข้อมูลทางสถิติ",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "COVID-19 🏥",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "สถานการณ์ผู้ติดเชื้อ COVID-19 อัพเดตรายวัน",
                    "size": "xs",
                    "color": "#aaaaaa"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "none",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "วันนี้",
                        "margin": "md",
                        "weight": "bold",
                        "decoration": "none",
                        "offsetStart": "none"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "😷 รายใหม่",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                            "offsetStart": "lg"
                        },
                        {
                            "type": "text",
                            "text": "999", # template['body']['contents'][4]['contents'][1]['contents'][1]['text'] = NewConfirmed
                            "size": "sm",
                            "color": "#111111",
                            "align": "end",
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "☠️ เสียชีวิต",
                            "size": "sm",
                            "color": "#FF4C29",
                            "flex": 0,
                            "offsetStart": "lg"
                        },
                        {
                            "type": "text",
                            "text": "999", # template['body']['contents'][4]['contents'][2]['contents'][1]['text'] = NewDeaths
                            "size": "sm",
                            "color": "#FF4C29",
                            "align": "end",
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "text",
                        "text": "ทั้งหมด",
                        "margin": "md",
                        "weight": "bold",
                        "decoration": "none",
                        "offsetStart": "none"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "ผู้ติดเชื้อสะสม",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "999", # template['body']['contents'][4]['contents'][4]['contents'][1]['text'] = Confirmed
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "เสียชีวิตสะสม",
                            "size": "sm",
                            "color": "#555555",
                            "flex": 0,
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "999", # template['body']['contents'][4]['contents'][5]['contents'][1]['text'] = Deaths
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                        {
                            "type": "text",
                            "size": "sm",
                            "color": "#555555",
                            "text": "กำลังรักษา"
                        },
                        {
                            "type": "text",
                            "size": "sm",
                            "color": "#111111",
                            "align": "end",
                            "text": "999" # template['body']['contents'][4]['contents'][7]['contents'][1]['text'] = Hospitalized
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                        {
                            "type": "text",
                            "text": "รักษาหายสะสม",
                            "size": "sm",
                            "color": "#555555"
                        },
                        {
                            "type": "text",
                            "text": "999", # template['body']['contents'][4]['contents'][8]['contents'][1]['text'] = Recovered
                            "size": "sm",
                            "color": "#111111",
                            "align": "end"
                        }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "ข้อมูลเพิ่มเติม",
                        "uri": "https://ddc.moph.go.th/covid19-dashboard/index.php?dashboard=main"
                        },
                        "style": "primary",
                        "height": "sm"
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "none"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "ข้อมูล ณ วันที่",
                        "size": "xs",
                        "color": "#aaaaaa",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "01/01/1990 13:26", # template['body']['contents'][6]['contents'][1]['text'] = UpdateDate
                        "color": "#aaaaaa",
                        "size": "xs",
                        "align": "end"
                    }
                    ]
                }
                ]
            },
            "styles": {
                "footer": {
                }
            }
        }
    
    def createFlex(self):
        """Create Flex message."""
        url = "https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=no&:isGuestRedirectFromVizportal=y&:display_spinner=no&:loadOrderID=0"
        ts = TS()
        ts.loads(url)

        self.template['body']['contents'][4]['contents'][1]['contents'][1]['text'] = str(ts.getWorksheet("D_New").data.to_dict()['SUM(case_new)-alias'][0])
        self.template['body']['contents'][4]['contents'][2]['contents'][1]['text'] = str(ts.getWorksheet("D_Death").data.to_dict()['SUM(death_new)-alias'][0])
        self.template['body']['contents'][4]['contents'][4]['contents'][1]['text'] = str(ts.getWorksheet("D_NewACM").data.to_dict()['SUM(case_new)-alias'][0])
        self.template['body']['contents'][4]['contents'][5]['contents'][1]['text'] = str(ts.getWorksheet("D_DeathACM").data.to_dict()['SUM(death_new)-alias'][0])
        self.template['body']['contents'][4]['contents'][7]['contents'][1]['text'] = str(ts.getWorksheet("D_Medic").data.to_dict()['SUM(in_medicate)-alias'][0])
        self.template['body']['contents'][4]['contents'][8]['contents'][1]['text'] = str(ts.getWorksheet("D_RecovACM").data.to_dict()['SUM(recovered_new)-alias'][0])
        self.template['body']['contents'][6]['contents'][1]['text'] = str(ts.getWorksheet("D_UpdateTime").data.to_dict()['max_update_date-alias'][0])
        
        return FlexSendMessage(alt_text='Covid19', contents=self.template)


if __name__ == "__main__":
    # data = myFlexDate('LINE-USER-ID')
    # data.createFlex()

    covid = myFlexCovid()
    covid.createFlex()


