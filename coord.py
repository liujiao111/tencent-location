import xlrd
from xlutils.copy import copy
import os
from transCoordinateSystem import gcj02_to_wgs84, gcj02_to_bd09, wgs84_to_gcj02, wgs84_to_bd09, bd09_to_gcj02, bd09_to_wgs84


def transfer(orgcoord, targetcoord, filename):
    '''
    坐标转换
    默认第一二列为经纬度
    :param filename:
    :return:
    '''
    workbook = xlrd.open_workbook(filename)
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(0)
    sheet = workbook.sheets()[0]
    index = 0
    for i in range(1, sheet.nrows):
        lon, lat = sheet.cell_value(i, 0), sheet.cell_value(i, 1)

        # 坐标转换
        if orgcoord == "1":
            if targetcoord == "1":
                pass
            elif targetcoord == "2":
                result = gcj02_to_wgs84(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
            elif targetcoord == "3":
                result = gcj02_to_bd09(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
        elif orgcoord == "2":
            if targetcoord == "1":
                result = wgs84_to_gcj02(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
            elif targetcoord == "2":
                pass
            elif targetcoord == "3":
                result = wgs84_to_bd09(float(lon), float(lat))
                lon = result[0]
                lat = result[1]

        elif orgcoord == "3":
            if targetcoord == "1":
                result = bd09_to_gcj02(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
            elif targetcoord == "2":
                result = bd09_to_wgs84(float(lon), float(lat))
                lon = result[0]
                lat = result[1]
            elif targetcoord == "3":
                pass



        for j in range(sheet.ncols):
            if index == 0:
                new_worksheet.write(i - 1, sheet.ncols + 1, 'lon-new')
                new_worksheet.write(i - 1, sheet.ncols + 2, 'lat-new')
            else:
                new_worksheet.write(i - 1, sheet.ncols + 1, lon)
                new_worksheet.write(i - 1, sheet.ncols + 2, lat)
        index = index + 1
    new_file_name = "upload/" + str(filename).split("/")[-1].split(".")[0] + "-new" + ".xls"
    new_file_path = os.path.abspath(os.getcwd()) + "/" + new_file_name
    new_workbook.save(new_file_path)  # 保存工作簿
    return new_file_name


