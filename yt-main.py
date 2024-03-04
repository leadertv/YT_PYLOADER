from pytube import YouTube
from pytube.cli import on_progress

def get_available_resolutions(streams):
    return sorted({stream.resolution for stream in streams if stream.resolution is not None}, key=lambda res: int(res[:-1]), reverse=True)

def download_youtube_video(url):
    yt = YouTube(url, on_progress_callback=on_progress)

    try:
        # Получаем список всех видео-потоков
        video_streams = yt.streams.filter(progressive=True, file_extension="mp4")
        available_resolutions = get_available_resolutions(video_streams)

        # Если не найдено ни одного видео
        if not available_resolutions:
            print("Доступные для скачивания видео-потоки не найдены.")
            return

        # Показываем пользователю доступные разрешения и просим сделать выбор
        print("Доступные разрешения:")
        for i, resolution in enumerate(available_resolutions, start=1):
            print(f"{i}. {resolution}")
        choice = input("Выберите желаемое разрешение (введите номер): ")

        # Проверяем корректность ввода
        try:
            selected_resolution = available_resolutions[int(choice) - 1]
        except (IndexError, ValueError):
            print("Некорректный выбор. Скачивание отменено.")
            return

        # Скачиваем выбранное видео
        video_stream = video_streams.filter(res=selected_resolution).first()
        video_path = video_stream.download()
        print(f"Видео скачано: {video_path}")
    except Exception as e:
        print(f"Произошла ошибка при скачивании видео: {e}")

if __name__ == "__main__":
    video_url = input("Вставь ссылку на видео с YouTube: ")
    download_youtube_video(video_url)
