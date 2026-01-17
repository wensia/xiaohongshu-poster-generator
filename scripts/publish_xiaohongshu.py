#!/usr/bin/env python3
"""
小红书笔记发布脚本
使用持久化用户数据目录，登录一次后会保持登录状态
"""

import asyncio
import sys
import os
from pathlib import Path

# 确保可以导入 playwright
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("请先安装 playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

# 配置
USER_DATA_DIR = os.path.expanduser("~/.xiaohongshu-browser")
HEADLESS = False  # 设为 True 可以无头运行（登录后）


async def publish_note(title: str, content: str, image_paths: list[str]):
    """发布小红书笔记"""

    async with async_playwright() as p:
        # 使用持久化上下文，保持登录状态
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=HEADLESS,
            viewport={"width": 1280, "height": 900},
            locale="zh-CN",
        )

        page = context.pages[0] if context.pages else await context.new_page()

        try:
            # 1. 导航到发布页面
            print("正在打开小红书创作者中心...")
            await page.goto("https://creator.xiaohongshu.com/publish/publish?source=official")
            await page.wait_for_timeout(3000)

            # 检查是否需要登录
            if "login" in page.url:
                print("\n⚠️  需要登录！请在浏览器中扫码登录，登录后按 Enter 继续...")
                input()
                await page.wait_for_timeout(2000)

            # 2. 点击"上传图文"
            print("选择上传图文...")
            await page.evaluate("""() => {
                const elements = document.querySelectorAll('div, span');
                for (const el of elements) {
                    if (el.textContent === '上传图文' && el.textContent.length < 10) {
                        el.click();
                        break;
                    }
                }
            }""")
            await page.wait_for_timeout(2000)

            # 3. 上传图片
            print(f"上传 {len(image_paths)} 张图片...")
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(image_paths)
                print("图片上传中，请等待...")
                await page.wait_for_timeout(10000)  # 等待上传完成
            else:
                print("❌ 未找到文件上传输入框")
                return False

            # 4. 填写标题
            print(f"填写标题: {title[:20]}...")
            title_input = await page.query_selector('input[placeholder*="标题"]')
            if title_input:
                await title_input.fill(title)
            else:
                # 尝试其他选择器
                title_input = await page.query_selector('.title-input input')
                if title_input:
                    await title_input.fill(title)

            await page.wait_for_timeout(500)

            # 5. 填写正文
            print("填写正文...")
            # 尝试多种选择器
            content_area = await page.query_selector('[contenteditable="true"]')
            if not content_area:
                content_area = await page.query_selector('.ql-editor')
            if not content_area:
                content_area = await page.query_selector('div[data-placeholder]')

            if content_area:
                await content_area.click()
                await page.wait_for_timeout(300)
                # 使用键盘输入以支持换行
                await content_area.fill(content)
            else:
                print("⚠️  未找到正文输入框，请手动填写")

            await page.wait_for_timeout(1000)

            # 6. 截图确认
            screenshot_path = "/tmp/xiaohongshu_preview.png"
            await page.screenshot(path=screenshot_path)
            print(f"预览截图已保存: {screenshot_path}")

            # 7. 询问是否发布
            print("\n✅ 内容已填写完成！")
            print("请检查浏览器中的预览，确认无误后：")
            confirm = input("输入 'y' 发布，输入其他取消: ")

            if confirm.lower() == 'y':
                # 点击发布按钮
                publish_btn = await page.query_selector('button:has-text("发布")')
                if publish_btn:
                    await publish_btn.click()
                    print("正在发布...")
                    await page.wait_for_timeout(5000)

                    if "success" in page.url:
                        print("🎉 发布成功！")
                        return True
                    else:
                        print(f"发布状态未知，当前URL: {page.url}")
                else:
                    print("❌ 未找到发布按钮")
            else:
                print("已取消发布")

            return False

        except Exception as e:
            print(f"❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            # 保持浏览器打开一会儿以便查看结果
            await page.wait_for_timeout(3000)
            await context.close()


async def main():
    # 笔记内容
    title = "射手座的生理性依赖：不粘则已，粘了恨不得天天见"

    content = """射手座的「生理性依赖」是什么？

就是平时爱自由、独来独往，
但对你，想放弃所有远方。

不是没有自己的世界，
是你成了我世界的中心。

遇到了，我会收起翅膀。
遇不到，我继续浪迹天涯。

如果射手开始天天找你、什么事都想拉着你，
那不是闲，是把自由都给你了。

#射手座 #星座 #生理性依赖 #反差萌"""

    # 图片路径
    image_dir = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/17/射手座的生理性依赖"
    image_paths = [
        f"{image_dir}/01_cover.png",
        f"{image_dir}/02_page.png",
        f"{image_dir}/03_page.png",
        f"{image_dir}/04_page.png",
        f"{image_dir}/05_page.png",
        f"{image_dir}/06_page.png",
        f"{image_dir}/07_end.png",
    ]

    # 验证图片存在
    for path in image_paths:
        if not os.path.exists(path):
            print(f"❌ 图片不存在: {path}")
            return

    print("=" * 50)
    print("小红书笔记发布工具")
    print("=" * 50)
    print(f"标题: {title}")
    print(f"图片: {len(image_paths)} 张")
    print("=" * 50)

    await publish_note(title, content, image_paths)


if __name__ == "__main__":
    asyncio.run(main())
