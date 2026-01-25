#!/usr/bin/env python3
"""更新飞书多维表格中的正文内容"""
import requests
import json

# 飞书配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

# 需要更新的内容
CONTENT_MAP = {
    "射手座喜欢的电影类型": """【封面】
副标题: 观影指南
主标题第一行: 射手看电影
主标题第二行: 只挑【爽】的看
点缀语: 剧情不重要 感觉到位就行

【第1页】选片标准
射手选电影
从来不看【评分】
只看一眼预告片
【感觉对】就直接开刷
"评分是别人的，爽感是自己的"

【第2页】最爱类型
公路片 冒险片
那种【说走就走】的故事
看着别人浪
自己也跟着【心痒】
比什么爱情片过瘾多了

【第3页】观影习惯
射手看电影
经常忍不住【快进】
不是不尊重导演
是真的【等不及】知道结局
然后再倒回来看喜欢的片段

【第4页】雷点
最受不了
那种【磨磨唧唧】的剧情
明明一句话能说清楚
非要【拖】上三集
看得人想砸遥控器

【第5页】看完之后
看完一部好片
能【念叨】好几天
逢人就安利
恨不得全世界都来【一起爽】

【结尾】写给射手
人生如电影
射手只想当【主角】
不想当观众
爽过才算【没白活】

愿你的人生
比电影还精彩""",

    "射手座最舍得花钱的地方": """【封面】
副标题: 消费真相
主标题第一行: 射手花钱
主标题第二行: 从不心疼【体验】
点缀语: 钱没了可以赚 感觉错过就没了

【第1页】旅行
射手最舍得花钱的
永远是【旅行】
机票酒店可以不便宜
但那种【说走就走】的自由
比什么都值

【第2页】吃喝
美食面前
射手从不【委屈】自己
想吃就吃
人生苦短
【嘴巴开心】最重要

【第3页】兴趣爱好
一旦【上头】了
射手花钱眼都不眨
装备买最好的
课程报最贵的
虽然可能【三分钟热度】

【第4页】朋友聚会
和朋友出去玩
射手从来不【计较】
抢着买单是常态
钱花在【关系】上
永远值得

【第5页】省钱的地方
但日常开销
射手反而很【抠门】
能省则省
因为要把钱留着
花在【刀刃】上

【结尾】写给射手
钱是用来【花】的
不是用来存的
但花在哪里
决定你【活成什么样】

愿你的每一分钱
都花得值得""",

    "射手座的存钱能力": """【封面】
副标题: 扎心了
主标题第一行: 射手座存钱
主标题第二行: 全靠【缘分】
点缀语: 不是不想存 是钱不想留

【第1页】存钱意愿
射手不是【不想】存钱
每个月发工资
都暗暗发誓这次一定要存
然后看到机票打折
【算了】下个月再说

【第2页】花钱速度
钱在射手手里
就像【水】一样
不知道怎么就流走了
回头一看余额
自己都【吓一跳】

【第3页】理财方式
射手的理财
就是把钱【藏】起来
换个银行卡
删掉支付密码
眼不见心不烦
能存多少算【多少】

【第4页】破功时刻
本来存得好好的
突然看到想要的东西
【冲动】一上头
什么存钱计划
全部【作废】

【第5页】自我安慰
射手安慰自己
钱是【挣】出来的
不是省出来的
与其存钱焦虑
不如努力去【搞钱】

【结尾】写给射手
存钱这件事
【慢慢来】就好
钱会有的
自由也【会有】的

愿你早日实现
财务自由""",

    "给射手座的人生建议": """【封面】
副标题: 真心话
主标题第一行: 给射手座的
主标题第二行: 【人生建议】
点缀语: 来自一个懂你的人

【第1页】关于自由
自由很重要
但【责任】也是
不是逃避一切才叫自由
是有能力【选择】留下
才是真正的自由

【第2页】关于热情
三分钟热度不丢人
但偶尔也要试试
把【热情】坚持久一点
你会发现
深耕比广撒网更【有趣】

【第3页】关于表达
有话就说
别【憋着】
射手最怕委屈自己
不开心就表达
别等到爆发才【后悔】

【第4页】关于选择
不是每个决定
都需要【立刻】做出
慢下来想一想
有时候等待
也是一种【智慧】

【第5页】关于感情
遇到对的人
可以试着【停下来】
不用一直跑
有人愿意陪你走
比独自狂奔更【幸福】

【结尾】写给射手
人生是【旷野】
不是轨道
但旷野里也可以
建一个【家】

愿你自由且有归途
洒脱且有人懂""",

    "射手座认定你之后的变化": """【封面】
副标题: 恋爱真相
主标题第一行: 射手认定你
主标题第二行: 之后的【变化】
点缀语: 从浪子变成了家

【第1页】主动变多
以前你找他
现在他【主动】找你
消息秒回
约会自己【安排】
完全变了一个人

【第2页】分享变多
开始把你
【拉进】他的世界
朋友认识一下
爱好分享给你
所有好玩的都想【带上你】

【第3页】耐心变多
以前三分钟热度
现在对你
【超有耐心】
你说什么都认真听
吵架也愿意【先低头】

【第4页】计划变多
以前只活在当下
现在开始【规划】未来
明年去哪玩
以后住哪里
都会把【你】算进去

【第5页】自由变少
以前说走就走
现在会【想着】你
哪怕在外面浪
也会惦记着
想早点【回到】你身边

【结尾】写给射手
射手的爱
是把【自由】分你一半
是把远方
变成有【你】的地方

愿你的认定
换来同样的珍惜""",

    "射手座的朋友圈人格": """【封面】
副标题: 社交人格
主标题第一行: 射手座的
主标题第二行: 【朋友圈】人格
点缀语: 表面热闹 内心有数

【第1页】发圈频率
射手发朋友圈
全看【心情】
高兴了连发十条
不高兴了消失半年
完全没有【规律】可言

【第2页】发圈内容
射手的朋友圈
要么是【出去玩】
要么是好吃的
要么是突然的【人生感悟】
很少发自拍

【第3页】点赞习惯
射手点赞
全凭【直觉】
喜欢的秒赞
不感兴趣的刷过去
从来【不回头】

【第4页】评论风格
射手评论
要么【不评】
要么一针见血
绝对不会说那种
客套的【场面话】

【第5页】分组可见
射手的分组
其实特别【讲究】
什么人看什么内容
心里清楚得很
表面大大咧咧
实际上【门清】

【结尾】写给射手
朋友圈是【窗口】
不是全部
射手的真实
只给【值得的人】看

愿你的朋友圈
都是真朋友"""
}

