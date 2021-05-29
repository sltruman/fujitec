# 富士达电梯运维

## 要求

参照”原型设计图”完成相应的界面与功能，并提供代码。

- 所有电梯参数以什么方式提供给你？（答：JSON，CSV，或者在APP/WEB端直接进行修改）
- 今后若一个月做一次数据变更如何操作？（答：可以提供一个数据库同步功能，需要提前制定数据格式）
- 我司的文员是否能够操作？（答：傻瓜式一键操作）
- 后续使用是否还要产生费用？（答：后续会有服务器租用费用，100元/1月）
- 是否要签一份协议？（答：基于互信长久合作原则，不需要签，如果甲方要求，按照一期一期的签）
- 付款方式？（免费修复BUG，需求变更额外计费，费用按照计划表）

## 时间

### 富士达电梯运维-0.0.1（工期7天，工作量11天）

- 初步想法主要是要实现：我们品牌（富士达）电梯的所在项目位置！
- 红色表示我们自己保养的！
- 蓝色表示第三方保养的！
- 黄色表示不久会进入我们保养的！
- 数字要实现可以任意修改，每个项目点击可以看到该项目的一些信息（包括具体位置、电梯数量、使用年限）！上述信息可以实现不定期便捷的修改！
- 能体现哪些项目保养了，哪些项目没保养这等内容，便于我们管理，可以在图标上动点心思，比如加一个字：未，已。或者换个图标，坏电梯或者好电梯。

## 人员

刘楚门，周兴邦，熊畅明，韩文轩。

## 工作安排

| 项目                 | 任务          | 问题                                                   | 时间      | 人员   |
| -------------------- | ------------- | ------------------------------------------------------ | --------- | ------ |
| 富士达电梯维护-0.0.1 | 硬件          | 服务器 公网IP                                          | 100元/1月 | 刘楚门 |
|                      | 前端-APP      | 功能-地图 功能-地图-缩放 功能-电梯-查询 功能-电梯-编辑 | 4天       | 熊畅明 |
|                      | 前端-数据管理 | 功能-电梯-数据同步 功能-电梯-数据同步-验证             | 2天       | 周兴邦 |
|                      | 后端-APP      | 接口-电梯-编辑 接口-电梯-查询                          | 2天       | 韩文轩 |
|                      | 后端-数据管理 | 接口-电梯信息-同步 接口-电梯信息-验证                  | 3天       | 韩文轩 |
|                      | 测试真机      | 谷歌 小米 红米 魅族                                    | 不定      | 刘楚门 |
|                      |               |                                                        |           |        |

# 前端-APP

