# -*- coding: UTF-8 -*-
# @Time :2021/12/1 9:29
# @Author :Liuzheng
# @Email :1540234613@qq.com

from pywebio.input import *
from pywebio.output import *
from pywebio import start_server,input,output
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie
from sqlalchemy import create_engine
"""
1、连接本地数据库对数据进行统计分析
2、对上述结果调用pywebio、进行界面化处理
3、运用pyecharts、对结果进行展示
4、docker部署服务器
"""

def  main():
    output.put_markdown('# 2021年蓟州区普高录取数据统计分析')
    output.put_markdown('**文档说明：**')
    output.put_markdown("""
    - 对数据进行统计分析
    - 对上述结果调用pywebio、进行界面化处理
    - 运用pyecharts、对结果进行展示
    - docker部署服务器
    - 发现文档问题联系：liuzheng.pn@unicloud.com
        """)
    content = open(r'C:\Users\liuzheng\Desktop\2021年蓟州区普通高中录取分数线.png', 'rb').read()
    put_file('2021年蓟州区普通高中录取分数线.png', content, '2021年蓟州区普通高中录取分数线下载')
    #连接数据库
    conn = create_engine('mysql+pymysql://root:密码@ip:3306/?charset=utf8')
    sql="""
       select *  from (
select 
n1.录取校,n1.数量,n2.分数线
from (
select *  from (
select 录取校,count(1) as 数量  from liuzheng.2021年蓟州区普高录取结果信息表  GROUP BY 录取校 ) t ORDER BY t.`数量` desc ) n1 left join 

(select *  from liuzheng.2021年蓟州区普通高中录取分数线  ) n2  on n1.录取校=n2.学校名称) m ORDER BY m.`分数线`
    """
    data=pd.read_sql_query(sql,conn)
    # print(data)
    # output.put_markdown('##2021年蓟州区普高录取结果信息')
    # output.put_html(data)
    lqx=list(data['录取校'])
    sl=list(data['数量'])
    fsx=list(data['分数线'])

    c = (
        Bar()
            .add_xaxis(lqx)
            .add_yaxis('分数线', fsx)
            .add_yaxis("招生数量", sl)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="2021年蓟州区普高录取结果(按分数线排名)"))

    )

    c.width = "120%"
    put_html(c.render_notebook())

    output.put_markdown(f'**分析结果：从图中可以看出分数线最高的是{lqx[-1]}({fsx[-1]})，排名前3位的分别是{lqx[-1]}({fsx[-1]})、{lqx[-2]}({fsx[-2]})、{lqx[-3]}({fsx[-3]})**')

    #性别比例
    sql2 = """
        select 性别,count(1) as 数量 from liuzheng.2021年蓟州区普高录取结果信息表  GROUP BY 性别
        """
    data2 = pd.read_sql_query(sql2, conn)
    xb=list(data2['性别'])
    xb_sl=list(data2['数量'])

    c = (
        Pie()
            .add("", [list(z) for z in zip(xb, xb_sl)])
            .set_global_opts(title_opts=opts.TitleOpts(title="2021年蓟州区普高录取男女比例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    )

    c.width = "100%"
    put_html(c.render_notebook())

    output.put_markdown(f'**分析结果：从图中可以看出男生人数为{xb_sl[1]}，女生人数为{xb_sl[0]}**')





if __name__ == '__main__':
    start_server(main, port=8088)
