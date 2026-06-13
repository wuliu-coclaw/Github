import requests, json, os
from PIL import Image

# ====== 配置 ======
APP_ID = 'wxaaaa5d87952b5648'
APP_SECRET = '8cdd2ca18d73b5c25bbf4b36ce9f40a1'
BASE_DIR = r'D:\AutoClaw-Pro\Marketing-writer\sites\wuliu-coclaw\articles\wechat'

# ====== Step 1: 获取token ======
print('>>> 获取access_token...')
params = {'grant_type': 'client_credential', 'appid': APP_ID, 'secret': APP_SECRET}
r = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=params)
token_data = r.json()
if 'access_token' not in token_data:
    print(f'获取token失败: {token_data}')
    exit(1)
token = token_data['access_token']
print(f'>>> token OK')

# ====== Step 2: 处理封面图(900x600) ======
print('>>> 处理封面图...')
# 使用AI生成的封面图
cover_src = os.path.join(BASE_DIR, 'images', 'cover_04_raw.png')
cover_jpg = os.path.join(BASE_DIR, 'images', 'cover_04.jpg')
img = Image.open(cover_src)
img = img.resize((900, 600), Image.LANCZOS)
img.save(cover_jpg, 'JPEG', quality=85)
print(f'>>> 封面图已保存: {cover_jpg}')

# ====== Step 3: 上传封面到微信素材库 ======
print('>>> 上传封面图...')
with open(cover_jpg, 'rb') as f:
    r2 = requests.post(
        'https://api.weixin.qq.com/cgi-bin/material/add_material',
        params={'access_token': token, 'type': 'image'},
        files={'media': ('cover_04.jpg', f, 'image/jpeg')}
    )
cover_result = r2.json()
if 'media_id' not in cover_result:
    print(f'上传封面失败: {cover_result}')
    exit(1)
thumb_id = cover_result['media_id']
print(f'>>> 封面上传成功, media_id: {thumb_id}')

# ====== Step 4: 上传正文配图(uploadimg接口返回URL) ======
print('>>> 上传正文配图...')
image_files = [
    'cover_04_raw.png',
    'image6_space_comparison.png',
    'image7_path_planning.png'
]
image_urls = {}
for img_name in image_files:
    img_path = os.path.join(BASE_DIR, 'images', img_name)
    if not os.path.exists(img_path):
        print(f'>>> 跳过不存在的图片: {img_name}')
        continue
    # 压缩到合理大小
    img_pil = Image.open(img_path)
    img_pil = img_pil.resize((900, 600), Image.LANCZOS)
    compressed_path = os.path.join(BASE_DIR, 'images', img_name.replace('.png', '_compressed.jpg'))
    img_pil.save(compressed_path, 'JPEG', quality=85)
    with open(compressed_path, 'rb') as f:
        r_img = requests.post(
            'https://api.weixin.qq.com/cgi-bin/media/uploadimg',
            params={'access_token': token},
            files={'media': (img_name, f, 'image/jpeg')}
        )
    img_result = r_img.json()
    if 'url' in img_result:
        image_urls[img_name] = img_result['url']
        print(f'>>> {img_name} 上传成功: {img_result["url"][:60]}...')
    else:
        print(f'>>> {img_name} 上传失败: {img_result}')

print(f'>>> 共上传 {len(image_urls)} 张正文配图')

# ====== Step 5: 读取HTML内容 ======
print('>>> 读取文章内容...')
html_path = os.path.join(BASE_DIR, '04_four_way_shuttle_wechat.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 提取body内的内容
import re
body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
if body_match:
    content = body_match.group(1).strip()
else:
    content = html_content

print(f'>>> 文章内容长度: {len(content)} 字符')

# ====== Step 6: 替换图片URL ======
print('>>> 替换图片URL...')
for img_name, url in image_urls.items():
    content = content.replace(f'src="images/{img_name}"', f'src="{url}"')

# ====== Step 7: 创建草稿 ======
print('>>> 创建草稿...')
article = {
    "title": "四向穿梭车效率翻倍的5个秘密",
    "author": "毅哥说物流",
    "digest": "别看单机速度，看系统吞吐。5个实战秘密帮你把仓库效率翻倍。",
    "content": content,
    "content_source_url": "",
    "thumb_media_id": thumb_id,
    "need_open_comment": 1,
    "only_fans_can_comment": 0
}

data = json.dumps({"articles": [article]}, ensure_ascii=False).encode('utf-8')
r3 = requests.post(
    'https://api.weixin.qq.com/cgi-bin/draft/add',
    params={'access_token': token},
    data=data,
    headers={'Content-Type': 'application/json; charset=utf-8'}
)
draft_result = r3.json()
if 'media_id' in draft_result:
    print(f'>>> 草稿创建成功! media_id: {draft_result["media_id"]}')
    print(f'>>> 请登录公众号后台查看并发布')
else:
    print(f'>>> 草稿创建失败: {draft_result}')
