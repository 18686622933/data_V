#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cx_Oracle
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Page, Pie
from pyecharts.charts import Bar, Funnel

conn = cx_Oracle.connect("zfxfzb/zfsoft_hqwy@192.168.2.11")
cur = conn.cursor()
sql = "SELECT zymc,male/male,round(female/male,2) bl FROM (SELECT * FROM (SELECT zymc,COUNT(1) male FROM zfjwgljkfs.v_xssj WHERE rxrq=2019 AND xb='男' GROUP BY zymc) a LEFT JOIN (SELECT zymc zymc1,COUNT(1) female FROM zfjwgljkfs.v_xssj WHERE rxrq=2019 AND xb='女' GROUP BY zymc ) b ON a.zymc = b.zymc1) ORDER BY bl DESC"
sqlxy = "SELECT xy, MALE / MALE, ROUND(FEMALE / MALE, 2) BL FROM (SELECT * FROM (SELECT xy, COUNT(1) MALE  FROM ZFJWGLJKFS.V_XSSJ  WHERE RXRQ = 2019  AND XB = '男'  GROUP BY xy) A  LEFT JOIN (SELECT xy ZYMC1, COUNT(1) FEMALE  FROM ZFJWGLJKFS.V_XSSJ  WHERE RXRQ = 2019  AND XB = '女'  GROUP BY xy) B ON A.xy = B.ZYMC1) ORDER BY BL DESC"
result = cur.execute(sql)
in_data1 = [[i[0], i[2]] for i in result]
print(in_data1)
cur.close()

cur = conn.cursor()
result_dict = cur.execute(sql)
re_dict = {}
for i in result_dict:
    re_dict[i[0]] = i[2]
print(re_dict)
cur.close()


cur = conn.cursor()
result_xy = cur.execute(sqlxy)
data_xy = [[i[0], i[2]] for i in result_xy]
print(data_xy)
cur.close()
conn.close()
def bar_base_with_animation(x_values, one) -> Bar:
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

            .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return c

def funnel_label_inside(title, data):
    c = (
        Funnel(init_opts=opts.InitOpts(height="500px"))
            .add("", data,label_opts=opts.LabelOpts(position="inside")
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title=title), legend_opts=opts.LegendOpts(is_show=False),
                             )
    )
    return c


def bar_reversal_axis() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts(height="800px",width="1300px"))
        .add_xaxis([k for k in re_dict.keys()])
        .add_yaxis("", [v for v in re_dict.values()])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="2019级各专业男女比例"))
    )
    return c

funnel_label_inside("2019级各专业男女比例", in_data1).render()
funnel_label_inside("2019级各学院男女比例", data_xy).render("2019级各学院男女比例.html")
bar_reversal_axis().render("2019级专业院男女比例.html")