def get_token():
    """获取访问令牌"""
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return resp.json()["tenant_access_token"]

def search_record(token, title):
    """根据标题搜索记录"""
    resp = requests.post(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "filter": {
                "conjunction": "and",
                "conditions": [
                    {"field_name": "标题", "operator": "is", "value": [title]}
                ]
            }
        }
    )
    data = resp.json()
    items = data.get("data", {}).get("items", [])
    return items[0] if items else None

def update_record(token, record_id, content):
    """更新记录的正文内容"""
    resp = requests.put(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "fields": {
                "正文内容": content
            }
        }
    )
    return resp.json()

def main():
    print("=" * 60)
    print("更新飞书多维表格正文内容")
    print("=" * 60)

    # 获取 token
    print("\n1. 获取访问令牌...")
    token = get_token()
    print("   ✓ 获取成功")

    # 更新每条记录
    print("\n2. 更新记录...")
    success = 0
    failed = 0

    for title, content in CONTENT_MAP.items():
        print(f"\n   处理: {title}")

        # 搜索记录
        record = search_record(token, title)
        if not record:
            print(f"   ✗ 未找到记录")
            failed += 1
            continue

        record_id = record.get("record_id")
        print(f"   找到记录: {record_id[:12]}...")

        # 更新内容
        result = update_record(token, record_id, content)
        if result.get("code") == 0:
            print(f"   ✓ 更新成功")
            success += 1
        else:
            print(f"   ✗ 更新失败: {result}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"更新完成: 成功 {success}, 失败 {failed}")
    print("=" * 60)

if __name__ == "__main__":
    main()
