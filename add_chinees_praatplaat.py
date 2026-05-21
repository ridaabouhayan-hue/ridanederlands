import re
import json

filepath = r"g:\Mijn Drive\HTML FILES\praatplaat.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Chinese button
flag_btn_str = '<button class="flag-btn" onclick="switchLanguage(\'ps\')" title="پښتو">🇦🇫 PS</button>'
flag_btn_zh = '<button class="flag-btn" onclick="switchLanguage(\'ps\')" title="پښتو">🇦🇫 PS</button>\n                        <button class="flag-btn" onclick="switchLanguage(\'zh\')" title="中文">🇨🇳 ZH</button>'
content = content.replace(flag_btn_str, flag_btn_zh)

flag_btn_str2 = '<button class="flag-btn" onclick="switchLanguage(\'ps\')" title="پښتو">🇦🇫 PS</button>'
# Wait, it's indent dependent. I'll just replace all occurrences:
content = content.replace(
    '<button class="flag-btn" onclick="switchLanguage(\'ps\')" title="پښتو">🇦🇫 PS</button>',
    '<button class="flag-btn" onclick="switchLanguage(\'ps\')" title="پښتو">🇦🇫 PS</button>\n                    <button class="flag-btn" onclick="switchLanguage(\'zh\')" title="中文">🇨🇳 ZH</button>'
)

# 2. Inject `zh` to `translations` object
zh_translation_block = """            },
            zh: {
                instructionsTitle: "它是如何工作的？(逐步)",
                step1Title: "选择一个主题",
                step1Desc: "点击下面你想练习的主题。",
                step2Title: "组建一个小组",
                step2Desc: "两人(2)或三人(3)一组合作。",
                step3Title: "练习对话",
                step3Desc: "一起交谈至少1分钟。互相问问题。问题和示例对话只是一个指南(帮助)，而不是面试！",
                step4Title: "录音并发送",
                step4Desc: "用手机录下你们的对话。通过WhatsApp将录音发送给老师！",
                selectTopic: "选择一个话题",
                backNav: "回到所有主题",
                roleTitle: "你是谁？点击一个角色来集中注意力：",
                roleAll: "一起练习(显示全部)",
                roleA: "🔵 我是学生A",
                roleB: "🟠 我是学生B",
                questionsHeader: "问这些问题(指南)",
                exampleHeader: "示例对话",
                helperHeader: "句子结构和词汇",
                helperStarters: "句子结构(起始句)：",
                helperVocab: "有用的词汇(词汇表)：",
                whatsappHeader: "练习完了？录下对话！",
                whatsappDesc: "用手机的录音机录下你们的对话。然后点击绿色按钮，通过WhatsApp将录音发给老师！",
                whatsappBtn: "打开WhatsApp并将录音发给老师",
                speedLabel: "说话速度：",
                speedSlow: "慢",
                speedNormal: "正常",
                notebookHeader: "现在轮到你了！编写你们自己的对话",
                notebookDesc: "填写你们的名字，写下你们自己的对话。使用问题和词汇！",
                labelNameA: "学生A的名字 (🔵)：",
                labelNameB: "学生B的名字 (🟠)：",
                placeholderA: "在这里输入学生A的句子...",
                placeholderB: "在这里输入学生B的句子...",
                chipsLabel: "💡 点击下面的提示来使用：",
                notebookSendBtn: "通过WhatsApp将对话发给老师",
                notebookClearBtn: "清除全部"
            }"""

if 'zh: {' not in content:
    content = content.replace(
        'notebookClearBtn: "ټول پاک کړئ"\n            }',
        'notebookClearBtn: "ټول پاک کړئ"\n' + zh_translation_block
    )

