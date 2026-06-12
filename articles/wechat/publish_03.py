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
cover_src = os.path.join(BASE_DIR, 'images', 'image1_warehouse_sorting_v2.png')
cover_jpg = os.path.join(BASE_DIR, 'images', 'cover_03.jpg')
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
        files={'media': ('cover.jpg', f, 'image/jpeg')}
    )
cover_result = r2.json()
if 'media_id' not in cover_result:
    print(f'上传封面失败: {cover_result}')
    exit(1)
thumb_id = cover_result['media_id']
print(f'>>> 封面上传成功, media_id: {thumb_id}')

# ====== Step 4: 上传5张正文图到微信(uploadimg接口返回URL) ======
print('>>> 上传正文配图...')
image_files = [
    'image1_warehouse_sorting_v2.png',
    'image2_dispatch_center_v2.png',
    'image3_meeting_presentation.png',
    'image4_logistics_center_panorama.png',
    'image5_agv_robots_v2.png'
]
image_urls = {}
for img_name in image_files:
    img_path = os.path.join(BASE_DIR, 'images', img_name)
    # 压缩到合理大小
    img_pil = Image.open(img_path)
    img_pil = img_pil.resize((900, 600), Image.LANCZOS)
    compressed_path = os.path.join(BASE_DIR, 'images', img_name.replace('.png', '_compressed.jpg'))
    img_pil.save(compressed_path, 'JPEG', quality=85)
    
    with open(compressed_path, 'rb') as f:
        r3 = requests.post(
            'https://api.weixin.qq.com/cgi-bin/media/uploadimg',
            params={'access_token': token},
            files={'media': (img_name, f, 'image/jpeg')}
        )
    result = r3.json()
    if 'url' in result:
        image_urls[img_name] = result['url']
        print(f'  {img_name} -> OK')
    else:
        print(f'  {img_name} -> FAIL: {result}')
        image_urls[img_name] = ''

# ====== Step 5: 构建HTML内容 ======
print('>>> 构建HTML内容...')

def img_tag(key, alt):
    url = image_urls.get(key, '')
    if url:
        return f'<p style="text-align:center;margin:25px 0;"><img src="{url}" alt="{alt}" style="max-width:100%;border-radius:8px;"/></p>'
    return ''

