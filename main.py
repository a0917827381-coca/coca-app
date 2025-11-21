import flet as ft
import random  # 匯入隨機模組，讓電腦可以隨機出拳

def main(page: ft.Page):
    # --- 1. 頁面基本設定 ---
    page.title = "跟皮卡丘猜拳！"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    # 設定一個可愛的背景顏色 (淡黃色)
    page.bgcolor = "#FFFACD" 

    # --- 2. 定義遊戲資料 ---
    # 剪刀石頭布的選項，我們用 Emoji 讓畫面更有趣
    options = ["✊ 石頭", "✌️ 剪刀", "🖐️ 布"]
    
    # 皮卡丘的圖片網址 (你以後可以換成自己喜歡的)
    pikachu_img_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"

    # --- 3. 建立 UI 元件 (先做出來，還沒放上去) ---
    
    # 皮卡丘的圖片元件
    pikachu_image = ft.Image(
        src=pikachu_img_url,
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    # 顯示狀態和結果的文字標籤
    status_text = ft.Text(
        value="皮卡丘準備好了，請出拳！",
        size=20,
        color=ft.colors.BROWN,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    # --- 4. 遊戲核心邏輯 (大腦) ---
    # 這個函式會在玩家點擊按鈕時執行
    def play_game(e):
        # e.control.text 會抓到玩家點擊的按鈕上面的文字 (例如 "✊ 石頭")
        player_move = e.control.text
        
        # 電腦隨機挑選一個
        computer_move = random.choice(options)

        # 開始判斷輸贏！
        result_message = ""
        
        # 情況一：平手
        if player_move == computer_move:
            result_message = "平手！皮卡丘跟你很有默契喔！"
            status_text.color = ft.colors.BLUE_GREY
            
        # 情況二：玩家贏了
        # (石頭贏剪刀) 或 (剪刀贏布) 或 (布贏石頭)
        elif (player_move == "✊ 石頭" and computer_move == "✌️ 剪刀") or \
             (player_move == "✌️ 剪刀" and computer_move == "🖐️ 布") or \
             (player_move == "🖐️ 布" and computer_move == "✊ 石頭"):
            result_message = "你贏了！皮卡丘不甘心地叫了一聲！"
            status_text.color = ft.colors.GREEN # 贏了變綠色

        # 情況三：剩下的情況就是玩家輸了
        else:
            result_message = "你輸了... 皮卡丘得意地搖尾巴！"
            status_text.color = ft.colors.RED # 輸了變紅色

        # 更新畫面上的文字
        # 顯示皮卡丘出了什麼，以及最後的結果
        status_text.value = f"皮卡丘出了「{computer_move}」\n\n{result_message}"
        
        # 告訴頁面要重新繪製
        page.update()

    # --- 5. 組合畫面 ---
    # 我們用 Column (垂直排列) 把所有東西疊起來
    page.add(
        ft.Column(
            [
                ft.Text("⚡ 跟皮卡丘猜拳挑戰 ⚡", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_700),
                pikachu_image,   # 放皮卡丘圖片
                status_text,     # 放結果文字
                ft.Divider(height=20, color=ft.colors.TRANSPARENT), # 增加一點透明的間距
                # 放三個按鈕，用 Row (水平排列) 讓它們並排
                ft.Row(
                    [
                        # 點擊按鈕時，呼叫 play_game 函式
                        ft.ElevatedButton("✊ 石頭", on_click=play_game, bgcolor=ft.colors.WHITE),
                        ft.ElevatedButton("✌️ 剪刀", on_click=play_game, bgcolor=ft.colors.WHITE),
                        ft.ElevatedButton("🖐️ 布", on_click=play_game, bgcolor=ft.colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20 # 按鈕之間的間距
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # 讓整列的東西都置中對齊
            spacing=10 # 垂直元件之間的間距
        )
    )

ft.app(target=main)
