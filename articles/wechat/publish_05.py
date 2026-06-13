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
cover_src = os.path.join(BASE_DIR, 'cover_05.png')
cover_jpg = os.path.join(BASE_DIR, 'cover_05.jpg')
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
        files={'media': ('cover_05.jpg', f, 'image/jpeg')}
    )
cover_result = r2.json()
if 'media_id' not in cover_result:
    print(f'上传封面失败: {cover_result}')
    exit(1)
thumb_id = cover_result['media_id']
print(f'>>> 封面上传成功, media_id: {thumb_id}')

# ====== Step 4: 读取HTML内容 ======
print('>>> 读取文章内容...')
html_path = os.path.join(BASE_DIR, '05_pharma_warehouse_data_wechat.html')
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

# ====== Step 5: 创建草稿 ======
print('>>> 创建草稿...')
article = {
    "title": "年出库500万件、人均效率差一倍，你的仓库在第几层？",
    "author": "毅哥说物流",
    "digest": "一个医药物流中心的真实运营数据，看完就知道差距在哪。",
    "content": content,
    "content_source_url": "https://wuliu-coclaw.github.io/Github/articles/05_pharma_warehouse_data.html",
    "thumb_media_id": thumb_id,
    "need_open_comment": 1,
    "only_fans_can_comment": 0
}

# 标题检查：不超过34字节（UTF-8）
title_bytes = len(article["title"].encode('utf-8'))
print(f'>>> 标题字节数: {title_bytes}')
if title_bytes > 34:
    print(f'警告: 标题超过34字节! 当前{title_bytes}字节')
    # 缩短标题
    article["title"] = "年出库500万件，你的仓库在第几层？"
    print(f'>>> 缩短后: {article["title"]} ({len(article["title"].encode("utf-8"))}字节)')

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
