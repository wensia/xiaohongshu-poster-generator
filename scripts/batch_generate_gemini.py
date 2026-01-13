#!/usr/bin/env python3
"""
批量生成双子座性格独白风套图 - 修复版
"""
import os
import re
import sys
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, '/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster')
from utils.screenshot import svg_to_png

# 模板路径
TEMPLATE_DIR = '/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster/assets/templates/personality-monologue'
OUTPUT_BASE = '/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output'

# 双子座 SVG 图标
GEMINI_SVG = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="60" height="60">
  <line x1="25" y1="20" x2="75" y2="20" stroke="#C4653A" stroke-width="4" fill="none"/>
  <line x1="25" y1="80" x2="75" y2="80" stroke="#C4653A" stroke-width="4" fill="none"/>
  <line x1="35" y1="20" x2="35" y2="80" stroke="#C4653A" stroke-width="4" fill="none"/>
  <line x1="65" y1="20" x2="65" y2="80" stroke="#C4653A" stroke-width="4" fill="none"/>
</svg>"""


def parse_highlight(text: str) -> str:
    """将【词】转换为 SVG tspan 高亮"""
    def replace(m):
        return f'<tspan fill="#C4653A">{m.group(1)}</tspan>'
    # 先处理已有的 tspan 标签内部
    result = re.sub(r'【([^】]+)】', replace, text)
    # 确保非高亮文字有正确的颜色
    if '<tspan' in result and not result.startswith('<tspan'):
        # 将整行包装，但保留高亮部分
        parts = re.split(r'(<tspan[^>]*>[^<]*</tspan>)', result)
        wrapped = []
        for part in parts:
            if part.startswith('<tspan'):
                wrapped.append(part)
            elif part:
                wrapped.append(f'<tspan fill="#3D3835">{part}</tspan>')
        result = ''.join(wrapped)
    return result


def generate_content_lines(lines: list, y_start: int = 0, line_height: int = 61) -> str:
    """生成正文行 SVG"""
    result = []
    for i, line in enumerate(lines):
        y = y_start + i * line_height
        # 处理高亮
        if '【' in line:
            processed = parse_highlight(line)
            result.append(f'    <text y="{y}" font-family="Noto Serif SC, serif" font-size="36" letter-spacing="2">{processed}</text>')
        else:
            result.append(f'    <text y="{y}" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="2">{line}</text>')
    return '\n'.join(result)


def parse_content(content: str) -> dict:
    """解析正文内容，提取各页数据"""
    pages = []
    current_page = None

    lines = content.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 封面
        if line.startswith('【封面】'):
            current_page = {'type': 'cover', 'title': line.replace('【封面】', '')}
            pages.append(current_page)
        # 内页
        elif line.startswith('【第') and '页】' in line:
            match = re.match(r'【第(\d+)页】(.+)', line)
            if match:
                current_page = {
                    'type': 'page',
                    'num': int(match.group(1)),
                    'section_title': match.group(2),
                    'content': [],
                    'quote': ''
                }
                pages.append(current_page)
        # 结尾
        elif line.startswith('【结尾】'):
            current_page = {
                'type': 'summary',
                'section_title': line.replace('【结尾】', ''),
                'content': [],
                'ending': []
            }
            pages.append(current_page)
        # 引用（以双引号开头）
        elif line.startswith('"') and current_page and current_page['type'] == 'page':
            current_page['quote'] = line.strip('"')
        # 正文内容
        elif current_page:
            if current_page['type'] == 'summary':
                # 结尾页的祝福语（通常是最后两行，不含高亮的短句）
                if len(current_page['content']) >= 4 and len(line) < 12 and '【' not in line:
                    current_page['ending'].append(line)
                else:
                    current_page['content'].append(line)
            elif current_page['type'] in ['page', 'cover']:
                if 'content' not in current_page:
                    current_page['content'] = []
                current_page['content'].append(line)

    return pages


def generate_cover_svg(record: dict, topic: str) -> str:
    """生成封面 SVG - 使用记录的标题和副标题"""
    with open(os.path.join(TEMPLATE_DIR, 'cover.svg'), 'r', encoding='utf-8') as f:
        template = f.read()

    # 从记录获取标题（两行）
    title = record.get('title', '')
    title_parts = title.split('\n')
    title_line1 = title_parts[0] if len(title_parts) > 0 else ''
    title_line2 = title_parts[1] if len(title_parts) > 1 else ''

    # 副标题
    subtitle = record.get('subtitle', '')

    # 从正文内容中提取标语（第一页的核心表达）
    content = record.get('content', '')
    pages = parse_content(content)

    # 获取封面的标语（从第一页内容提取）
    tagline1 = ''
    tagline2_text = ''
    tagline2_highlight = ''

    if len(pages) > 1 and pages[1]['type'] == 'page':
        first_page = pages[1]
        page_content = first_page.get('content', [])
        if len(page_content) >= 2:
            tagline1 = page_content[0].replace('【', '').replace('】', '')
            tagline2 = page_content[-1] if len(page_content) > 1 else ''
            # 解析标语高亮
            if '【' in tagline2:
                match = re.match(r'(.*)【([^】]+)】(.*)', tagline2)
                if match:
                    tagline2_text = match.group(1) + match.group(3)
                    tagline2_highlight = match.group(2)
            else:
                tagline2_text = tagline2

    # 处理主标题高亮（第一行和第二行）
    title_line1_processed = parse_highlight(title_line1)
    title_line2_processed = parse_highlight(title_line2)

    # 替换模板变量
    svg = template.replace('{{ZODIAC}}', '双子座')
    svg = svg.replace('{{TOPIC}}', topic)
    svg = svg.replace('{{ZODIAC_SVG}}', GEMINI_SVG)
    svg = svg.replace('{{SUBTITLE}}', subtitle)
    svg = svg.replace('{{TITLE_LINE1}}', title_line1_processed)
    svg = svg.replace('{{TITLE_LINE2}}', title_line2_processed)
    svg = svg.replace('{{TAGLINE1}}', tagline1)
    svg = svg.replace('{{TAGLINE2_TEXT}}', tagline2_text)
    svg = svg.replace('{{TAGLINE2_HIGHLIGHT}}', tagline2_highlight)
    svg = svg.replace('{{PAGE_NUM}}', '0 1')

    return svg


def generate_page_svg(data: dict, topic: str, page_num: int) -> str:
    """生成内页 SVG"""
    with open(os.path.join(TEMPLATE_DIR, 'page.svg'), 'r', encoding='utf-8') as f:
        template = f.read()

    # 生成正文内容
    content_lines = generate_content_lines(data.get('content', []))

    # 章节标题处理高亮
    section_title = parse_highlight(data.get('section_title', ''))

    # 替换模板变量
    svg = template.replace('{{ZODIAC}}', '双子座')
    svg = svg.replace('{{TOPIC}}', topic)
    svg = svg.replace('{{ZODIAC_SVG}}', GEMINI_SVG)
    svg = svg.replace('{{PART_NUM}}', f'{data.get("num", 1):02d}')
    svg = svg.replace('{{SECTION_TITLE}}', section_title)
    svg = svg.replace('{{CONTENT_LINES}}', content_lines)
    svg = svg.replace('{{QUOTE}}', data.get('quote', ''))
    svg = svg.replace('{{PAGE_NUM}}', f'0 {page_num}')

    return svg


def generate_summary_svg(data: dict, topic: str, page_num: int) -> str:
    """生成结尾页 SVG"""
    with open(os.path.join(TEMPLATE_DIR, 'summary.svg'), 'r', encoding='utf-8') as f:
        template = f.read()

    # 生成正文内容
    content_lines = generate_content_lines(data.get('content', []))

    # 结语
    ending = data.get('ending', [])
    ending_line1 = ending[0] if len(ending) > 0 else ''
    ending_line2 = ending[1] if len(ending) > 1 else ''

    # 章节标题
    section_title = data.get('section_title', '写给双子')

    # 替换模板变量
    svg = template.replace('{{ZODIAC}}', '双子座')
    svg = svg.replace('{{TOPIC}}', topic)
    svg = svg.replace('{{ZODIAC_SVG}}', GEMINI_SVG)
    svg = svg.replace('{{SECTION_TITLE}}', section_title)
    svg = svg.replace('{{CONTENT_LINES}}', content_lines)
    svg = svg.replace('{{ENDING_LINE1}}', ending_line1)
    svg = svg.replace('{{ENDING_LINE2}}', ending_line2)
    svg = svg.replace('{{PAGE_NUM}}', f'0 {page_num}')

    return svg


def generate_poster_set(record: dict) -> dict:
    """为一条记录生成完整套图"""
    record_id = record['record_id']
    title = record['title']
    subtitle = record['subtitle']
    content = record['content']

    # 提取话题
    topic_match = re.search(r'【([^】]+)】', title)
    topic = topic_match.group(1) if topic_match else '性格独白'

    # 创建输出目录
    timestamp = datetime.now().strftime('%y%m%d-%H%M')
    safe_title = re.sub(r'[【】\n\\/:*?"<>|]', '', title)[:10]
    output_dir = os.path.join(OUTPUT_BASE, datetime.now().strftime('%Y/%m/%d'), f'双子座-{safe_title}-{timestamp}')
    os.makedirs(output_dir, exist_ok=True)

    # 解析内容
    pages = parse_content(content)

    svg_files = []
    png_files = []
    page_num = 1

    for page_data in pages:
        if page_data['type'] == 'cover':
            # 封面 - 使用完整的 record 信息
            svg_content = generate_cover_svg(record, topic)
            svg_path = os.path.join(output_dir, 'cover.svg')
            png_path = os.path.join(output_dir, 'cover.png')
        elif page_data['type'] == 'page':
            # 内页
            page_num += 1
            svg_content = generate_page_svg(page_data, topic, page_num)
            svg_path = os.path.join(output_dir, f'page-{page_data["num"]:02d}.svg')
            png_path = os.path.join(output_dir, f'page-{page_data["num"]:02d}.png')
        elif page_data['type'] == 'summary':
            # 结尾页
            page_num += 1
            svg_content = generate_summary_svg(page_data, topic, page_num)
            svg_path = os.path.join(output_dir, 'summary.svg')
            png_path = os.path.join(output_dir, 'summary.png')
        else:
            continue

        # 保存 SVG
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        svg_files.append(svg_path)

        # 转换为 PNG
        try:
            svg_to_png(svg_path, png_path)
            png_files.append(png_path)
            print(f'  ✅ {os.path.basename(png_path)}')
        except Exception as e:
            print(f'  ❌ {os.path.basename(svg_path)}: {e}')

    return {
        'record_id': record_id,
        'output_dir': output_dir,
        'svg_files': svg_files,
        'png_files': png_files
    }


# 6条记录数据 - 包含完整的标题、副标题（更新后的内容）
RECORDS = [
    {
        'record_id': 'recv86QzWGZV9u',
        'title': '双子座说【没事】\n就是【有事】',
        'subtitle': '嘴硬心软的日常',
        'content': '''【封面】双子座的口是心非

【第1页】说没事的时候
其实【心里】在翻涌
只是不想让你担心
习惯了【独自消化】
"嘴硬只是不想让你担心"

【第2页】越说没事
越是【在意】
双子的倔强
全藏在【沉默】里
"沉默是最深的在乎"

【第3页】不是不想说
是怕【说出口】
你也不懂
还不如【自己扛】
"逞强是给你的温柔"

【第4页】表面云淡风轻
内心【翻江倒海】
笑着说没关系
转身【红了眼眶】
"我的情绪只在深夜上线"

【第5页】如果双子说没事
请【多问】一句
那句没事背后
是说不出口的【委屈】
"沉默有时比话语更需要回应"

【结尾】写给双子
你不必总是【逞强】
偶尔示弱也没关系
愿有人能【读懂】你的没事

愿你被温柔以待
不再独自承受'''
    },
    {
        'record_id': 'recv899UDj3mZC',
        'title': '双子座【恋爱】前后\n判若【两人】',
        'subtitle': '反差萌本萌',
        'content': '''【封面】双子座的恋爱反差

【第1页】恋爱前
【高冷】得像座冰山
谁追都爱理不理
一副【无所谓】的样子
"靠近可以 但别想读懂我"

【第2页】恋爱后
秒变【话痨】小可爱
一天发几百条消息
【黏人】得不行
"遇见你后 我认不出自己"

【第3页】追人的时候
【主动】得吓人
追到手之后
又开始【作】了
"得到了反而更患得患失"

【第4页】单身时
【潇洒】得很
恋爱后
天天想【腻】在一起
"我的时间观因你而改变"

【第5页】以前觉得恋爱麻烦
现在【甜蜜】得上头
双子一旦动心
就会【全力以赴】
"我的所有反差都是因为你"

【结尾】写给双子
恋爱里的你
【真实】又可爱
愿你遇到那个让你【变软】的人

愿你被偏爱
肆意做自己'''
    },
    {
        'record_id': 'recv899VbC6njH',
        'title': '双子座【吃醋】的样子\n嘴上说【不介意】',
        'subtitle': '口是心非代表',
        'content': '''【封面】双子座的醋意表达

【第1页】嘴上说不在乎
眼神却在【偷瞄】
说随便你
心里早就【炸了】
"我的嘴和心从来不同步"

【第2页】看到你和别人聊天
表面【淡定】
手机却攥得紧紧的
【酸】到不行
"我的大度都是装的"

【第3页】不会直接说吃醋
只会【阴阳怪气】
故意不回消息
等你来【哄】
"我的沉默是无声的吃醋"

【第4页】越是在意
越要【装作】无所谓
双子的醋意
都藏在【冷淡】里
"我的语气已经说明一切"

【第5页】其实很简单
想要你的【眼里】
只有我一个
不是【不介意】是太介意
"我的醋意只为你而泡"

【结尾】写给双子
吃醋不丢人
大胆【说出来】
愿有人懂你的【口是心非】

愿你被珍视
不必再伪装'''
    },
    {
        'record_id': 'recv899VPEIglx',
        'title': '双子座的【职场】人格\n上班下班【两个人】',
        'subtitle': '人格分裂现场',
        'content': '''【封面】双子座的职场双面

【第1页】上班的双子
【专业】又高效
开会发言有条理
同事都说【靠谱】
"工作中的我就是这么能打"

【第2页】下班的双子
瞬间【放飞】自我
能躺着绝不坐着
【懒】到极致
"下班后的我 请勿打扰"

【第3页】工作中
【社牛】附体
和谁都聊得来
回到家就【社恐】
"工作和生活是两个我"

【第4页】在公司
【情绪稳定】
回家才敢
把【疲惫】释放
"没人能同时看到两个我"

【第5页】不是双重人格
是【保护】自己的方式
职场是战场
回家才是【港湾】
"我的分裂有益身心健康"

【结尾】写给双子
你的【切换】很正常
该认真时认真
该【放松】时放松

愿你工作顺利
生活也有滋味'''
    },
    {
        'record_id': 'recv899WiDh06f',
        'title': '双子座【灵感】来了\n谁也【挡不住】',
        'subtitle': '创意爆发时刻',
        'content': '''【封面】双子座的灵感时刻

【第1页】灵感来的时候
【脑子】像开了挂
想法一个接一个
根本【停不下来】
"灵感不等人 我也不等天亮"

【第2页】可能在洗澡时
突然【灵光】一闪
可能在睡前
被【点子】砸醒
"我的脑洞不讲道理"

【第3页】一旦进入状态
整个世界【消失】
眼里只有那个
正在【成型】的想法
"别打扰我 我在创造"

【第4页】别人觉得疯狂
双子乐在其中
那种【创造】的快感
【上瘾】得很
"我的创造力也随机播放"

【第5页】灵感是双子的
【超能力】
虽然来去无踪
但每次都【惊艳】
"灵感珍贵 不容辜负"

【结尾】写给双子
你的【脑洞】是宝藏
别让别人的不理解
浇灭你的【热情】

愿你灵感常在
创意永不枯竭'''
    },
    {
        'record_id': 'recv899WOgurzK',
        'title': '2026双子座【翻身】的一年\n好运终于【来了】',
        'subtitle': '触底反弹开始',
        'content': '''【封面】双子座的2026运势

【第1页】过去几年
双子【扛】了太多
委屈 挫折 误解
都【熬】过来了
"该来的终于来了"

【第2页】2026开始
运势【回升】
之前种下的因
开始【结果】了
"机会已经在路上"

【第3页】事业上
会有【贵人】相助
之前的努力
终于被【看见】
"该来的人会来"

【第4页】感情上
该来的会【来】
不对的会【走】
一切都是最好的安排
"稳稳的幸福最踏实"

【第5页】双子要相信
你值得【好运】
那些咬牙坚持的日子
都会【发光】
"低谷是为了蹬得更高"

【结尾】写给双子
2026是你【翻身】的一年
勇敢向前
好运正在【路上】

愿你心想事成
万事胜意'''
    }
]


if __name__ == '__main__':
    print('🎨 开始批量生成双子座套图（修复版）...\n')

    results = []
    for record in RECORDS:
        print(f"📝 处理: {record['title'].replace(chr(10), ' ')}")
        result = generate_poster_set(record)
        results.append(result)
        print(f"   输出目录: {result['output_dir']}\n")

    # 保存结果
    results_path = os.path.join(OUTPUT_BASE, 'batch_results.json')
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f'\n✨ 完成! 共处理 {len(results)} 条记录')
    print(f'📄 结果保存至: {results_path}')
