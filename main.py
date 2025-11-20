import flet as ft

def main(page: ft.Page):
    page.title = "我的計數器 App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  

   
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update() 

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

   
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



ft.app(target=main)

