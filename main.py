import pytchat
import time
import random
cat_images = ["cat1.png", "cat2.png", "cat3.png", "cat4.png"]
from sudachipy import dictionary, tokenizer
from collections import deque

# SudachiPy の辞書をfull指定で読み込み
tokenizer_obj = dictionary.Dictionary(dict="full").create()

# 名前ごとに色を割り当てる辞書
name_to_color = {}
cute_colors = [
    "#d6336c", "#ff6f61", "#cc66ff", "#3399ff",
    "#ff9900", "#33cc99", "#ff3366", "#9966cc",
]

# 漢字の読みを付ける関数
def add_ruby(text):
    result = ""
    for m in tokenizer_obj.tokenize(text, tokenizer.Tokenizer.SplitMode.C):
        surface = m.surface()
        reading = m.reading_form()
        if any("\u4e00" <= ch <= "\u9fff" for ch in surface):
            if surface != reading:
                result += f"<ruby>{surface}<rt>{reading}</rt></ruby>"
            else:
                result += surface
        else:
            result += surface
    return result

# HTMLファイルに書き出す
def write_to_html(all_messages):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="5">
  <style>
    body {{
      background: #ffe4ec;
      font-family: "Rounded Mplus 1c", "Hiragino Maru Gothic ProN", "メイリオ", sans-serif;
      padding: 30px;
    }}
    .comment-box {{
      display: flex;
      align-items: flex-end;
      margin-bottom: 30px;
    }}
    .icon {{
      width: 60px;
      height: 60px;
      margin: 0 10px;
    }}
    .comment {{
      position: relative;
      padding: 15px 20px;
      background: #ffffff;
      border: 2px solid #ccc;
      border-radius: 20px;
      max-width: 70%;
      font-size: 22px;
      color: #333;
      line-height: 1.6;
      box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }}
    .comment::after {{
      content: "";
      position: absolute;
      bottom: -15px;
      left: 30px;
      width: 0;
      height: 0;
      border: 15px solid transparent;
      border-top-color: #ffffff;
    }}
    ruby rt {{
      font-size: 14px;
      color: #ff69b4;
    }}
  </style>
</head>
<body>
{all_messages}
</body>
</html>""")

# ==== メイン処理 ====
video_id = input("YouTubeの動画IDを入力してください（例：5qap5aO4i9A）: ")
chat = pytchat.create(video_id=video_id)
comment_queue = deque(maxlen=100)

print("確認用: チャット取得オブジェクト作成完了")
print("動画ID:", video_id)
print("chat.is_alive() =", chat.is_alive())

try:
    while chat.is_alive():
        chatdata = chat.get()
        # print("デバッグ: チャットを取得")
        for c in chatdata.sync_items():
            ruby_text = add_ruby(c.message)
            print(f"{c.author.name}: {ruby_text}")

            if c.author.name not in name_to_color:
                name_to_color[c.author.name] = random.choice(cute_colors)
            name_color = name_to_color[c.author.name]

            cat_image = random.choice(cat_images)  # ← ここで猫画像をランダムに選ぶ！

            comment_html = f'''
<div class="comment-box">
  <img class="icon" src="{cat_image}" alt="cat">
  <div class="comment">
    <span style="color: {name_color}; font-weight: bold;">{c.author.name}</span>: {ruby_text}
  </div>
</div>'''

            comment_queue.append(comment_html)
            all_comments = "\n".join(comment_queue)
            write_to_html(all_comments)
        time.sleep(1)
except Exception as e:
    print("⚠️ エラーが発生:", e)
