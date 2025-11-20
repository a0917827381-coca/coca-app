import flet as ft

def main(page: ft.Page):
    # 1. 設定 App 標題與基本樣式
    page.title = "我的計數器 App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # 可以改成 DARK 試試看

    # 2. 定義一個顯示數字的欄位
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # 3. 定義按鈕的觸發事件
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update() # 通知頁面更新數據

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # 4. 將元件加入頁面 (使用 Row 讓它們橫向排列)
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# 啟動 App
ft.app(target=main)