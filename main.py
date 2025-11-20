import flet as ft

def main(page: ft.Page):
    # 1. 設定 App 標題與基本樣式
    page.title = "我的計數器 App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # 想換成黑底可以改成 ft.ThemeMode.DARK

    # 2. 定義一個顯示數字的欄位
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # 3. 定義按鈕的觸發事件 (按下去會發生什麼事)
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update() # 通知頁面更新畫面

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # 4. 將元件加入頁面
    # 我們改用了字串寫法 "remove" 和 "add"，這樣新版 Flet 就不會報錯了
    page.add(
        ft.Row(
            [
                ft.IconButton(icon="remove", on_click=minus_click),
                txt_number,
                ft.IconButton(icon="add", on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# 啟動 App
ft.app(target=main)
