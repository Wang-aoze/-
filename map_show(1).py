import requests
import json
import math
import folium
#定义一个函数，传入线路名称相当于在高德地图搜索，来获取每趟公交的站点名称和经纬度
def get_location(city,line,mykey):
    url_api='https://restapi.amap.com/v3/bus/linename?city={}&keywords={}&key={}&extensions=all'.format(city,line,mykey)
    res = requests.get(url_api).text
    rt = json.loads(res)
    i = 0
    line_name = rt['buslines'][0]['name']
    polyline = rt['buslines'][0]['polyline']
    info = [line_name, polyline]
    stop = rt['buslines'][0]['busstops']
    type=rt['buslines'][0]['type']#线路类型
    name = rt['buslines'][0]['name']  # 线路名称
    start_time=rt['buslines'][0]['start_time']#开始营运时间
    end_time = rt['buslines'][0]['end_time']  # 停止营运时间
    time_buy=''
    try:
        time_buy=start_time+'--'+end_time
    except:
        pass
    company = rt['buslines'][0]['company']  # 公交公司
    distance=rt['buslines'][0]['distance']  # 总里程
    basic_price = rt['buslines'][0]['basic_price']  # 参考票价
    form_lines=""
    for i in range(len(stop)):
        station = stop[i]['name']
        location = stop[i]['location']
        info_ = [line, station, location]
        form_lines +=info_[1]
        if i!=(len(stop)-1):
            form_lines += ','
        if (i+1)%4==0:
            form_lines+='\n'
    back_lines = ""
    for i in range(len(stop)):
        station = stop[len(stop)-i-1]['name']
        location = stop[len(stop)-i-1]['location']
        info_ = [line, station, location]
        back_lines += info_[1]
        if i != (len(stop) - 1):
            back_lines += ','
        if (i+1)%4==0:
            back_lines+='\n'
    '''
    线路名称--------name
    线路类型--------type
    运行时间--------time_buy
    总里程----------distance   
    公交公司---------company
    正向路线---------form_lines
    反向向路线---------back_lines
    [name,type,time_buy,distance,company,form_lines,back_lines,info[1]]
    '''
    cnt = 0
    x = []  # busstop站点坐标x
    y = []  # busstop站点坐标y
    plots_name = []  # 车站名称
    length = len(stop)
    for i in range(length):   #遍历 stop 列表中的每个车站，然后将它们的坐标和名称分别存储在 x、y 和 plots_name 列表中
        x.append(f"{stop[i]['location']}".split(",")[0])   #获取了每个站点的坐标
        y.append(f"{stop[i]['location']}".split(",")[1])
        plots_name.append(f"{stop[i]['name']}")    #添加车站的名称


    return [x,y,plots_name,polyline]

def gcj02towgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def transformlat(lng, lat):  #经纬度坐标的偏移转换
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret
def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

def coordinates(c):   #使用逗号 , 进行分割，得到经度 (lng) 和纬度 (lat) 的字符串。然后，它使用 float() 函数将这些字符串转换为浮点数
    lng, lat = c.split(',')
    lng, lat = float(lng), float(lat)
    wlng, wlat = gcj02towgs84(lng, lat)
    return wlng, wlat
def transf_xy(f_x,f_y):
    res=[]

    for i in range(len(f_x)):
        g_x,g_y=gcj02towgs84(f_x[i],f_y[i])
        res.append([g_y,g_x])
    return res
def draw_map(f_x,f_y,name,city,line):
    trans_data=transf_xy(f_x,f_y)
    bj_map = folium.Map(location=trans_data[0], zoom_start=12,attr='高德-常规图',) #地图中心，缩放值12
    sta=0
    for i in trans_data:   #循环遍历坐标数据，为每个坐标点创建一个，添加到地图对象中
        folium.Marker(
            location=i,
            popup=name[sta],
            icon=folium.Icon(icon='cloud')
        ).add_to(bj_map)
        sta+=1
    for i in range(len(trans_data)-1):
        folium.PolyLine(locations=[trans_data[i],trans_data[i+1]], color='green').add_to(bj_map)   #两点之间画一条绿色的折线
    bj_map.save(f'map/{city}{line}地图.html')
def draw_city_line(city,line,mykey):
    data=get_location(city,line,mykey)#更换城市和线路
    f_x = [float(item) for item in data[0]]
    f_y = [float(item) for item in data[1]]
    name=data[2]
    draw_map(f_x,f_y,name,city,line)

# 公交坐标数据转化
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率
mykey='4aca394e7bea4547ba8ad7f4cf02e34e'
print('请输入城市：')
city=input()
print('请输入线路名：')
line=input()
draw_city_line(city,line,mykey)
