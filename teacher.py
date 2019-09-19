# from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Scatter

nf = [str(i) for i in range(1995, 2020)]
rz = [2, 3, 4, 5, 12, 10, 21, 26, 10, 24, 20, 35, 27, 38, 14, 37, 46, 24, 33, 61, 39, 81, 135, 111, 79]
zz = [1, 3, 3, 5, 12, 9, 19, 21, 9, 18, 16, 27, 24, 32, 13, 28, 32, 16, 21, 38, 24, 52, 81, 93, 68]
lz = [1, 0, 1, 0, 0, 1, 2, 5, 1, 6, 4, 8, 3, 6, 1, 9, 14, 8, 12, 23, 15, 29, 54, 18, 11]
lzl1 = [0.5, 0, 0.25, 0, 0, 0.1, 0.1, 0.19, 0.1, 0.25, 0.2, 0.23, 0.11, 0.16, 0.07, 0.24, 0.3, 0.33, 0.36, 0.38, 0.38,
        0.36, 0.4, 0.16, 0.14]
lzl = [67.0, 0, 25.0, 0, 0, 10.0, 10.0, 22.0, 18.0, 28.0, 29.0, 31.0, 23.0, 27.0, 25.0, 41.0, 39.0, 46.0, 54.0, 56.0,
       42.0, 39.0, 36.0, 9.0, 11.0]


def grid_mutil_yaxis() -> Grid:
    x_data = nf
    bar = (
        Bar()
            .add_xaxis(x_data)
            .add_yaxis("离职人数", lz, yaxis_index=1, color="#5793f3", stack="stack1", )
            .add_yaxis("在职人数", zz, yaxis_index=1, color="#d14a61", stack="stack1", )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False), )
            .extend_axis(
            yaxis=opts.AxisOpts(name="人数", position="left",
                                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#d14a61")),
                                axislabel_opts=opts.LabelOpts(formatter="{value} 人"),
                                ))
            .extend_axis(
            yaxis=opts.AxisOpts(name="离职率", position="right",
                                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#8F4586")),
                                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)),  # 刻度线
                                ))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="教师流动情况"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),  # x轴标签倾斜
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),  # 鼠标悬停刻度线
        )
    )

    line = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis(
            "离职率",
            lzl,
            yaxis_index=2,
            color="blue",
            # label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)
    # return bar


grid_mutil_yaxis().render("教师流动情况.html")
print(nf)
