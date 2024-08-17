import pygame
import random
import sys
import requests
from lxml import html, etree
from io import BytesIO

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置字体和大小
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 定义常用词列表
words = {
    "苹果": "apple",
    "香蕉": "banana",
    "橘子": "orange",
    "草莓": "strawberry",
    "葡萄": "grape",
    "西瓜": "watermelon"
}

# 随机选择一个词
def get_random_word():
    return random.choice(list(words.items()))

# 显示文本在屏幕上
def draw_text(surface, text, color, pos):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

# 从 Bing 搜索获取图片
def fetch_image_from_bing(query):
    search_url = f"https://cn.bing.com/images/search?q={query}&form=HDRSC2&first=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()  # 如果请求失败，会抛出异常

    # 解析 HTML 内容
    tree = html.fromstring(response.content)

    # 打印整个 HTML 文档（调试用）
    # html_string = etree.tostring(tree, pretty_print=True, encoding='unicode')
    # print(html_string)

    # 使用正则表达式查找图片 URL
    img_tags = tree.xpath('//img[contains(@class, "mimg")]/@src')
    if img_tags:
        img_url = img_tags[0]
        if img_url.startswith("//"):
            img_url = "http:" + img_url
        response = requests.get(img_url)
        return pygame.image.load(BytesIO(response.content))
    return None

# 主程序
def main():
    current_word, current_translation = get_random_word()
    input_text = ""
    show_image = False
    image_surface = None

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    input_text = ""
                    current_word, current_translation = get_random_word()
                    show_image = False
                    image_surface = None
                else:
                    input_text += event.unicode

                if input_text.lower() == current_translation:
                    if not show_image:
                        prompt = f"{current_translation}"
                        image_surface = fetch_image_from_bing(prompt)
                        show_image = True

        # 显示中文
        draw_text(screen, current_word, BLACK, (50, 150))

        # 显示用户输入的文本
        for i, letter in enumerate(current_translation):
            if i < len(input_text):
                color = GREEN if input_text[i].lower() == letter else RED
            else:
                color = BLACK
            draw_text(screen, letter, color, (50 + i * 50, 250))

        # 如果用户成功输入全部字母，则显示图片
        if show_image and image_surface:
            screen.blit(image_surface, (50, 350))
            draw_text(screen, "按 Enter 继续", BLACK, (50, 500))

        pygame.display.flip()

if __name__ == "__main__":
    main()
