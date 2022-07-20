import gspread
import json

class Data:
    """Handle data for Google sheet.
    
    Attributes:
        client (gspread.Client): Authenticate using a service account.
        sheet (gspread.Spreadsheet): Opens a spreadsheet specified by key (a.k.a Spreadsheet ID).
        nameWorksheet (str): Name of worksheet.
        wks (gspread.Worksheet): Worksheet with specified title.

    """

    def __init__(self, nameWorksheet: str) -> None:
        """Handle data for Google sheet.

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
        """Get All day list."""
        list_of_lists = self.wks.get_all_values()
        day = []
        for row in list_of_lists:
            if row[1] in day:
                continue
            day.append(row[1])

        return day

    def delRow(self):
        """Delete row."""
        day = self.listDay
        if len(day) > 15:
            delDay = day[0]
            while self.wks.row_values(1)[1] == delDay:
                self.wks.delete_rows(1)

    def insertData_inside(self, data: list):
        """Insert data with message event['เข้า']."""
        self.wks.append_rows([data])

    def insertData_outside(self, timeData: str):
        """Insert data with message event['ออก']."""
        cell = self.wks.row_values((self.wks.row_count))
        if len(cell[3]) > 0:
            return
        self.wks.update_cell(self.wks.row_count, 4, f"'{timeData}")
    

if __name__ == '__main__':
    data = ["Username", '01/01/1990', "1:11:11", "", "NameLocation", "Location", "(99.999xxxxxxxxxxxx, 999.999xxxxxxxxxxx)"]
    myData = Data('test')
    myData.insertData_inside(data)
    print(len(myData.listDay))
    myData.delRow()
    print(len(myData.listDay))
    # myData.insertData_outside("10:44:02")


