import tkinter as tk
from tkinter import messagebox
import threading
import requests
import random

class StreamViewer:
    def init(self, root):
        self.root = root
        self.root.title("Stream Viewer")
        self.root.geometry("400x300")
        self.proxies = self.load_proxies("proxies.txt")  # Загрузка списка прокси из файла
        self.running = False
        self.threads = []

        # Поле для ввода URL стрима
        self.url_label = tk.Label(root, text="Stream URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        # Поле для ввода прокси (опционально)
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
        try:
            with open(filename, "r") as file:
                proxies = file.read().splitlines()
            return proxies
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {filename} not found!")
            return []

    def start(self):
        if not self.running:
            self.running = True
            url = self.url_entry.get()
            num_viewers = self.viewers_entry.get()

            if not url:
                messagebox.showerror("Error", "Please enter a valid stream URL.")
                return
            if not num_viewers.isdigit() or int(num_viewers) <= 0:
                messagebox.showerror("Error", "Please enter a valid number of viewers.")
                return

            num_viewers = int(num_viewers)
            for _ in range(num_viewers):
                thread = threading.Thread(target=self.watch_stream, args=(url,))
                self.threads.append(thread)
                thread.start()
            messagebox.showinfo("Info", f"Started {num_viewers} viewers.")

    def stop(self):
        if self.running:
            self.running = False
            for thread in self.threads:
                thread.join()
            self.threads = []
            messagebox.showinfo("Info", "Stopped all viewers.")

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

if "Stream Viewer" == "main":
    root = tk.Tk()
    app = StreamViewer(root)
    root.mainloop()