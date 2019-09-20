#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import cx_Oracle
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Page, Pie
from pyecharts.charts import Bar
from pyecharts.charts import Funnel, Page


def get_db_data(id_info, sql):
    conn = cx_Oracle.connect(id_info)
    cur = conn.cursor()
    cur_exe = cur.execute(sql)
    result = [i for i in cur_exe]
    return result
    cur.close()
    conn.close()


def funnel_label_inside(title, data) -> Funnel:
    c = (
        Funnel()
            .add("", data, label_opts=opts.LabelOpts(position="inside"),
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title=title), legend_opts=opts.LegendOpts(is_show=False), )
    )
    return c


def bar_base_with_animation(title, x, y, y_label) -> Bar:
    c = (
        Bar(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="elasticOut"
                )
            )
        )
            .add_xaxis(x)
            .add_yaxis(y_label, y)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))

        .set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        # datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return c


id_info = "zfxfzb/zfsoft_hqwy@192.168.2.11"
sql = "SELECT jszgh,jsxm,COUNT(*) FROM " \
      "(SELECT * FROM (SELECT XKKH xkkha, XH, XM FROM XSXKBO WHERE XN = '2018-2019') A " \
      "LEFT JOIN (SELECT DISTINCT JSZGH, JSXM, XKKH, KCMC, KCXZ FROM JXRWB WHERE XN = '2018-2019' " \
      "UNION ALL SELECT DISTINCT JSZGH, JSXM, XKKH, KCMC, KCXZ FROM TYKJXRWB  WHERE XN = '2018-2019' " \
      "UNION ALL SELECT DISTINCT JSZGH, JSXM, XKKH, KCMC, KCXZ  FROM XXKJXRWB WHERE XN = '2018-2019') B " \
      "ON A.XKKHa = B.XKKH) " \
      "WHERE jszgh NOT IN ('06666','2017800401') GROUP BY jszgh,jsxm HAVING count(*) >=1500 ORDER BY COUNT(*) DESC"

out_data1 = get_db_data(id_info, sql)
in_data = {}
for i in out_data1:
    in_data[i[1]] = i[2]
out_data = [[k, v] for k, v in in_data.items()]

funnel_label_inside("指导学生最多的老师", out_data).render(path="./指导学生最多的老师.html")

sql2 = "SELECT kh,kcmc,gkrs,gkl FROM " \
       "(SELECT kh,kcmc,rs,gkrs,round(gkrs/rs,2) gkl FROM " \
       "(SELECT * FROM (SELECT substr(xkkh,0,22) kh,kcmc,COUNT(*) rs FROM " \
       "(SELECT  XKKH,KCMC,XH,XM,(CASE WHEN DYCJ IS NOT NULL THEN DYCJ ELSE to_number(a.CJ) END) zzcj FROM " \
       "(SELECT XKKH,KCMC,XH,XM,CJ FROM CJB WHERE XN='2018-2019'  AND  CJ IS NOT NULL ) A " \
       "LEFT JOIN (SELECT CJ,DYCJ FROM CJDZB) B ON A.CJ = B.CJ) GROUP BY substr(xkkh,0,22),kcmc) m " \
       " LEFT JOIN (SELECT * FROM (SELECT substr(xkkh,0,22) kh1,COUNT(*) gkrs FROM " \
       "(SELECT  XKKH,KCMC,XH,XM,(CASE WHEN DYCJ IS NOT NULL THEN DYCJ ELSE to_number(a.CJ) END) zzcj FROM " \
       "(SELECT XKKH,KCMC,XH,XM,CJ FROM CJB WHERE XN='2018-2019'  AND  CJ IS NOT NULL ) A " \
       "LEFT JOIN (SELECT CJ,DYCJ FROM CJDZB) B ON A.CJ = B.CJ) WHERE zzcj<60 GROUP BY substr(xkkh,0,22),kcmc)) n  " \
       "ON m.kh= n.kh1) WHERE gkrs IS NOT NULL AND rs>=10  ORDER BY gkl DESC) WHERE ROWNUM <=10"

out_data2 = get_db_data(id_info, sql2)
in_data2 = {}
for i in out_data2:
    in_data2[i[1]] = i[3]
bar_base_with_animation("挂科率最高的课程", [k for k in in_data2.keys()], [v for v in in_data2.values()], "挂科率").render(
    path="./挂科率最高的课程.html")