# 3. Translate themesData
translations_dict = {
  "I watch a movie. Or I cook. Do you have a hobby?": "我看电影。或者我做饭。你有爱好吗？",
  "Where do you live now?": "你现在住在哪里？",
  "bicycle / bus": "自行车 / 公交车",
  "I come from the Netherlands. Which language do you speak?": "我来自荷兰。你会说什么语言？",
  "Where do you buy food?": "你在哪里买食物？",
  "My name is ...": "我的名字是 ...",
  "I live in a ...": "我住在一个 ...",
  "My name is Jan. Where do you come from?": "我叫Jan。你来自哪里？",
  "I visit family. Or friends. And you?": "我拜访家人。或者朋友。你呢？",
  "I live with my husband and two children. And you?": "我和我的丈夫还有两个孩子住在一起。你呢？",
  "What time do you get up?": "你几点起床？",
  "In the evening I watch TV or learn Dutch. What time do you go to sleep?": "晚上我看电视或学习荷兰语。你几点睡觉？",
  "What do you do in your free time?": "你在空闲时间做什么？",
  "Do you have children?": "你有孩子吗？",
  "What are you eating tonight?": "你今晚吃什么？",
  "I live in an apartment. And you?": "我住在一间公寓里。你呢？",
  "In the morning I drink ...": "早上我喝 ...",
  "Who do you live with?": "你和谁住在一起？",
  "I always go to school by bicycle. And how do you travel?": "我总是骑自行车去学校。你怎么去？",
  "sport / hobby": "运动 / 爱好",
  "No, my husband cooks. I do the groceries.": "不，我丈夫做饭。我买杂货。",
  "Do you like to walk?": "你喜欢散步吗？",
  "I eat yogurt. How do you go to school?": "我吃酸奶。你怎么去学校？",
  "I go by bus. What do you usually do in the evening?": "我坐公交车。你晚上通常做什么？",
  "I go to sleep at ... o'clock.": "我...点睡觉。",
  "What time do you eat hot dinner?": "你几点吃热晚餐？",
  "breakfast / food": "早餐 / 食物",
  "language / languages": "语言 / 语言",
  "Hello, what is your name?": "你好，你叫什么名字？",
  "I live alone. Is your neighborhood nice?": "我一个人住。你的社区好吗？",
  "breakfast / dinner": "早餐 / 晚餐",
  "I speak Arabic. And a little Dutch. And you?": "我说阿拉伯语。还有一点荷兰语。你呢？",
  "What music do you like?": "你喜欢什么音乐？",
  "My neighborhood is also nice. The forest is nearby.": "我的社区也很好。森林就在附近。",
  "I live in Utrecht. And you?": "我住在乌得勒支。你呢？",
  "to read / book": "阅读 / 书",
  "country / city": "国家 / 城市",
  "to live / address": "居住 / 地址",
  "Sleep well already for later!": "提前祝你晚安！",
  "walking / outside": "散步 / 外面",
  "I come from Syria. And you?": "我来自叙利亚。你呢？",
  "I get up at ... o'clock.": "我...点起床。",
  "Is your house nice?": "你的房子好吗？",
  "I don't like ...": "我不喜欢 ...",
  "What do you eat in the morning?": "你早上吃什么？",
  "I speak ...": "我说 ...",
  "I go to sleep early, around 10 o'clock. And you?": "我睡得很早，大概10点。你呢？",
  "For breakfast I eat ...": "我早餐吃 ...",
  "Yes, it is quiet. There is a park nearby. And your neighborhood?": "是的，很安静。附近有个公园。你的社区呢？",
  "kitchen / bathroom": "厨房 / 浴室",
  "I get up at 6 o'clock. What do you eat for breakfast?": "我6点起床。你早餐吃什么？",
  "I buy food in ...": "我在...买食物。",
  "Do you like to watch TV?": "你喜欢看电视吗？",
  "Which language do you speak?": "你会说什么语言？",
  "Yes, I have a balcony. Is your garden big?": "是的，我有一个阳台。你的花园大吗？",
  "On the weekend I go to ...": "周末我去 ...",
  "Yes, I cook every day. Do you cook too?": "是的，我每天都做饭。你也做饭吗？",
  "Do you have a garden or a balcony?": "你有一个花园还是一个阳台？",
  "I eat bread with cheese. And you?": "我吃面包加奶酪。你呢？",
  "My house has ... rooms.": "我的房子有...个房间。",
  "Nice!": "真好！",
  "Bye Jan! Goodbye.": "再见Jan！再见。",
  "No, the garden is small. Who do you live with?": "不，花园很小。你和谁住在一起？",
  "music / listening": "音乐 / 听",
  "apartment / house": "公寓 / 房子",
  "Which room do you like?": "你喜欢哪个房间？",
  "I live with ...": "我和...住在一起。",
  "Yes, I work in the garden. That is fun.": "是的，我在花园里干活。那很有趣。",
  "I live in Zeist. Nice to meet you!": "我住在Zeist。很高兴见到你！",
  "You too, Jan! See you tomorrow.": "你也是，Jan！明天见。",
  "coffee / tea": "咖啡 / 茶",
  "How do you go to school?": "你怎么去学校？",
  "I buy food in the supermarket.": "我在超市买食物。",
  "husband / wife": "丈夫 / 妻子",
  "What don't you like?": "你不喜欢什么？",
  "I drink coffee. What are you eating tonight?": "我喝咖啡。你今晚吃什么？",
  "Do you like sports?": "你喜欢运动吗？",
  "What time do you go to sleep?": "你几点睡觉？",
  "living room / bedroom": "客厅 / 卧室",
  "I come from ...": "我来自 ...",
  "I get up at 7 o'clock. And you?": "我7点起床。你呢？",
  "My number is ...": "我的号码是 ...",
  "What do you do on the weekend?": "你周末做什么？",
  "I like to walk. And you?": "我喜欢散步。你呢？",
  "In my free time ...": "在我的空闲时间 ...",
  "My favorite room is ...": "我最喜欢的房间是 ...",
  "name / last name": "名字 / 姓氏",
  "What do you do in the evening?": "你晚上做什么？",
  "I go running. What do you do on the weekend?": "我去跑步。你周末做什么？",
  "Where do you come from?": "你来自哪里？",
  "In the evening I ...": "晚上我 ...",
  "My hobby is ...": "我的爱好是 ...",
  "I speak Dutch and English. Where do you live?": "我说荷兰语和英语。你住在哪里？",
  "I live in a house. With a garden. Do you have a balcony?": "我住在一栋房子里。带花园。你有阳台吗？",
  "How many rooms does your house have?": "你的房子有多少个房间？",
  "neighborhood / park": "社区 / 公园",
  "Do you like ...?": "你喜欢 ...吗？",
  "Do you live in a house or an apartment?": "你住在房子里还是公寓里？",
  "garden / balcony": "花园 / 阳台",
  "What do you drink in the morning?": "你早上喝什么？",
  "I go to sleep a bit later, around 11 o'clock. But I read a little bit first.": "我睡得晚一点，大概11点。但我先读一会书。",
  "Yes, I play soccer on Saturdays. And you?": "是的，我星期六踢足球。你呢？",
  "I like to watch ...": "我喜欢看 ...",
  "Do you cook yourself?": "你自己做饭吗？",
  "I eat fish with fries. Do you cook?": "我吃炸鱼薯条。你做饭吗？",
  "I eat rice with chicken. And you?": "我吃鸡肉米饭。你呢？",
  "supermarket / market": "超市 / 市场",
  "to get up / morning": "起床 / 早上",
  "What do you like?": "你喜欢什么？",
  "I live in ...": "我住在 ...",
  "I like to eat ...": "我喜欢吃 ...",
  "I go to school / work by ...": "我乘坐...去学校/工作。",
  "Hi! My name is Maria. And you?": "你好！我叫Maria。你呢？",
  "to cook / to make food": "做饭 / 做食物",
  "What is your name?": "你叫什么名字？",
  "I listen to music. And I read a book. Do you play sports?": "我听音乐。我读书。你做运动吗？",
  "I drink tea. And you?": "我喝茶。你呢？",
  "I like sports, I do ...": "我喜欢运动，我做 ...",
  "evening / to sleep": "晚上 / 睡觉",
  "What is your phone number?": "你的电话号码是多少？",
  "fruit / vegetables": "水果 / 蔬菜",
  "what time / time": "几点 / 时间",
  "I have a garden / balcony.": "我有一个花园 / 阳台。",
  "friends / family": "朋友 / 家人",
  "dinner": "晚餐",
  "breakfast": "早餐"
}

def replacer(match):
    en_str = match.group(1)
    if en_str in translations_dict:
        # If zh already exists (like if we ran this twice), don't add it again
        if ', zh:' in match.group(0):
            return match.group(0)
        zh_str = translations_dict[en_str]
        return f'en: "{en_str}", zh: "{zh_str}"'
    return match.group(0)

# We use regex to find all `en: "..."` and inject `zh: "..."`
content = re.sub(r'en:\s*"([^"]+)"', replacer, content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Finished injecting Chinese translations into praatplaat.html")
