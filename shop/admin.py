from django.contrib import admin
from .models import Category, Product


import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
import csv



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug',]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available','description', 'materials', 'size','quantity']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'description', 'materials', 'size', 'quantity']
    prepopulated_fields = {'slug': ('name',)}

    actions = ['excel_file_create', 'export_to_csv']

    @admin.action(description="Cформировать файл для EXCEL")
    def excel_file_create(self, request, queryset):
        # Создаем новую рабочую книгу (файл)
        wb = Workbook()
        # Получаем активный лист (по умолчанию создается один лист)
        sheet = wb.active
        # Устанавливаем имя листа
        sheet.title = "Товары"
        # Записываем данные в ячейки

        abc = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I",
               10: "J", 11: "K", 12: "L", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R",
               19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X", 25: "Y", 26: "Z"}

        data = []
        # Формирую заголовок
        # data.append(list(queryset[0].__dict__.keys())[1:])
        data.append([field.verbose_name for field in self.model._meta.fields])

        # Формирую остальные строки
        [data.append(list(object.__dict__.values())[1:]) for object in queryset]
        for row in data:
            for i in range(len(row)):
                if isinstance(row[i], datetime.datetime):
                    row[i] = str(row[i].date()) + str(row[i].time())

        # Заношу данные
        for row in data:
            sheet.append(row)

        # Формирую информацию о размере таблицы(можно закоментировать этот блок, чтобы отображать таблицу в сыром виде)
        length = len(queryset[0].__dict__) - 1
        height = len(queryset) + 1

        # Задаю ширину ячеек
        for i in range(1, length + 1):
            sheet.column_dimensions[abc[i]].width = 20

        # Определяем диапазон для таблицы
        table = Table(displayName="MyTable", ref=f"A1:{abc[length]}{height}")
        # Настраиваем стиль таблицы
        style = TableStyleInfo(
            name="TableStyleMedium9", showFirstColumn=False,
            showLastColumn=False, showRowStripes=True, showColumnStripes=True
        )
        table.tableStyleInfo = style
        # Добавляем таблицу на лист
        sheet.add_table(table)

        # Сохраняем файл на диск
        name = " ".join(str(datetime.datetime.now()).split(':')).split('.')[0]
        # Чтобы файл сохранялся в корневую папку проекта можно оставить просто f"{name}.xlsx"
        wb.save(f'excel_files/goods/{name}.xlsx')

        with open(f"excel_files/goods/{name}.xlsx", "rb") as excel:
            data = excel.read()

            response = HttpResponse(data, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(name)

        return response

    # Для разнообразия оставил csv в версии без декоратора
    def export_to_csv(modeladmin, request, queryset):  # указывается modeladmin в отличии от версии с декоратором
        opts = modeladmin.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;' \
                                          'filename={}.csv'.format(opts.verbose_name)
        writer = csv.writer(response)
        fields = [field for field in opts.get_fields() if not field.many_to_many \
                  and not field.one_to_many]
        # Записываем первую строку с заголовками полей.
        writer.writerow([field.verbose_name for field in fields])
        # Записываем данные.
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                data_row.append(value)
            writer.writerow(data_row)
        return response

    export_to_csv.short_description = 'Экспорт в CSV'