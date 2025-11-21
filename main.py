import flet as ft
import random

def main(page: ft.Page):
    # --- 1. 頁面基本設定 ---
    page.title = "皮卡丘大對決"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#FFFACD"  # 淡黃色背景
    page.scroll = "AUTO"      # 允許捲動

    # --- 2. 遊戲變數 ---
    state = {
        "player_score": 0,
        "pikachu_score": 0,
        "target_score": 0,
        "mode": ""
    }

    # --- 3. 定義 UI 元件 ---

    img_pikachu = ft.Image(
        src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        width=180,
        height=180,
    )

    # 結果文字 (會顯示皮卡丘的情緒)
    txt_result = ft.Text(
        value="請選擇戰鬥模式！",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BROWN,
        text_align=ft.TextAlign.CENTER
    )

    # 計分板
    txt_p_score = ft.Text("玩家: 0", size=18, color=ft.colors.BLUE_800, weight=ft.FontWeight.BOLD)
    txt_c_score = ft.Text("皮卡丘: 0", size=18, color=ft.colors.ORANGE_800, weight=ft.FontWeight.BOLD)

    score_board = ft.Row(
        [
            ft.Column([ft.Text("🧑 你"), txt_p_score], horizontal_alignment="CENTER"),
            ft.Text("VS", size=30, color=ft.colors.GREY_400, italic=True),
            ft.Column([ft.Text("⚡ 對手"), txt_c_score], horizontal_alignment="CENTER"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        width=300,
        visible=False
    )

    # --- 4. 遊戲邏輯 ---

    def update_score_ui():
        txt_p_score.value = str(state["player_score"])
        txt_c_score.value = str(state["pikachu_score"])
        page.update()

    def check_game_over():
        if state["target_score"] == 999:
            return

        win_score = state["target_score"]
        
        if state["player_score"] >= win_score:
            txt_result.value = "🏆 恭喜！你贏得了這場對決！\n皮卡丘倒在地板上裝死..."
            txt_result.color = ft.colors.GREEN
            game_controls.visible = False
            btn_surrender.text = "回到主選單"
            page.update()
            
        elif state["pikachu_score"] >= win_score:
            txt_result.value = "💀 遺憾... 皮卡丘獲勝了！\n它跳到你頭上慶祝！"
            txt_result.color = ft.colors.RED
            game_controls.visible = False
            btn_surrender.text = "回到主選單"
            page.update()

    def play(e):
        player_move = e.control.data
        options = ["石頭", "剪刀", "布"]
        computer_move = random.choice(options)

        msg = ""
        
        # --- 這裡把皮卡丘的情緒找回來了！ ---
        
        # 1. 平手的情況
        if player_move == computer_move:
            # 隨機挑選一種反應
            reactions = [
                "皮卡丘跟你很有默契喔！⚡",
                "皮卡丘疑惑地歪著頭看你？",
                "你們撞拳了！不分勝負！"
            ]
            msg = random.choice(reactions)
            txt_result.color = ft.colors.BLUE_GREY
            
        # 2. 玩家贏的情況
        elif (player_move == "石頭" and computer_move == "剪刀") or \
             (player_move == "剪刀" and computer_move == "布") or \
             (player_move == "布" and computer_move == "石頭"):
            
            state["player_score"] += 1
            # 隨機挑選一種反應
            reactions = [
                "你贏了！皮卡丘不甘心地叫了一聲 Pika... 🥲",
                "皮卡丘氣噗噗地跺腳！😤",
                "效果顯著！皮卡丘嚇了一跳！"
            ]
            msg = random.choice(reactions)
            txt_result.color = ft.colors.GREEN
            
        # 3. 皮卡丘贏的情況
        else:
            state["pikachu_score"] += 1
            # 隨機挑選一種反應
            reactions = [
                "你輸了... 皮卡丘得意地搖尾巴 Chu! 🎵",
                "皮卡丘對你做了一個鬼臉 😛",
                "皮卡丘看起來非常驕傲！✨"
            ]
            msg = random.choice(reactions)
            txt_result.color = ft.colors.RED

        txt_result.value = f"對手出【{computer_move}】\n{msg}"
        update_score_ui()
        check_game_over()

    def start_game(target, mode_name):
        state["target_score"] = target
        state["player_score"] = 0
        state["pikachu_score"] = 0
        state["mode"] = mode_name
        
        mode_selection.visible = False
        score_board.visible = True
        game_controls.visible = True
        btn_surrender.visible = True
        btn_surrender.text = "🏳️ 放棄戰鬥"
        
        txt_result.value = f"模式：{mode_name}\n皮卡丘蓄勢待發！"
        txt_result.color = ft.colors.BROWN
        update_score_ui()
        page.update()

    def surrender(e):
        mode_selection.visible = True
        score_board.visible = False
        game_controls.visible = False
        btn_surrender.visible = False
        
        txt_result.value = "皮卡丘覺得你逃跑了...\n請選擇戰鬥模式！"
        txt_result.color = ft.colors.BROWN
        page.update()

    # --- 5. 建立按鈕 ---

    mode_selection = ft.Column(
        [
            ft.ElevatedButton("🔥 3戰 2勝", on_click=lambda e: start_game(2, "3戰2勝"), width=200),
            ft.ElevatedButton("⚔️ 5戰 3勝", on_click=lambda e: start_game(3, "5戰3勝"), width=200),
            ft.ElevatedButton("∞ 不限次數", on_click=lambda e: start_game(999, "無限模式"), width=200),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    game_controls = ft.Row(
        [
            ft.ElevatedButton("✊", data="石頭", on_click=play, width=80, height=80),
            ft.ElevatedButton("✌️", data="剪刀", on_click=play, width=80, height=80),
            ft.ElevatedButton("🖐️", data="布", on_click=play, width=80, height=80),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False
    )

    btn_surrender = ft.TextButton("🏳️ 放棄戰鬥", on_click=surrender, visible=False)

    # --- 6. 組合畫面 ---
    page.add(
        ft.Column(
            [
                ft.Text("⚡ 皮卡丘大對決 ⚡", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_700),
                img_pikachu,
                score_board,
                ft.Divider(height=10, color="transparent"),
                txt_result,
                ft.Divider(height=10, color="transparent"),
                mode_selection,
                game_controls,
                ft.Divider(height=20, color="transparent"),
                btn_surrender
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

ft.app(target=main)
