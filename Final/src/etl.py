import os
import numpy as np
import requests

from bs4 import BeautifulSoup

import pandas as pd

import json
import time

import matplotlib.pyplot as plt

from skimage import data
from skimage.color import rgb2hsv

from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.color import rgb2gray

from skimage import io
import skimage
import os

from skimage import data
from skimage.color import rgb2hsv

from scipy import ndimage
from skimage.color import rgb2gray


def get_data(links, outdir):
    link0 = 'https://rkd.nl/en/explore/images/record?query=&filters[kunstenaar]=Mondriaan%2C+Piet&filters[kunstenaar_status][0]=Mondriaan%2C+Piet+%28huidig%29&filters[kunstenaar_kwalificatie][0]=Mondriaan%2C+Piet&start='
    oc = []
    sm = []
    years = []
    srcs = []
    known = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 46, 49, 50, 52, 53, 55, 57, 58, 60, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 97, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 109, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 176, 177, 178, 179, 180, 181, 182, 183, 184, 186, 187, 188, 189, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 305, 306, 307, 308, 309, 311, 312, 314, 315, 318, 319, 320, 322, 323, 324, 325, 326, 327, 328, 329, 332, 333, 334, 335, 337, 338, 339, 340, 341, 342, 346, 347, 348, 349, 350, 353, 354, 355, 356, 358, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 381, 382, 383, 385, 386, 388, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 473, 474, 475, 477, 478, 479, 481, 482, 485, 486, 487, 488, 489, 490, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 530, 531, 532, 533, 535, 536, 538, 539, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 555, 556, 557, 558, 559, 560, 562, 563, 564, 565, 566, 567, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 620, 656, 657, 658, 659, 660, 661, 662, 665, 666, 667, 668, 669, 671, 672, 673, 675, 676, 677, 678, 679, 680, 681, 682, 683, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 716, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 736, 737, 738, 740, 741, 742, 743, 790, 791, 792, 793, 794, 795, 796, 797, 798, 800, 801, 802, 803, 804, 805, 806, 807, 808, 810, 811, 812, 813, 814, 815, 816, 817, 821, 823, 824, 826, 827, 829, 830, 832, 833, 834, 839, 840, 843, 844, 845, 846, 848, 849, 850, 853, 854, 855, 856, 857, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 873, 874, 875, 876, 877, 878, 880, 881, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 909, 910, 911, 913, 914, 915, 916, 917, 918, 919, 920, 921, 923, 924, 925, 926, 927, 928, 929, 930, 931, 934, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 947, 948, 950, 951, 952, 953, 954, 955, 956, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 974, 975, 976, 977, 978, 980, 982, 983, 984, 985, 987, 988, 989, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1067, 1068, 1069, 1070, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1101, 1102, 1104, 1105, 1106, 1107, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1168, 1169, 1170, 1172, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1223, 1224, 1225, 1227, 1228, 1229, 1230, 1231, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1261, 1263, 1264, 1265, 1266, 1269, 1270, 1271, 1272, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1289, 1290, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1300, 1301, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1357, 1358, 1360, 1361, 1362, 1364, 1365, 1369, 1370, 1371, 1372, 1373, 1379, 1380, 1381, 1382, 1383, 1385, 1386, 1387, 1388, 1391, 1393, 1394, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1422, 1423, 1427, 1428, 1429, 1430, 1432, 1433, 1435, 1436, 1438, 1439, 1440, 1441, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1464, 1465, 1466, 1467, 1468, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1479, 1481, 1483]

    for i in range(len(links)):
        if i in known:
            if i%5 == 0 and i!=0:
                time.sleep(10)
            link = link0 + str(i)
            url = link

            response = requests.get(url)

            soup = BeautifulSoup(response.text, "html.parser")

            x = soup.find_all(id = 'galleria')
            y = soup.find_all('dl')
            try:
                a = x[0].find('img')['src']
                if a in links:
                    data = [i.text.strip() for i in soup.find_all('dd')]
                    oc.append(data[1])
                    sm.append(data[2])
                    srcs.append(a)

                    stringyear = ''
                    for i in y[4].text:
                        if len(stringyear) < 4:
                            try:
                                char = int(i)
                                stringyear += i
                            except:
                                continue
                    years.append(stringyear)
                    
                
            except:
                continue 
    datadict = {'srcs': links, 'Object categories': oc[:-1], 'Support/medium': sm[:-1], 'Dates': years }
    data = pd.DataFrame(datadict)
   
    return data

