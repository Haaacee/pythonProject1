from turtledemo.penrose import start
import pandas as pd
import numpy as np
from database import Database


BotDB = Database('.venv/botdb')
def get_df(numpy_array, my_list):
    try:
        datearray = numpy_array[startrange,1]
    except:
        stop = 1
        return stop
    datanp = datearray.date()
    arrayprepodovatel = 0 #Переменная для подсчета строк при редактировании ФИО преподавателя в цикле
    nomer = 0

    for x in range(len(my_list)):
        numpy_array[my_list[nomer],1] = datanp
        nomer+=1

    df = numpy_array[(numpy_array == datanp).any(axis=1)]

    my_list.reverse()
    for x in range(len(my_list)):
        numpy_array = np.delete(numpy_array, (my_list[x]), axis=0)

    listydal = list()
    condition = 1
    odnapara = 0
    propusk = 0
    dveparu = 0
    for x in range(len(df)):
        if propusk == 1:
            propusk = 0
            continue
        else:
            prepodavatel = df[x, 3]
            colum5n = df[x, 4]
            colum2n = df[x, 2]
            columnpredmet = df[x - 1, 3]
            if x != len(df) - 1:
                columnpredmet2 = df[x + 1, 3]
                proverkaculumnpredmet2 = pd.isnull(columnpredmet2)
            else:
                proverkaculumnpredmet2 = True
            proverkacolum5n = pd.isnull(colum5n)
            proverkaprepodavatel = pd.isnull(prepodavatel)
            proverkacolum2n = pd.isnull(colum2n)
            proverkaculumnpredmet = pd.isnull(columnpredmet)
            if proverkaprepodavatel != True and x != 0 and arrayprepodovatel >= 4:
                if arrayprepodovatel == 6:
                    df[x, 0] = df[0, 0]
                    df[x, 4] = df[x + 1, 3]
                    condition = 0
                    odnapara = 2
                    arrayprepodovatel = 0
                else:
                    df[x, 4] = df[x + 3, 3]
                    df[x + 3, 3] = df[x, 3]
                    df[x + 3, 4] = df[x, 4]
                    df[x, 0] = df[0, 0]
                    df[x + 3, 0] = df[x, 0]
                    df[x + 3, 2] = df[x + 2, 2]
                    arrayprepodovatel = 0
                    condition = 0
            elif  x != 0 and condition == 0 and odnapara == 2 and proverkaculumnpredmet != True:
                listydal.append(x)
                continue
            elif proverkaprepodavatel != True and x != 0 and condition == 0 and odnapara == 1 and proverkaculumnpredmet != True:
                df[x, 4] = df[x + 1,3]
                df[x, 0] = df[0, 0]
                condition = 0
                odnapara = 2
            elif proverkaprepodavatel != True and x != 0 and dveparu == 1:
                dveparu = 0
                continue
            elif proverkaprepodavatel != True and x != 0 and condition == 0:
                odnapara = 1
                continue
            elif proverkaculumnpredmet2 != True and proverkaprepodavatel != True:
                df[x, 4] = df[x + 1, 3]
                df[x, 0] = df[0, 0]
                listydal.append(x + 1)
                propusk = 1
            elif proverkaprepodavatel != True and x != 0:
                if x >= 6:
                    df[x, 4] = df[x + 3, 3]
                    df[x, 0] = df[0, 0]
                    df[x + 3, 0] = df[0, 0]
                    df[x + 3, 2] = df[x + 2, 2]
                    df[x + 3, 3] = df[x, 3]
                    df[x + 3, 4] = df[x, 4]
                    listydal.append(x + 1)
                    listydal.append(x + 2)
                    condition = 0
                else:
                    df[x, 4] = df[x + 3, 3]
                    df[x, 0] = df[0, 0]
                    df[x + 3, 4] = df[x, 4]
                    df[x + 3, 3] = df[x, 3]
                    df[x + 3, 0] = df[x, 0]
                    df[x + 3, 2] = df[x + 2, 2]
                    arrayprepodovatel = 0
                    dveparu = 1
            elif proverkaprepodavatel != True and x == 0:
                df[x, 4] = df[x + 3, 3]
                df[x + 3, 0] = df[x, 0]
                df[x + 3, 2] = df[x + 2, 2]
                df[x + 3, 3] = df[x, 3]
                df[x + 3, 4] = df[x, 4]
                dveparu = 1
                arrayprepodovatel += 1
            else:
                arrayprepodovatel += 1
                if proverkaprepodavatel == True and proverkacolum5n == True:
                    listydal.append(x)

    unique_listydal = list(set(listydal))
    unique_listydal.reverse()
    for x in range(len(unique_listydal)):
        df = np.delete(df, (unique_listydal[x]), axis=0)

    dataframe=pd.DataFrame(df, columns=['Day', 'Data', 'Vremya', 'Para', 'Prepodavatel'])
    return dataframe



def length123(numpy_array, startrange):
    my_list = list()
    my_list.append(startrange)
    for x in range(startrange + 1, len(numpy_array)):
        rekvizit = numpy_array[x, 1]
        naimpara = numpy_array[x, 3]
        proverka = pd.isnull(rekvizit)
        if proverka == True:
            my_list.append(x)
        else:
            break
    return my_list

def excelparser():
    data = pd.read_excel('1.xlsx')
    pd.set_option("display.max_columns", None)
    pd.options.display.expand_frame_repr = False
    numpy_array = data.values
    startrange = 19
    attempt = 1
    for x in range(startrange, len(numpy_array)):
        dlinaspiska = length123(numpy_array, startrange)
        if len(dlinaspiska) == 1:
            break
        else:
            BotDB.add_raspisanie(get_df(numpy_array, dlinaspiska))
            startrange = startrange + len(dlinaspiska)
            attempt+=1
