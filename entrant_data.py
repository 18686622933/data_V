#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cx_Oracle
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Page, Pie
from pyecharts.charts import Bar


def get_grate_data(grate, id_info):
    """
    获取指定年级的学生信息
    先取 xsjbxxb ，如果未取到数据，则取 zfjwgljkfs.v_xssj
    :param grate: 入学年份，而不是当前所在级，int
    :param id_info: 数据库的账号信息 id/password@server_name
    :return: 返回 [(),(),...] (xh,xm,sfzh,rxrq(取年份),xy,zymc)
    """

    sql1 = "select xh,xm,substr(sfzh,0,2),sfzh,substr(rxrq,0,4),xy,zymc from xsjbxxb where substr(rxrq,0,4)=:x"
    sql2 = "select xh,xm,substr(sfzh,0,2),sfzh,substr(rxrq,0,4),xy,zymc from zfjwgljkfs.v_xssj where substr(rxrq,0,4)=:x"

    conn = cx_Oracle.connect(id_info)
    cur = conn.cursor()
    oracle_cursor = cur.execute(sql1, x=grate)
    result = [i for i in oracle_cursor]
    cur.close()
    if len(result) == 0:
        cur = conn.cursor()
        oracle_cursor = cur.execute(sql2, x=grate)
        result = [i for i in oracle_cursor]
        return result
    else:
        return result

    conn.close()


def get_API_data(old_data, adjust_value):
    """
    根据从数据库中获取到的学生数据(list)，按生源地统计人数，并将格式转换为pyecharts API格式，[["省份",人数],[],...]
    因为显示颜色的关系，这里需要给出一个值 来调整人数，来让显示更直观
    :param old_data: 从数据库获取到的数据 [(),(),...] (xh,xm,sfzh,rxrq(取年份),xy,zymc)
    :param adjust_value: 人数调整值，为了显示更直观
    :return:  pyecharts的API格式，[["省份",人数],[],...]
    """
    number_of_provinces = {"北京": 0, "天津": 0, "河北": 0, "山西": 0, "内蒙古": 0, "辽宁": 0, "吉林": 0, "黑龙江": 0,
                           "上海": 0, "江苏": 0, "浙江": 0, "安徽": 0, "福建": 0, "江西": 0, "山东": 0, "河南": 0,
                           "湖北": 0, "湖南": 0, "广东": 0, "广西": 0, "海南": 0, "重庆": 0, "四川": 0, "贵州": 0,
                           "云南": 0, "西藏": 0, "陕西": 0, "甘肃": 0, "青海": 0, "宁夏": 0, "新疆": 0,
                           "台湾": 0, "香港": 0, "澳门": 0}

    code_of_provinces = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林",
                         "23": "黑龙江", "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西",
                         "37": "山东", "41": "河南", "42": "湖北", "43": "湖南", "44": "广东", "45": "广西", "46": "海南",
                         "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏自治区", "61": "陕西", "62": "甘肃",
                         "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门"}

    for student in old_data:
        province = code_of_provinces[student[2]]
        number_of_provinces[province] += 1

    provinces = [[k, v] for k, v in number_of_provinces.items()]
    for i in provinces:
        i[1] += adjust_value

    return provinces


def geo_heatmap(name, data):
    c = (
        Geo()
            .add_schema(maptype="china")
            .add(name, data, type_=ChartType.HEATMAP, )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="Geo-HeatMap"),
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=250), )
    )
    return c


def pie_base(name, data) -> Pie:
    c = (
        Pie()
        .add(name, data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def bar_base_with_animation(x_values, one, two, three) -> Bar:
    c = (
        Bar(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="elasticOut"
                )
            )
        )
        .add_xaxis(x_values)
        .add_yaxis("2019", one)
        .add_yaxis("2018", two)
        .add_yaxis("2017", three)

        .set_global_opts(
        title_opts=opts.TitleOpts(title="近三年生源地统计图"),
        datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return c

id_info = "zfxfzb/zfsoft_hqwy@192.168.2.11"
re = get_grate_data(2019, id_info)
last_re = get_API_data(re, 50)
unadjust_re = get_API_data(re, 0)
pie_base("", unadjust_re).render(path="./2019级生源地饼图.html")
geo_heatmap("2019级生源地热图", last_re).render(path='./2019新生录取地热图.html')


re2019 = get_API_data(get_grate_data(2019, id_info), 0)
re2018 = get_API_data(get_grate_data(2018, id_info), 0)
re2017 = get_API_data(get_grate_data(2017, id_info), 0)

x = [i[0] for i in re2019]
one = [i[1] for i in re2019]
print(one)
two = [i[1] for i in re2018]
three = [i[1] for i in re2017]

bar_base_with_animation(x, one, two, three).render(path="./近三年生源地统计.html")
