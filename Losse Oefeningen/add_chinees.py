import re
import os

filepath = r"g:\Mijn Drive\HTML FILES\Losse Oefeningen\voorzetsels.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add lang-btn
if '<button class="lang-btn" id="btn-zh"' not in content:
    content = content.replace(
        '<button class="lang-btn" id="btn-vi" onclick="setLang(\'vi\')">🇻🇳 Tiếng Việt</button>',
        '<button class="lang-btn" id="btn-vi" onclick="setLang(\'vi\')">🇻🇳 Tiếng Việt</button>\n        <button class="lang-btn" id="btn-zh" onclick="setLang(\'zh\')">🇨🇳 中文</button>'
    )

# 2. Add spans
spans = [
    (r'<span lang="vi">Địa điểm</span>', r'<span lang="vi">Địa điểm</span><span lang="zh">位置</span>'),
    (r'<span lang="vi">Phương hướng</span>', r'<span lang="vi">Phương hướng</span><span lang="zh">方向</span>'),
    (r'<span lang="vi">Để thực hành</span>', r'<span lang="vi">Để thực hành</span><span lang="zh">练习</span>'),
    (r'<span lang="vi" >Học giới từ</span>', r'<span lang="vi" >Học giới từ</span><span lang="zh">学习介词</span>'),
    (r'<span lang="vi" >Tìm hiểu sự khác biệt giữa Địa điểm</span>', r'<span lang="vi" >Tìm hiểu sự khác biệt giữa Địa điểm</span><span lang="zh">学习<strong>位置</strong>和<strong>方向</strong>之间的区别。</span>'),
    (r'<span lang="vi">Lưu ý: Nhiều nghĩa</span>', r'<span lang="vi">Lưu ý: Nhiều nghĩa</span><span lang="zh">注意：多重含义</span>'),
    (r'<span lang="vi">Hãy coi chừng! Một số giới từ có nhiều nghĩa. Ý nghĩa phụ thuộc vào ngữ cảnh và các từ khác trong câu.</span>', r'<span lang="vi">Hãy coi chừng! Một số giới từ có nhiều nghĩa. Ý nghĩa phụ thuộc vào ngữ cảnh và các từ khác trong câu.</span><span lang="zh">注意！有些介词有多种含义。其含义取决于上下文和句子中的其他词。</span>'),
    (r'<span lang="vi">địa điểm \(\\"trước cửa\\"\) so với thời gian \(\\"trước 9 giờ sáng\\"\) so với mục đích \(\\"dành cho bạn\\"\)</span>', r'<span lang="vi">địa điểm (\"trước cửa\") so với thời gian (\"trước 9 giờ sáng\") so với mục đích (\"dành cho bạn\")</span><span lang="zh">地点 (\"在门前\") vs. 时间 (\"9点前\") vs. 目的 (\"给你\")</span>'),
    (r'<span lang="vi">hướng/bắt đầu \(\\"từ nơi làm việc\\"\) so với sở hữu \(\\"của tôi\\"\)</span>', r'<span lang="vi">hướng/bắt đầu (\"từ nơi làm việc\") so với sở hữu (\"của tôi\")</span><span lang="zh">方向/起点 (\"下班\") vs. 所属 (\"我的\")</span>'),
    (r'<span lang="vi">địa điểm \(\\"trên bàn\\"\) so với thời gian \(\\"vào thứ Hai\\"\)</span>', r'<span lang="vi">địa điểm (\"trên bàn\") so với thời gian (\"vào thứ Hai\")</span><span lang="zh">地点 (\"在桌子上\") vs. 时间 (\"在星期一\")</span>'),
    (r'<span lang="vi">địa điểm \(\\"trong hộp\\"\) so với thời gian \(\\"trong tháng 1\\"\)</span>', r'<span lang="vi">địa điểm (\"trong hộp\") so với thời gian (\"trong tháng 1\")</span><span lang="zh">地点 (\"在盒子里\") vs. 时间 (\"在一月\")</span>'),
    (r'<span lang="vi">phương hướng \(\\"qua cầu\\"\) so với thời gian \(\\"trong 5 phút\\"\) so với chủ đề \(\\"nói về\\"\)</span>', r'<span lang="vi">phương hướng (\"qua cầu\") so với thời gian (\"trong 5 phút\") so với chủ đề (\"nói về\")</span><span lang="zh">方向 (\"过桥\") vs. 时间 (\"5分钟后\") vs. 主题 (\"谈论关于\")</span>')
]

for search, replace in spans:
    content = re.sub(search, replace, content)

