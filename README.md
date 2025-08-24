# NetTalk

💬 NetTalk (LAN Chat Application)

A real-time LAN-based chat application built with Python (WebSocket, HTTP Server) and Vanilla JavaScript.
It allows users on the same network to create rooms, join with a PIN, chat instantly, see typing indicators, and (soon) share files.

✨ Features

🏠 Create & Join Rooms with unique 4-digit PINs

👥 List Active Rooms with user counts

💬 Real-time Messaging with chat history

✍️ Typing Indicators ("User is typing...")

🟢 Online Avatars with random colors

📂 Planned Feature: File Sharing

🛠️ Tech Stack

Backend: Python, asyncio, websockets, http.server

Frontend: HTML, CSS, JavaScript (Vanilla)

Protocol: WebSocket for real-time communication

🚀 Getting Started
1️⃣ Install dependencies

Make sure you have Python 3.8+ installed.
Install the required package:

pip install websockets

2️⃣ Run the server
python server.py


WebSocket will run on: ws://localhost:6789

HTTP Server will run on: http://localhost:8000

3️⃣ Open in browser

Navigate to:

http://localhost:8000/index.html


Now you can chat with multiple users on the same LAN network. 🎉


🔮 Roadmap

✅ Typing indicators

✅ Chat history

🔜 Mobile responsive design improvements

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss.

📜 License

MIT License © 2025 [Subodh]
