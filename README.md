# 富士达电梯运维

## 要求

参照”原型设计图”完成相应的界面与功能，并提供代码。

* 所有电梯参数以什么方式提供给你？（答：JSON，CSV，或者在APP/WEB端直接进行修改）
* 今后若一个月做一次数据变更如何操作？（答：可以提供一个数据库同步功能，需要提前制定数据格式）
* 我司的文员是否能够操作？（答：傻瓜式一键操作）
* 后续使用是否还要产生费用？（答：后续会有服务器租用费用，100元/1月）
* 是否要签一份协议？（答：基于互信长久合作原则，不需要签，如果甲方要求，按照一期一期的签）
* 付款方式？（免费修复BUG，需求变更额外计费，费用按照计划表）

## 时间

### 富士达电梯运维-0.0.1（工期7天，费用11天）

* 11天，根据工作计划表的任务量的进行时间的估算。

## 人员

刘楚门，周兴邦，熊畅坤，韩文轩。

## 工作安排

| 项目                 | 任务          | 问题                                                         | 时间      | 人员   |
| -------------------- | ------------- | ------------------------------------------------------------ | :-------- | ------ |
| 富士达电梯维护-0.0.1 | 硬件          | 服务器<br />公网IP                                           | 100元/1月 | 刘楚门 |
|                      | 前端-APP      | 功能-地图<br />功能-地图-缩放<br />功能-电梯-查询<br />功能-电梯-编辑 | 4天       | 熊畅坤 |
|                      | 前端-数据管理 | 功能-电梯-数据同步<br />功能-电梯-数据同步-验证              | 2天       | 周兴邦 |
|                      | 后端-APP      | 接口-电梯-添加  <br />接口-电梯-编辑  <br />接口-电梯-查询   | 3天       | 韩文轩 |
|                      | 端-数据管理后 | 接口-电梯-数据同步<br />接口-电梯-数据同步-验证              | 2天       | 刘楚门 |
|                      | 测试真机      | 谷歌<br />小米<br />红米<br />魅族                           | 不定      | 刘楚门 |
|                      |               |                                                              |           |        |

# 前端-APP

![](prototype-design\APP.png)

# 前端-数据管理

![](prototype-design\数据管理.png)

## 电梯信息-验证

```python
###验证电梯数据是否符合要求
POST http://dungbeetles.xyz:60000/fujitec/sync
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
#输入
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="电梯信息.xls"
Content-Type: application/octet-stream

< ./电梯信息.xls
------WebKitFormBoundary7MA4YWxkTrZu0gW--
#输出
{
    "err":null,		#验证失败则返回明确的错误信息
    "val":true 		#true：格式正确，false：格式错误
}
```

## 电梯信息-同步

```python
###同步电梯数据到json文件数据
POST http://dungbeetles.xyz:60000/fujitec/sync
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
#输入
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="电梯信息.xls"
Content-Type: application/octet-stream

< ./电梯信息.xls
------WebKitFormBoundary7MA4YWxkTrZu0gW--
#输出
{
    "err":null,
    "val":true 		#true：同步成功，false：同步失败
}

```

### JSON数据库目录结构

```python
.
..
│  fujitec.py #后端接口服务
│
├─db
│  ├─湖南长沙金轮时代广场 #电梯信息JSON数据储存目录，每一行xls/csv数据对应一份json文件
│  │      XAA9550.json
│  │
│  └─湖南长沙长沙华润置地广场一期
│          XAA9548.json
│          XAA9549.json
│
└─static
    └─data
            电梯信息0524.xls #电梯信息文件上传目录
```

### 电梯信息-XLS/CSV格式

```python
# data/电梯信息.xls
工程名称,电梯编号(单台）,电梯类别,省份,城市
长沙华润置地广场一期,XAA9548,其它类型梯,湖南,长沙
长沙华润置地广场一期,XAA9549,F_SW扶梯,湖南,长沙
金轮时代广场,XAA9550,F_HS升降梯,湖南,长沙
```

### 电梯信息-JSON格式

```python
# db/湖南长沙 长沙华润置地广场一期/XAA9548.json
{
    "location":"湖南长沙长沙华润置地广场一期",    #电梯位置，由省份+城市+工程名称拼接而成
    "id":"XAA9548",			 #电梯编号，独一无二
    "type":"其它类型梯",		#电梯类型 F_SW扶梯，F_HS升降梯，其它类型梯
    "maintaining_type":"第三方保养", #保养类型 我方保养，即将我方保养，第三方保养：默认
    "maintaining_state":"未保养", #保养状态 已保养，未保养：默认
    "service_life":"10年"   #使用年限 10年：默认
}

# db/湖南长沙长沙华润置地广场一期/XAA9549.json
{
    "location":"湖南长沙长沙华润置地广场一期",  
    "id":"XAA9549",			 
    "type":"F_SW扶梯",		
    "maintaining_type":"第三方保养",
    "maintaining_state":"未保养",
    "service_life":"10年"
}

# db/金轮时代广场/XAA9550.json
{
    "location":"湖南长沙金轮时代广场",  
    "id":"XAA9550",			 
    "type":"F_HS升降梯",		
    "maintaining_type":"第三方保养",
    "maintaining_state":"未保养",
    "service_life":"10年"
}
```

