import openpyxl

def test(file_):
    scga_workbook = openpyxl.load_workbook(file_)
    scga_sheets = scga_workbook.worksheets
    for sheet in scga_sheets:
        print(sheet.title)

if __name__ == "__main__":
    test(r"C:\Users\H471967\Documents\4_SelfDev\SCGA\SCGAs\Test2\EDSGGF_GS_GCOM_00_016_SCGA.xlsm")