content = '''<p>干了25年物流，从月薪3000的基层仓管，一路做到管几百人的物流VP。</p>
<p>这条路上，我踩过坑、走过弯路，也见过太多人卡在某个阶段上不去。今天不讲大道理，就聊聊每个阶段的薪资天花板在哪，怎么突破。</p>
<hr/>
<p style="font-size:18px;font-weight:bold;color:#2ab4d8;">第一阶段，月薪3000-5000，干1到3年</p>
<p>你可能是仓管、拣货员、叉车司机、调度助理。干的都是执行层的活，重复、体力、枯燥。</p>
<p>很多人觉得物流就是搬箱子、开车、记账，干一辈子也就这样。</p>
<p><strong>错了。</strong></p>
<p>物流的本质是供应链管理。你今天搬的每一个箱子，背后都是库存策略、订单路由、成本优化。只不过你现在看到的只是最后一公里。</p>
<p>这个阶段的天花板不是能力，是认知。</p>
<p>我刚入行的时候，每天在仓库里搬货。但我多做了一件事：每次搬完货，我都记下来这批货的流向。从哪来，到哪去，走的什么路线，用了多长时间。</p>
<p>三个月后，我比主管还清楚仓库的货物流动规律。</p>
<p>这就是我第一次涨薪的原因。不是因为我搬得快，是因为我知道为什么要这么搬。</p>
<p>那怎么突破呢？</p>
<p>搞懂你搬的箱子。这批货从哪来？到哪去？为什么这么走？搞懂流程，你就不再是搬箱子的。</p>
<p>学会用系统。WMS、TMS、ERP，哪怕你现在用不上，也要了解。系统是物流的神经网络，不懂系统的人，永远只能干体力活。</p>
<p>考个证。物流师、供应链管理师，不值钱，但能帮你敲门。证书不能代表能力，但能代表态度。</p>
''' + img_tag('image1_warehouse_sorting_v2.png', '仓库分拣线') + '''
<hr/>
<p style="font-size:18px;font-weight:bold;color:#2ab4d8;">第二阶段，月薪5000-10000，干3到5年</p>
<p>你现在可能是仓经理、调度主管、物流专员。开始带团队、管流程、扛KPI了。</p>
<p>这个阶段的天花板是什么？</p>
<p><strong>系统思维。</strong></p>
<p>很多人在这个阶段干得很好，但只会管自己的一亩三分地。仓库管得好，但不知道运输怎么回事；调度做得好，但不懂成本怎么算。</p>
<p>物流是一条链。你只懂一个环节，就只能当一个环节的螺丝钉。</p>
<p>我在仓经理岗位干了两年，主动申请去管运输。领导觉得我疯了。仓库管得好好的，干嘛去运输？</p>
<p>但正是这个决定，让我后来有机会管整个物流中心。</p>
<p>因为领导发现：这个人懂仓库、懂运输、能算账、能带团队。这才是VP的苗子。</p>
<p>那怎么突破呢？</p>
<p>横向扩展。主动参与其他环节的项目。仓库的去了解运输，运输的去了解仓储。物流是一条链，你得懂全链。</p>
<p>学会算账。物流的核心是成本。你得知道一单货的运输成本、仓储成本、人工成本分别是多少。会算账的人，才有资格谈优化。</p>
<p>带出一个能打的团队。你一个人干得再好，也不如带出5个能干的人。学会授权、培训、激励。</p>
''' + img_tag('image2_dispatch_center_v2.png', '物流调度中心') + '''
<hr/>
<p style="font-size:18px;font-weight:bold;color:#2ab4d8;">第三阶段，月薪10000-20000，干5到10年</p>
<p>你可能是物流经理、区域物流负责人、供应链经理。开始参与战略决策、对接高层、管理多个团队。</p>
<p>这个阶段的天花板是什么？</p>
<p><strong>商业思维。</strong></p>
<p>很多人在这个阶段卡住了，因为只会做事，不会想事。能管好一个仓，但不知道这个仓在公司战略里是什么位置。</p>
<p>我在这个阶段干了五年，最大的突破是学会了一件事：用CEO的视角看物流。</p>
<p>以前我汇报，只说仓库效率提升了多少。</p>
<p>后来我汇报，说物流成本降低了多少、客户满意度提升了多少、对公司利润贡献了多少。</p>
<p>同样的工作，不同的讲法，效果天差地别。</p>
<p>那怎么突破呢？</p>
<p>理解业务。物流不是独立存在的，它是业务的一部分。你得知道公司的业务模式、客户是谁、利润在哪。物流怎么支撑业务？这才是高层想听的。</p>
<p>学会汇报。干得好不如说得好。这不是教你吹牛，是教你用数据、用案例、用故事，把你的价值讲清楚。</p>
<p>建立行业人脉。参加行业会议、加入物流协会、认识同行。信息差就是机会差。</p>
''' + img_tag('image3_meeting_presentation.png', '会议汇报') + '''
<hr/>
<p style="font-size:18px;font-weight:bold;color:#2ab4d8;">第四阶段，月薪20000-30000，干10到15年</p>
<p>你可能是物流总监、供应链总监、VP。开始参与公司战略、管理几十上百人、对P&L负责。</p>
<p>这个阶段的天花板是什么？</p>
<p><strong>格局。</strong></p>
<p>很多人在这个阶段止步，因为只会管物流，不会管公司。物流总监和VP的区别，不在于谁更懂物流，而在于谁更懂公司。</p>
<p>我做VP时，最大的感悟是：物流管理的本质不是管流程，而是管人。</p>
<p>流程可以标准化，但人不能。你得让几百号人愿意干活、会干活、干好活。这需要的不是物流专业知识，是领导力。</p>
<p>那怎么突破呢？</p>
<p>理解公司战略。物流在公司战略里是什么角色？是成本中心还是利润中心？你的老板怎么想？理解战略，才能对齐目标。</p>
<p>培养接班人。你得有人能接你的班，你才能往上走。培养接班人，不是削弱自己，是放大自己。</p>
<p>跨界学习。财务、营销、人力，你不需要精通，但需要懂。VP是通才，不是专才。</p>
''' + img_tag('image4_logistics_center_panorama.png', '物流中心全景') + '''
<hr/>
<p style="font-size:18px;font-weight:bold;color:#2ab4d8;">第五阶段，月薪30000以上，干15年以上</p>
<p>你可能是VP、COO、创业者。你的价值不再是"懂物流"，而是"懂商业"。</p>
<p>到了这个层级，没有标准答案，没有前人经验，你得自己趟路。能走多远，取决于你的视野、格局、魄力。</p>
<p>这个阶段的天花板是什么？</p>
<p><strong>你自己。</strong></p>
<p>保持学习。行业在变，技术在变，你不学就退。AI、自动化、数字化，这些不是趋势，是现实。我身边有太多老物流人，因为不愿意学新技术，被年轻人替代了。</p>
<p>敢于决策。高层的价值不是做正确的事，是在不确定中做决策。敢于拍板，敢于承担。</p>
<p>回馈行业。你有25年的经验，不分享出来太可惜。写文章、做培训、带新人。这是对行业最好的回报。</p>
''' + img_tag('image5_agv_robots_v2.png', 'AGV机器人') + '''
<hr/>
<p style="font-size:18px;font-weight:bold;color:#2ab4d8;">写在最后</p>
<p>物流这条路，没有捷径，但有方法。</p>
<p>我用25年走完了这条路，希望我的经验能帮你少走几年弯路。</p>
<p>你在哪个阶段？卡在什么地方？评论区聊聊，毅哥帮你分析分析。</p>
<hr/>
<p style="font-size:14px;color:#999;">毅哥说物流 | 20多年医药物流全链路实战专家<br/>聚焦于医药生产工艺优化、医药企业信息化咨询及绿色能源改造升级<br/>致力于用AI与数字技术驱动医药企业精益增长<br/>更多干货，关注：<a href="https://wuliu-coclaw.github.io/Github/" style="color:#2ab4d8;text-decoration:none;">https://wuliu-coclaw.github.io/Github/</a></p>
<p style="font-size:12px;color:#999;">数据来源说明：本文薪资数据基于行业调研报告及作者25年从业经验，具体薪资因地区、企业规模、个人能力等因素存在差异，仅供参考。</p>'''

# ====== Step 6: 创建草稿 ======
print('>>> 创建草稿...')
body = {
    'articles': [{
        'title': '物流人月薪3000到30000，每个阶段怎么突破？',
        'author': '毅哥说物流',
        'digest': '干了25年物流，从月薪3000的基层仓管，一路做到管几百人的物流VP。每个阶段的薪资天花板在哪，怎么突破？',
        'content': content,
        'thumb_media_id': thumb_id,
        'need_open_comment': 1,
        'only_fans_can_comment': 0
    }]
}

json_str = json.dumps(body, ensure_ascii=False)
headers = {'Content-Type': 'application/json; charset=utf-8'}
r4 = requests.post(
    'https://api.weixin.qq.com/cgi-bin/draft/add',
    params={'access_token': token},
    data=json_str.encode('utf-8'),
    headers=headers
)
draft_result = r4.json()

if 'media_id' in draft_result:
    print(f'')
    print(f'========================================')
    print(f'  草稿创建成功!')
    print(f'  media_id: {draft_result["media_id"]}')
    print(f'  请到公众号后台 -> 草稿箱 发布')
    print(f'========================================')
else:
    print(f'草稿创建失败: {draft_result}')
