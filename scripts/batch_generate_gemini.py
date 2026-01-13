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

    # 处理主标题高亮（第一行）
    title_line1_processed = parse_highlight(title_line1)

    # 替换模板变量
    svg = template.replace('{{ZODIAC}}', '双子座')
    svg = svg.replace('{{TOPIC}}', topic)
    svg = svg.replace('{{ZODIAC_SVG}}', GEMINI_SVG)
    svg = svg.replace('{{SUBTITLE}}', subtitle)
    svg = svg.replace('{{TITLE_LINE1}}', title_line1_processed)
    svg = svg.replace('{{TITLE_LINE2}}', title_line2)
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


# 6条记录数据 - 包含完整的标题、副标题
RECORDS = [
    {
        'record_id': 'recv86QzWGZV9u',
        'title': '双子座说【没事】\n就是有事',
        'subtitle': '嘴硬心软的日常',
        'content': '''【封面】双子座说没事就是有事

【第1页】嘴上说的【没事】
别信
其实心里已经【翻江倒海】
只是不想让你担心
"嘴和心从来不同步"

【第2页】【报喜不报忧】
是双子的习惯
宁愿自己【消化】情绪
也不愿成为别人的负担
"懂事的人最累"

【第3页】越是【在乎】的人
越不想说
因为怕说出口
反而【让你为难】
"我的逞强是给你的温柔"

【第4页】"没事"的背后
藏着【无数次】深呼吸
和【自我说服】的挣扎
还有不想被看穿的倔强
"我的情绪只在深夜上线"

【第5页】下次双子说【没事】
请多问【一句】
或者什么都别问
就默默陪着就好
"沉默有时比话语更温暖"

【结尾】写给双子
你不必总是【逞强】
偶尔说"有事"也没关系
愿有人懂你的【言不由衷】

愿你的脆弱
被温柔接住'''
    },
    {
        'record_id': 'recv899UDj3mZC',
        'title': '双子座【恋爱】前后\n判若两人',
        'subtitle': '反差感拉满',
        'content': '''【封面】双子座恋爱前后判若两人

【第1页】恋爱【之前】
高冷 神秘 若即若离
让人【捉摸不透】
永远保持安全距离
"靠近我可以 但别想读懂我"

【第2页】恋爱【之后】
黏人 话多 患得患失
【反差】大到自己都害怕
怎么变成这样了
"遇见你之后 我认不出自己"

【第3页】【没确定】关系时
理智在线 进退自如
一旦【动了真心】
智商立刻下线
"心动的瞬间 理智已离家出走"

【第4页】以前觉得【独处】最舒服
现在只想和你【腻在一起】
以前回消息看心情
现在秒回都嫌慢
"我的时间观因你而改变"

【第5页】双子的【反差】
不是人格分裂
是【认定】了你
才愿意卸下所有伪装
"我的所有反差 都是因为你"

【结尾】写给双子
你不是【善变】
只是太会【保护】自己
认定了才敢全部交出

愿你遇到
值得变化的人'''
    },
    {
        'record_id': 'recv899VbC6njH',
        'title': '双子座【吃醋】的样子\n嘴上说不介意',
        'subtitle': '口是心非代言人',
        'content': '''【封面】双子座吃醋的样子嘴上说不介意

【第1页】"我【不介意】"
是双子最大的【谎言】
说出口的时候
心里已经酸成柠檬
"我的嘴和心从来不同步"

【第2页】表面【风轻云淡】
"你随便啊"
实际内心【翻涌】
已经开始脑补一百种剧情
"我的大度都是装的"

【第3页】吃醋的双子
不会【直说】
只会变得【话少】
或者突然变得很忙
"我的沉默是无声的吃醋"

【第4页】如果开始【阴阳怪气】
"哦 挺好的"
恭喜你踩中了【雷区】
但双子死都不会承认
"我的语气已经说明一切"

【第5页】其实双子的【醋】
是【在乎】的证明
不在乎的人
连吃醋的资格都没有
"我的醋意只为你而泡"

【结尾】写给双子
承认【吃醋】不丢人
喜欢一个人【本就如此】
别总是嘴硬心软

愿你的在乎
被认真对待'''
    },
    {
        'record_id': 'recv899VPEIglx',
        'title': '双子座的【职场】人格\n上班和下班不是一个人',
        'subtitle': '职场变色龙',
        'content': '''【封面】双子座的职场人格上班和下班不是一个人

【第1页】【上班】的双子
专业 高效 逻辑清晰
【气场】全开
仿佛什么都能搞定
"工作中的我就是这么能打"

【第2页】【下班】的双子
废物 躺平 只想发呆
能不说话就【不说话】
社交能量已清零
"下班后的我 请勿打扰"

【第3页】开会的时候【侃侃而谈】
下班后【一句话】都不想说
不是双重人格
是【社交电量】用光了
"工作和生活 是两个我"

【第4页】工作中【专业靠谱】
生活里【随性散漫】
同事以为你很强
朋友知道你【很废】
"没人能同时看到两个我"

【第5页】这就是双子的【生存法则】
工作是【演出】
下班才是真实的自己
两个人格和谐共处
"我的分裂有益身心健康"

【结尾】写给双子
你不必【全天候】都完美
允许自己【切换模式】
工作和生活都是你

愿你上班有气场
下班能躺平'''
    },
    {
        'record_id': 'recv899WiDh06f',
        'title': '双子座【灵感】来了\n谁也挡不住',
        'subtitle': '创意爆发体质',
        'content': '''【封面】双子座灵感来了谁也挡不住

【第1页】灵感【来的时候】
挡都挡不住
凌晨三点也要【爬起来】
不记下来会死
"灵感不等人 我也不等天亮"

【第2页】那种【脑子】里
突然【炸开烟花】的感觉
必须立刻动手
过了这村就没这店
"我的脑洞不讲道理"

【第3页】【专注】起来的双子
六亲不认
手机不看 饭不吃
【沉浸】在自己的世界里
"别打扰我 我在创造"

【第4页】但灵感这东西
【来去无踪】
上一秒还在【爆发】
下一秒可能就摸鱼去了
"我的创造力也随机播放"

【第5页】所以双子【趁热打铁】
是对灵感最大的【尊重】
因为谁也不知道
下一次是什么时候
"灵感珍贵 不容辜负"

【结尾】写给双子
你的【灵感】是天赋
珍惜每一次【爆发】
然后勇敢创造

愿你的脑洞
永远精彩'''
    },
    {
        'record_id': 'recv899WOgurzK',
        'title': '2026双子座【翻身】的一年\n好运终于来了',
        'subtitle': '转运年份指南',
        'content': '''【封面】2026双子座翻身的一年好运终于来了

【第1页】【2026】对双子
是【转运】的一年
前几年积攒的努力
终于要开花结果
"该来的终于来了"

【第2页】事业上会有【突破】
之前卡住的项目
今年【顺利推进】
贵人运也在上升
"机会已经在路上"

【第3页】感情方面【明朗】
单身的有机会【脱单】
有对象的感情稳定
暧昧不清的会有答案
"该来的人会来"

【第4页】财运【稳步上升】
不是一夜暴富
是【持续进账】的踏实感
钱包慢慢鼓起来
"稳稳的幸福 最踏实"

【第5页】最重要的是【心态】
经历过低谷
才懂得【珍惜】好运
这一年会越来越自信
"低谷是为了蹬得更高"

【结尾】写给双子
你的【好运】不是偶然
是【努力】的回报
2026大胆往前冲

愿你翻身成功
光芒万丈'''
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