def pixel_count(img):
    pixelcount = img.shape[0] * img.shape[1]
    return pixelcount

def mean_saturation_brightness(img):
    rgb_img = img
    hsv_img = rgb2hsv(rgb_img)
    hue_img = hsv_img[:, :, 0]
    saturation_img = hsv_img[:,:, 1]
    value_img = hsv_img[:, :, 2]
    mean_saturation = np.mean(saturation_img, axis=(0,1))
    mean_brightness = np.mean(value_img)
    return [mean_saturation,mean_brightness]

def edgescore(img):
    hsv_img = rgb2hsv(img)
    value_img = hsv_img[:, :, 2]
    edges = ndimage.sobel(value_img)

    s = sum(edges)
    count = 0
    for i in range(len(s)):
        if s[i] != 0:
            count += 1
    return count

def unique_rgb(pic):
    uniquergb = np.unique(pic.reshape(-1, pic.shape[2]), axis=0)
    uniquergb = len(uniquergb)
    return uniquergb


def gray_var(img):
    gray_img = rgb2gray(img)
    return np.var(gray_img)

def entropy_var(img):
    gray_img = rgb2gray(pic)
    entr_img = entropy(gray_img, disk(10))
    return np.var(entr_img)

def new_color(pic):
    uniquergb = np.unique(pic.reshape(-1, pic.shape[2]), axis=0)
    #getting unique red, blue, green values
    uniquer = [i[0] for i in uniquergb]
    uniqueg = [i[1] for i in uniquergb]
    uniqueb = [i[2] for i in uniquergb]
    varr = np.var(uniquer)
    varg = np.var(uniqueg)
    varb = np.var(uniqueb)
    return np.mean([varr,varg,varb])

def add_features(df):
    '''
    adds features computed from each image
    '''
    pixels = []
    saturation = []
    brightness = []
    edges = []
    greyvar = []
    unknown = []
    uniquecolors = []
    entropyvar = []
    newcolors = []
    links = list(df['srcs'])

    for i in range(len(links)):
        try:
            pic = io.imread(links[i])
            saturation.append(mean_saturation_brightness(pic)[0])
            brightness.append(mean_saturation_brightness(pic)[1])
            edges.append(edgescore(pic))
            pixels.append(pixel_count(pic))
            greyvar.append(gray_var(pic))
            uniquecolors.append(unique_rgb(pic))
            entropyvar.append(entropy_var(pic))
            newcolors.append(new_color(pic))

        except:
            #print(i)
            unknown.append(i)
    
    df2 = {'Pixels': pixels, 'Saturation': saturation, 'Brightness': brightness, 'Edge': edges, 'Grey Var': greyvar, 'Unique Colors': uc, 'Entropy Variance': entropyvar, 'New Colors': newcolors}

    try:
        df = df.drop(['Unnamed: 0'], axis=1)
    except:
        df = df

    try:
        df2 = df2.drop(columns = ['Unnamed: 0'])
    except:
        df2 = df2


    df['Pixels'] = list(df2['Pixels'])
    df['Saturation'] = list(df2['Saturation'])
    df['Brightness'] = list(newdf['Brightness'])
    df['Edge'] = list(newdf['Edge'])
    df['Grey Var'] = list(newdf['Grey Var'])
    df['Unique Colors'] = list(newdf['Unique Colors'])
    df['Entropy Variance'] = list(newdf['Entropy Variance'])


    return df


def make_int(year):
    if year == '':
        return np.NaN 
    else:
        return int(year)

def clean_df(df):

    df = df.dropna()
    df = df[(df['Dates'] > 1800) & (df['Dates'] < 2000)]

    df['Edge'] = df['Edge']/df['Pixels']
    df['Dates'] = df['Dates'].apply(lambda x: make_int(x))
    df = df[(df['Edge'] > .0017) & (df['Edge'] < .003)].reset_index(drop=True)

    return df




# ---------------------------------------------------------------------
# Driver Function
# ---------------------------------------------------------------------

def get_data(links, outdir, **kwargs):

    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    make_df = get_data(links,**kwargs)
    make_features = add_features(make_df)
    clean = clean_df(make_features)
    clean.to_csv(os.path.join(outdir, 'datafile.csv'))
            
    return