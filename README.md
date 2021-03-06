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

| 项目                 | 任务          | 问题                                                         | 时间      | 人员   |
| -------------------- | ------------- | ------------------------------------------------------------ | :-------- | ------ |
| 富士达电梯维护-0.0.1 | 硬件          | ~~服务器~~<br />~~公网IP~~                                   | 100元/1月 | 刘楚门 |
|                      | 前端-APP      | ~~功能-地图~~<br />~~功能-地图-缩放~~<br />功能-电梯-查询<br />功能-电梯-编辑 | 4天       | 熊畅明 |
|                      | 前端-数据管理 | ~~功能-电梯-数据同步~~<br />~~功能-电梯-数据同步-验证~~      | 2天       | 周兴邦 |
|                      | 后端-APP      | ~~接口-电梯-编辑~~<br />~~接口-电梯-查询~~                   | 2天       | 韩文轩 |
|                      | 后端-数据管理 | ~~接口-电梯信息-同步~~<br />~~接口-电梯信息-验证~~           | 3天       | 韩文轩 |
|                      | 测试真机      | 谷歌<br />小米<br />红米<br />魅族                           | 不定      | 刘楚门 |
|                      |               |                                                              |           |        |

# 前端-APP

![img](./prototype-design/APP.png)

## 电梯信息-查询所有-简洁

```python
### 所有电梯信息
GET http://dungbeetles.xyz:60000/fujitec/elevators-less
#输入
#输出
{
    "err":null,
    "val":[
        [112.74692048046873,28.183942807485778,60,"第三方保养","华润置地广场一期","长沙","湖南"],
        [112.74692048046873,28.183942807485778,5,"我方保养","华润置地广场一期","长沙","湖南"]
    ]
}
```

## 电梯信息-查询

```python
### 所有电梯信息
GET http://dungbeetles.xyz:60000/fujitec/elevator
#输入
{
    "location":"长沙华润置地广场一期"
}
#输出
{
    "err":null,
    "val":[
        { 	# 电梯数2部
            "id":"XAA9548",			 #电梯编号，独一无二
            "type":"其它类型梯",		#电梯类型 扶梯：F/SW，升降梯：F/HS，其它类型梯：默认
            "maintaining_type":"第三方保养", #保养类型 代理商保养，第三方保养，我方保养，即将我方保养
            "maintaining_state":"已保养", #保养状态 未保养，已保养：默认
            "service_life":"10"   #使用年限 免保结束日后开始计算 
        },{
            "id":"XAA9549",			
            "type":"其它类型梯",		
            "maintaining_type":"我方保养",
            "maintaining_state":"已保养",
            "service_life":"10年"
        }
    ]
}
```

## 电梯信息-查询所有

```python
### 所有电梯信息
GET http://dungbeetles.xyz:60000/fujitec/elevators
#输入
#输出
{
    "err":null,
    "val":[{       
        	"city":"长沙",
            "longitude":112.74692048046873,
            "latitude":28.183942807485778,
            "location":"华润置地广场一期",    #电梯位置
            "elevators":[{ 	# 电梯数2部
                    "id":"XAA9548",			 #电梯编号，独一无二
                    "type":"其它类型梯",		#电梯类型 扶梯：F/SW，升降梯：F/HS，其它类型梯：默认
                    "maintaining_type":"第三方保养", #保养类型 代理商保养，第三方保养，我方保养，即将我方保养
                    "maintaining_state":"已保养", #保养状态 未保养，已保养：默认
                    "service_life":"10"   #使用年限 免保结束日后开始计算 
                },{
                    "id":"XAA9549",			
                    "type":"其它类型梯",		
                    "maintaining_type":"我方保养",
                    "maintaining_state":"已保养",
                    "service_life":"10年"
                }
            ]
        },{
        	"city":"株洲",
            "longitude":112.74692048046873,
            "latitude":28.183942807485778,
        	"location":"金轮时代广场",  
        	"elevators":[{	#电梯数1部
            	"id":"XAA9550",
                "type":"升降梯",
                "maintaining_type":"第三方保养",
                "maintaining_state":"未保养",
                "service_life":"10"
            }]
        }
    ]
}
```

## 电梯信息-修改

```python
### 修改一台电梯信息
PUT http://dungbeetles.xyz:60000/fujitec/elevator-set
#输入
{
    "location":"长沙华润置地广场一期",  #必填
    "id":"XAA9548",						 	#必填
    "type":"其它类型梯",		
    "maintaining_type":"我方保养",
    "maintaining_state":"已保养",
    "service_life":"10年"
}
#输出
{
    "err":null,		#失败返回明确的错误信息
    "val":true 		#true：格式正确，false：格式错误
}
```

# 前端-数据管理

[![img](./prototype-design/数据管理.png)

## 电梯信息-同步-日期

```python
###数据信息
GET http://dungbeetles.xyz:60000/fujitec/elevators-sync-date

#输出
{
    "err":null,		#失败返回明确的错误信息
    "val": "2010-06-01" 	#同步时间
}
```



## 电梯信息-同步-状态

```bash
###数据信息
GET http://dungbeetles.xyz:60000/fujitec/elevators-sync-status

#输出
{
    "err":null,		#失败返回明确的错误信息
    "val": {
        date:"2010-06-01", 	#同步时间
        count:4000, 	    #数据量
        status:'syncing',  	# syncing：同步中，synced：同步结束
        errors:[]			#同步失败的数据
    }
}
```

## 电梯信息-同步

```bash
###同步电梯数据到json文件数据
POST http://dungbeetles.xyz:60000/fujitec/elevators-sync
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

#输入
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="电梯信息.xls"
Content-Type: application/octet-stream

< C:\Users\SLTru\Desktop\fujitec\doc\电梯信息0527.xls
------WebKitFormBoundary7MA4YWxkTrZu0gW--
#输出
{
    "err":null, 	#失败返回明确的错误信息
    "val":true 		#true：开始同步，false：无法同步
}
```

### JSON数据库目录结构

```bash
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

```python
# data/电梯信息.xls
省份	地区	工程号	工程名	机种类别	维保状态	保养公司名	免保开始日	免保结束日	免保期限	项目地址
湖南	长沙	AEA1143	湖南长沙晚报	F/HS	代理商有偿保养	长沙富士达	2002-12-31	2003-12-31	12个月	
湖南	长沙	AEA1144	湖南长沙晚报	F/HS	代理商有偿保养	长沙富士达	2002-12-31	2003-12-31	12个月	
湖南	长沙	AEA1145	湖南长沙晚报	F/HS	代理商有偿保养	长沙富士达	2001-7-10	2002-7-10	12个月	
```

### 电梯信息-JSON格式

```python
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
    "service_life":"10年"   #使用年限 免保日开始后开始计算
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