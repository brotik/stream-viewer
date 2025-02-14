import tkinter as tk
import threading
import requests
import random

class StreamViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Stream Viewer")
        self.proxies = self.load_proxies("proxies.txt")  # Загрузка списка прокси из файла
        self.running = False
        self.threads = []

        # Поле для ввода URL стрима
        self.url_label = tk.Label(root, text="Stream URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        # Поле для ввода прокси
        self.proxy_label = tk.Label(root, text="Proxy (IP:Port):")
        self.proxy_label.pack()
        self.proxy_entry = tk.Entry(root, width=50)
        self.proxy_entry.pack()

        # Поле для установки количества зрителей
        self.viewers_label = tk.Label(root, text="Number of Viewers:")
        self.viewers_label.pack()
        self.viewers_entry = tk.Entry(root, width=50)
        self.viewers_entry.pack()

        # Кнопки запуска и остановки
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack()
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()

    def load_proxies(self, filename):
        with open(filename, "r") as file:
            proxies = file.read().splitlines()
        return proxies

    def start(self):
        if not self.running:
            self.running = True
            url = self.url_entry.get()
            num_viewers = int(self.viewers_entry.get())
            for _ in range(num_viewers):
                thread = threading.Thread(target=self.watch_stream, args=(url,))
                self.threads.append(thread)
                thread.start()

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()
        self.threads = []

    def watch_stream(self, url):
        while self.running:
            proxy = self.get_random_proxy()
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
                if response.status_code == 200:
                    print(f"Watching stream via {proxy}")
                else:
                    print(f"Failed to connect via {proxy}")
            except requests.RequestException as e:
                print(f"Error with proxy {proxy}: {e}")

    def get_random_proxy(self):
        return random.choice(self.proxies)

if __name__ == "__main__":
    root = tk.Tk()
    app = StreamViewer(root)
    root.mainloop()