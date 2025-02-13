# main.py

import flet as ft
import asyncio
import httpx


class MelonPage(ft.Container):
    def __init__(self):
        super().__init__()
        self.song_list = []
        self.ref = ft.Ref[ft.ListView]()

    def build(self) -> None:
        self.expand = True
        self.content = ft.ListView(
            ref=self.ref,
            controls=[],
        )

    def did_mount(self):
        asyncio.run(self.update_list_async())

    async def update_list_async(self) -> None:
        url = 'https://pyhub.kr/melon/20231204.json'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                song_list = response.json()
                listview = self.ref.current
                if listview is not None:
                    listview.controls = [
                        self.make_tile(song) for song in song_list
                    ]
                    listview.update()

    def make_tile(self, song: dict) -> ft.Control:
        return ft.GestureDetector(
            content=ft.ListTile(
                leading=ft.Image(src=song['커버이미지_주소'],
                                 width=50, height=50),
                title=ft.Text(song['곡명']),
                subtitle=ft.Text(song['가수']),
            ),
            # on_tap=lambda __: self.alert(f"{song['곡명']} - {song['가수']}"),
            on_tap=lambda __: self.page.launch_url(
                f"https://www.melon.com/song/detail.htm?songId={song['곡일련번호']}"
            ),
            mouse_cursor=ft.MouseCursor.CLICK,
        )

    def alert(self, message: str) -> None:
        self.page.open(ft.AlertDialog(content=ft.Text(message, size=30)))


def main(page: ft.Page):
    page.adaptive = True
    page.appbar = ft.AppBar(title=ft.Text('Melon 2023-12-04'))
    page.add(MelonPage())


ft.app(target=main)