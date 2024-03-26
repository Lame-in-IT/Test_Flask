import openpyxl

def creat_xksx(data):
    """Создание xlsx файла"""
    book = openpyxl.Workbook()
    del book['Sheet']
    sheet = book.create_sheet("Данные таблицы переводов")
    sheet["A1"] = "Фраза на русском"
    sheet.column_dimensions['A'].width = 30
    sheet["B1"] = "Транслитерация"
    sheet.column_dimensions['B'].width = 30
    row = 3
    for index_text, item_text in enumerate(data[0]):
        sheet[f"A{row}"] = item_text
        sheet[f"B{row}"] = data[1][index_text]
        row += 1
    book.save("Данные таблицы переводов.xlsx")
    book.close()