# 3. Add to JS arrays
# We will do a generic replacement for JS objects
translations = {
    # Plaats
    "Trong một không gian trống rỗng.": "在一个空心空间里。",
    "Sữa ở trong tủ lạnh.": "牛奶在冰箱里。",
    "Tôi đang ở siêu thị.": "我在超市里。",
    "Cây bút ở trong túi.": "笔在包里。",
    "IN = Vật rỗng.": "IN = 空心物体。",
    
    "Trên một bề mặt.": "在一个表面上。",
    "Cuốn sách ở trên bàn.": "书在桌子上。",
    "Tôi đang ngồi trên đi văng.": "我坐在沙发上。",
    "Quả táo ở trên đĩa.": "苹果在盘子里。",
    "OP = Tiếp xúc với bề mặt.": "OP = 接触表面。",
    
    "Cao hơn (không liên lạc).": "高于（没有接触）。",
    "Chiếc đèn treo phía trên bàn.": "灯悬挂在桌子上方。",
    "Con chim bay phía trên cây.": "鸟在树上方飞翔。",
    "Đám mây lơ lửng phía trên thành phố.": "云在城市上空漂浮。",
    "TRÊN = Di chuột qua nó.": "BOVEN = 悬浮在上方。",
    
    "Thấp hơn.": "低于。",
    "Con mèo ở dưới gầm bàn.": "猫在桌子底下。",
    "Đôi giày ở dưới ghế sofa.": "鞋子在沙发下面。",
    "Tôi đang tắm.": "我在洗澡。",
    "DƯỚI = Thấp hơn.": "ONDER = 低于。",
    
    "Đằng trước.": "前面。",
    "Ôtô đậu trước nhà.": "车在房子前面。",
    "Tôi đang ở cửa.": "我在门前。",
    "Jan đang ngồi trước tivi.": "Jan坐在电视机前。",
    "TRƯỚC = Phía trước.": "VOOR = 前面。",
    
    "Mặt sau.": "后面。",
    "Khu vườn nằm phía sau nhà.": "花园在房子后面。",
    "Mặt trời ở sau những đám mây.": "太阳在云层后面。",
    "Tôi ở phía sau bạn.": "我在你后面。",
    "SAU = Trở lại.": "ACHTER = 后面。",
    
    "Bên.": "旁边。",
    "Tôi đang ngồi cạnh bạn tôi.": "我坐在朋友旁边。",
    "Tiệm bánh nằm cạnh ngân hàng.": "面包店在银行旁边。",
    "Chiếc kính ở cạnh máy tính xách tay.": "眼镜在笔记本电脑旁边。",
    "TIẾP THEO = Bên cạnh.": "NAAST = 旁边。",
    
    "Ở giữa 2.": "在两者之间。",
    "Tôi đang đứng giữa hai cái cây.": "我站在两棵树之间。",
    "Đứa trẻ ngủ giữa bố mẹ.": "孩子睡在父母之间。",
    "Chìa khóa nằm giữa các đệm.": "钥匙在垫子之间。",
    "GIỮA = Giữa.": "TUSSEN = 中间。",
    
    "Dựa vào.": "靠着。",
    "Chiếc xe đạp dựa vào tường.": "自行车靠在墙上。",
    "Tôi dựa vào tủ.": "我靠在柜子上。",
    "Cái thang dựa vào cái cây.": "梯子靠在树上。",
    "CHỐNG = Liên hệ.": "TEGEN = 靠着。",
    
    "Mắc kẹt.": "附着。",
    "Đồng hồ treo trên tường.": "钟挂在墙上。",
    "Chiếc áo khoác treo trên giá treo áo khoác.": "外套挂在衣架上。",
    "Tôi sống trên mặt nước.": "我住在水边。",
    "BẬT = Đã xác nhận.": "AAN = 附着/固定。",
    
    "Khoảng cách ngắn.": "近距离。",
    "Tôi sống gần trường học.": "我住得离学校很近。",
    "Trạm xe buýt ở gần đó.": "公交车站在附近。",
    "Hãy đến đứng gần tôi.": "靠近我站着。",
    "ĐÓNG = Gần.": "DICHT BIJ = 附近。",
    
    "Khoảng cách lớn.": "远距离。",
    "Tôi sống xa nơi làm việc.": "我住得离工作地点很远。",
    "Siêu thị ở xa đây.": "超市离这里很远。",
    "Chúng tôi đang ở xa nhà.": "我们离家很远。",
    "XA TỪ = Khoảng cách.": "VER VAN = 距离。",
    
    "Bên trái.": "左边。",
    "Cái tủ ở bên trái.": "柜子在左边。",
    "Nhà vệ sinh ở bên trái hành lang.": "厕所在走廊的左边。",
    "Cô ấy ngồi bên trái tôi.": "她坐在我左边。",
    "TRÁI = Bên trái.": "LINKS = 左边。",
    
    "Bên phải.": "右边。",
    "Ghế sofa ở bên phải.": "沙发在右边。",
    "Nhà bếp nằm ở bên phải phòng khách.": "厨房在客厅的右边。",
    "Anh ấy đi về phía bên phải của con đường.": "他走在路的右边。",
    "PHẢI = Bên phải.": "RECHTS = 右边。",
    
    # Richting
    "Bên trong.": "向内。",
    "Lên xe buýt.": "上公交车。",
    "Bước vào cửa hàng.": "走进商店。",
    "Vứt nó vào thùng rác.": "把它扔进垃圾桶。",
    "IN = Hướng vào trong.": "IN = 向内。",
    
    "Ngoài.": "向外。",
    "Xuống xe buýt.": "下公交车。",
    "Bước ra khỏi tòa nhà.": "走出大楼。",
    "Lấy sữa ra khỏi tủ lạnh.": "把牛奶从冰箱里拿出来。",
    "NGOÀI = Bên ngoài.": "UIT = 向外。",
    
    "Điểm đến.": "目的地。",
    "Tôi đang về nhà.": "我正在回家。",
    "Chúng tôi đạp xe đến thành phố.": "我们骑自行车去城市。",
    "Cô ấy đang xem phim.": "她正在看电影。",
    "ĐẾN = Điểm đến.": "NAAR = 目的地。",
    
    "Nguồn gốc.": "起点。",
    "Tôi đang đi làm về.": "我刚下班。",
    "Tàu xuất phát từ Amsterdam.": "火车从阿姆斯特丹开来。",
    "Tôi đã nhận được một món quà từ Jan.": "我收到了Jan的礼物。",
    "TỪ = Điểm bắt đầu.": "VAN = 起点。",
    
    "Trở lên.": "向上。",
    "Tôi đang đi lên lầu.": "我正在上楼。",
    "Con chim bay lên cao.": "鸟儿向上飞。",
    "Đặt hộp ngửa lên.": "把盒子放在楼上。",
    "LÊN = Lên.": "BOVEN = 向上。",
    
    "Xuống.": "向下。",
    "Tôi đang đi xuống tầng dưới.": "我正在下楼。",
    "Thang máy đi xuống.": "电梯正在下降。",
    "Đặt cuốn sách của bạn xuống.": "把你的书放下。",
    "XUỐNG = Xuống.": "BENEDEN = 向下。",
    
    "Vượt qua.": "穿过/跨过。",
    "Tôi đi bộ qua cầu.": "我走过桥。",
    "Chúng tôi bay qua biển.": "我们飞过大海。",
    "Nhảy qua hàng rào.": "跳过篱笆。",
    "TRÊN = Vượt qua.": "OVER = 穿过/跨过。",
    
    "Ở giữa nó.": "穿过(中间)。",
    "Tôi lái xe qua đường hầm.": "我开车穿过隧道。",
    "Chúng tôi đi bộ qua công viên.": "我们走过公园。",
    "Nhìn qua cửa sổ.": "透过窗户看。",
    "QUA = Thoát ra.": "DOOR = 穿过/出来。",
    
    "Vòng tròn.": "圆圈。",
    "Chúng tôi đi dạo quanh hồ.": "我们绕着湖走。",
    "Ôtô chạy vòng vòng.": "汽车绕着环岛行驶。",
    "Hãy nhìn quanh phòng.": "环顾四周。",
    "TRÒN = Vòng tròn.": "ROND = 圆圈。",
    
    "Song song.": "沿着/平行。",
    "Tôi đi bộ dọc theo con đường.": "我沿着路走。",
    "Tàu chạy dọc bờ biển.": "火车沿着海岸行驶。",
    "Hãy đến nhà tôi.": "顺便来我家一趟。",
    "ALONG = Bên cạnh nó.": "LANGS = 沿着/旁边。",
    
    "Khoảng cách.": "远离(距离)。",
    "Tôi bước ra khỏi đám cháy.": "我走离火堆。",
    "Lái xe ra khỏi thành phố.": "开车驶离城市。",
    "Thoát khỏi nơi nguy hiểm.": "离开危险的地方。",
    "AWAY = Khoảng cách.": "WEG = 距离。"
}

for vi, zh in translations.items():
    content = content.replace(f'vi: "{vi}"', f'vi: "{vi}", zh: "{zh}"')
    content = content.replace(f"vi: '{vi}'", f"vi: '{vi}', zh: '{zh}'")

content = content.replace('vi: "Quy tắc logic"', 'vi: "Quy tắc logic", zh: "逻辑规则"')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Done updating")
