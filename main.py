import flet as ft
import random
import time

def main(page: ft.Page):
    # --- 1. 頁面基本設定 ---
    page.title = "皮卡丘大對決"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#FFFACD"  # 淡黃色背景
    page.scroll = "AUTO"      # 如果螢幕太小，允許捲動

    # --- 2. 遊戲變數 (State) ---
    # 我們用一個字典來存儲狀態，方便在函式中修改
    state = {
        "player_score": 0,
        "pikachu_score": 0,
        "target_score": 0,  # 目標分數 (例如 3戰2勝 就是 2)
        "mode": ""          # "Bo3", "Bo5", "Unlimited"
    }

    # --- 3. 定義 UI 元件 ---

    # 皮卡丘圖片
    img_pikachu = ft.Image(
        src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        width=180,
        height=180,
    )

    # 狀態文字 (顯示誰贏誰輸)
    txt_result = ft.Text(
        value="請選擇戰鬥模式！",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BROWN,
        text_align=ft.TextAlign.CENTER
    )

    # 計分板 (左邊玩家，右邊皮卡丘)
    txt_p_score = ft.Text("玩家: 0", size=18, color=ft.colors.BLUE_800, weight=ft.FontWeight.BOLD)
    txt_c_score = ft.Text("皮卡丘: 0", size=18, color=ft.colors.ORANGE_800, weight=ft.FontWeight.BOLD)

    score_board = ft.Row(
        [
            ft.Column([ft.Text("🧑 你"), txt_p_score], horizontal_alignment="CENTER"),
            ft.Text("VS", size=30, color=ft.colors.GREY_400, italic=True),
            ft.Column([ft.Text("⚡ 對手"), txt_c_score], horizontal_alignment="CENTER"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND, # 左右分散對齊
        width=300,
        visible=False # 一開始先隱藏，選完模式才出現
    )

    # --- 4. 遊戲邏輯函式 ---

    def update_score_ui():
        """更新計分板文字"""
        txt_p_score.value = str(state["player_score"])
        txt_c_score.value = str(state["pikachu_score"])
        page.update()

    def check_game_over():
        """檢查是否達到勝利條件"""
        # 如果是不限次數模式 (target_score = 999)，就不會結束
        if state["target_score"] == 999:
            return

        win_score = state["target_score"]
        
        if state["player_score"] >= win_score:
            txt_result.value = "🏆 恭喜！你贏得了這場對決！"
            txt_result.color = ft.colors.GREEN
            game_controls.visible = False # 隱藏猜拳按鈕
            btn_surrender.text = "回到主選單" # 改按鈕文字
            btn_surrender.icon = "HOME" # 舊版Flet可能不支援icon屬性如果報錯請刪除這行，這裡先保留字串寫法
            page.update()
            
        elif state["pikachu_score"] >= win_score:
            txt_result.value = "💀 遺憾... 皮卡丘獲勝了！"
            txt_result.color = ft.colors.RED
            game_controls.visible = False
            btn_surrender.text = "回到主選單"
            page.update()

    def play(e):
        """玩家出拳邏輯"""
        player_move = e.control.data # 取得按鈕上的資料 (石頭/剪刀/布)
        options = ["石頭", "剪刀", "布"]
        computer_move = random.choice(options)

        msg = ""
        # 判斷勝負
        if player_move == computer_move:
            msg = "平手！"
            txt_result.color = ft.colors.BLUE_GREY
        elif (player_move == "石頭" and computer_move == "剪刀") or \
             (player_move == "剪刀" and computer_move == "布") or \
             (player_move == "布" and computer_move == "石頭"):
            msg = "你贏了這一局！"
            state["player_score"] += 1
            txt_result.color = ft.colors.GREEN
        else:
            msg = "皮卡丘贏了這一局！"
            state["pikachu_score"] += 1
            txt_result.color = ft.colors.RED

        txt_result.value = f"對手出【{computer_move}】\n{msg}"
        update_score_ui()
        check_game_over()

    def start_game(target, mode_name):
        """開始遊戲初始化"""
        state["target_score"] = target
        state["player_score"] = 0
        state["pikachu_score"] = 0
        state["mode"] = mode_name
        
        # UI 切換
        mode_selection.visible = False # 隱藏選單
        score_board.visible = True     # 顯示計分板
        game_controls.visible = True   # 顯示猜拳按鈕
        btn_surrender.visible = True   # 顯示投降/回首頁
        btn_surrender.text = "🏳️ 放棄戰鬥" # 重置按鈕文字
        
        txt_result.value = f"模式：{mode_name}\n戰鬥開始！"
        txt_result.color = ft.colors.BROWN
        update_score_ui()
        page.update()

    def surrender(e):
        """投降 / 回到主選單"""
        # UI 切換回主選單
        mode_selection.visible = True
        score_board.visible = False
        game_controls.visible = False
        btn_surrender.visible = False
        
        txt_result.value = "請選擇戰鬥模式！"
        txt_result.color = ft.colors.BROWN
        page.update()

    # --- 5. 建立按鈕群組 ---

    # 模式選擇按鈕
    mode_selection = ft.Column(
        [
            ft.ElevatedButton("🔥 3戰 2勝", on_click=lambda e: start_game(2, "3戰2勝"), width=200),
            ft.ElevatedButton("⚔️ 5戰 3勝", on_click=lambda e: start_game(3, "5戰3勝"), width=200),
            ft.ElevatedButton("∞ 不限次數", on_click=lambda e: start_game(999, "無限模式"), width=200),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # 遊戲控制按鈕 (石頭剪刀布) - 放在 Row 裡面並排
    game_controls = ft.Row(
        [
            ft.ElevatedButton("✊", data="石頭", on_click=play, width=80, height=80),
            ft.ElevatedButton("✌️", data="剪刀", on_click=play, width=80, height=80),
            ft.ElevatedButton("🖐️", data="布", on_click=play, width=80, height=80),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False # 一開始隱藏
    )

    # 投降按鈕
    btn_surrender = ft.TextButton(
        "🏳️ 放棄戰鬥", 
        on_click=surrender, 
        visible=False
    )

    # --- 6. 組合最終畫面 ---
    page.add(
        ft.Column(
            [
                ft.Text("⚡ 皮卡丘大對決 ⚡", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_700),
                img_pikachu,
                score_board,     # 計分板 (左右顯示)
                ft.Divider(height=10, color="transparent"),
                txt_result,      # 顯示結果文字
                ft.Divider(height=10, color="transparent"),
                mode_selection,  # 模式選擇區
                game_controls,   # 猜拳按鈕區
                ft.Divider(height=20, color="transparent"),
                btn_surrender    # 投降按鈕
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

ft.app(target=main)