[![img](https://github.com/sltruman/fujitec/raw/main/prototype-design%5CAPP.png)](https://github.com/sltruman/fujitec/blob/main/prototype-design\APP.png)

## 电梯-查询

```
### 所有电梯信息
GET /fujitec/elevators
#输入
#输出
{
    "err":null,		
    "val":[{
            "longitude":112.74692048046873,
            "latitude":28.183942807485778,
            "location":"长沙华润置地广场一期",    #电梯位置
            "elevators":[{ 	# 电梯数2部
                    "city":"长沙",
                    "longitude":112.74692048046873,
                    "latitude":28.183942807485778,
                    "id":"XAA9548",			 #电梯编号，独一无二
                    "type":"其它类型梯",		#电梯类型 扶梯：F/SW，升降梯：F/HS，其它类型梯：默认
                    "maintaining_type":"第三方保养", #保养类型 
                                                    # 代理商保养：代理商有偿保养，代理商免保中
                                                    # 第三方保养：其他公司保养
                                                    # 我方保养：有偿保养中，免保中
                                                    # 即将我方保养：默认
                    "maintaining_state":"已保养", #保养状态 未保养，已保养：默认
                    "service_life":"10年"   #使用年限 免保结束日后开始计算 
                },{
                    "city":"长沙",
                    "longitude":112.74692048046873,
                    "latitude":28.183942807485778,
                    "id":"XAA9549",			 #电梯编号，独一无二
                    "type":"其它类型梯",		#电梯类型 扶梯：F/SW，升降梯：F/HS，其它类型梯：默认
                    "maintaining_type":"我方保养",
                    "maintaining_state":"已保养",
                    "service_life":"10年"
                }
            ]
        },{
        	"longitude":112.74692048046873,
        	"latitude":28.183942807485778,
        	"location":"株洲金轮时代广场",  
        	"elevators":[{	#电梯数1部
                "longitude":112.74692048046873,
                "latitude":28.183942807485778,
            	"id":"XAA9550",
                "type":"升降梯",
                "maintaining_type":"第三方保养",
                "maintaining_state":"未保养",
                "service_life":"10年"
            }]
        }
    ]
}
```

## 电梯-修改

```
### 修改一台电梯信息
PUT /fujitec/elevator-set
#输入
{
    "city":"长沙",
    "longitude":112.74692048046873,
    "latitude":28.183942807485778,
    "id":"XAA9548",			 #电梯编号，独一无二
    "type":"其它类型梯",		#电梯类型 扶梯：F/SW，升降梯：F/HS，其它类型梯：默认
    "maintaining_type":"第三方保养", #保养类型 
                                     # 代理商保养：代理商有偿保养，代理商免保中
                                     # 第三方保养：其他公司保养
                                     # 我方保养：有偿保养中，免保中
                                     # 即将我方保养：默认
    "maintaining_state":"已保养", #保养状态 未保养，已保养：默认
    "service_life":"10年"   #使用年限 免保结束日后开始计算 
                
}
#输出
{
    "err":null,		#失败返回明确的错误信息
    "val":true 		#true：格式正确，false：格式错误
}
```

# 前端-数据管理

[![img](https://github.com/sltruman/fujitec/raw/main/prototype-design%5C%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86.png)](https://github.com/sltruman/fujitec/blob/main/prototype-design\数据管理.png)

## 电梯信息-验证

```
###验证电梯数据是否符合要求
POST http://dungbeetles.xyz:60000/fujitec/elevators_sync
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
#输入
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; file="电梯信息.xls"
Content-Type: application/octet-stream

< ./电梯信息.xls
------WebKitFormBoundary7MA4YWxkTrZu0gW--
#输出
{
    "err":null,		#失败返回明确的错误信息
    "val":true 		#true：格式正确，false：格式错误
}
```

## 电梯信息-同步

```
###同步电梯数据到json文件数据
POST http://dungbeetles.xyz:60000/fujitec/elevators-valid
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
#输入
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; file="电梯信息.xls"
Content-Type: application/octet-stream

< ./电梯信息.xls
------WebKitFormBoundary7MA4YWxkTrZu0gW--
#输出
{
    "err":null, 	#失败返回明确的错误信息
    "val":true 		#true：同步成功，false：同步失败
}
```

### JSON数据库目录结构

```
.
..
│  fujitec.py #后端接口服务
│
├─db #电梯信息JSON数据储存目录
│  ├─金轮时代广场 # 目录名是工程名
│  │      XAA9550.json 每一行xls/csv数据对应一份json文件
│  │
│  └─长沙华润置地广场一期
│         XAA9548.json
│         XAA9549.json
│
└─static
    └─data #电梯信息文件上传目录
          电梯信息0524.xls 
```

### 电梯信息-XLS/CSV格式

```
# data/电梯信息.xls
地区,工程号,工程名,机种类别,维保状态,保养公司名,免保开始日,免保结束日,免保期限,项目地址
长沙,AEA1143,湖南长沙晚报,F/HS,代理商有偿保养,长沙富士达,2002-12-31,2003-12-31,12个月, 	
长沙,EXF5072,湖南长沙晚报,F/J,代理商有偿保养,长沙富士达,2000-1-1,2001-1-1,12个月, 
长沙,KAX2217,长沙房地产交易市场,F/SW,停用,不明,2007-5-22,2008-5-22,12个月, 	
```

### 电梯信息-JSON格式

```
# db/长沙华润置地广场一期/XAA9548.json
{
    "city":"长沙",
    "longitude":112.74692048046873,
    "latitude":28.183942807485778,
    "id":"XAA9548",			 #电梯编号，独一无二
    "type":"其它类型梯",		#电梯类型 扶梯：F/SW，升降梯：F/HS，其它类型梯：默认
    "maintaining_type":"第三方保养", #保养类型 
    							  	# 代理商保养：代理商有偿保养，代理商免保中
    								# 第三方保养：其他公司保养
    								# 我方保养：有偿保养中，免保中
    								# 即将我方保养：默认
    "maintaining_state":"已保养", #保养状态 未保养，已保养：默认
    "service_life":"10年"   #使用年限 免保结束日后开始计算
}

# db/长沙华润置地广场一期/XAA9549.json
{
    "city":"长沙",
    "longitude":112.74692048046873,
    "latitude":28.183942807485778,
    "id":"XAA9549",			 
    "type":"扶梯",		
    "maintaining_type":"第三方保养",
    "maintaining_state":"未保养",
    "service_life":"10年"
}

# db/金轮时代广场/XAA9550.json
{
    "city":"长沙",
    "longitude":112.74692048046873,
    "latitude":28.183942807485778,
    "id":"XAA9550",			 
    "type":"升降梯",		
    "maintaining_type":"第三方保养",
    "maintaining_state":"未保养",
    "service_life":"10年"
}
```