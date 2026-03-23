# 💬 LANChat

LANChat is a **real-time LAN-based chat application** that allows users to create and join chat rooms with a secure PIN system.  
It features **typing indicators, chat history, file sharing support, and room management** — all running seamlessly over WebSocket.

---

## ✨ Features

- 🔒 **Room Creation with PIN Authentication** – Secure and private chat rooms  
- 👥 **Join/Leave Rooms** – Flexible room management  
- 💬 **Real-time Messaging** – Instant message delivery with timestamps  
- ⌨️ **Typing Indicators** – See when others are typing  
<!-- - 🕑 **Chat History** – Keeps track of recent messages  
- 📂 **File Sharing Support** – Send and receive files in chat  
- 🌐 **LAN Hosting** – Works without internet, just on local network  -->

---

## 🚀 Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla JS, WebSocket API)  
- **Backend**: Python (asyncio, websockets, http.server)  
- **Communication**: WebSocket Protocol  

---

## 📷 Screenshot

![Screenshot](assets/image.png)

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/subodh-git77/NetTalk.git
cd NetTalk
```

### 2️⃣ Install Dependencies

Make sure Python 3.8+ is installed.

```bash
pip install websockets
```

### 3️⃣ Run the Server

```bash
python server.py
```

The server will start on:

```
http://localhost:8000
```

### 4️⃣ Access from Other Devices (LAN)

1. Find your local IP address:

   On Windows:
   ```bash
   ipconfig
   ```

   On macOS/Linux:
   ```bash
   ifconfig
   ```

2. Look for something like:
   ```
   192.168.1.5
   ```

3. Other users on the same Wi-Fi/LAN can open:

   ```
   http://192.168.1.5:8000
   ```

---

## 🔐 How It Works

- A user creates a room with a unique Room ID and PIN.
- Other users join using the same Room ID and PIN.
- WebSocket maintains real-time bidirectional communication.
- The server manages:
  - Active rooms
  - Connected users
  - Message history
  - File transfers

---

## 📂 Project Structure

```
LANChat/
│── server.py
│── index.html
│── assets/
│   └── image.png
│── static/
│   ├── style.css
│   └── script.js
│── README.md
```

---

## 🛠️ Future Improvements

- ✅ Private messaging  
- ✅ User authentication system  
- ⏳ Message encryption  
- ⏳ Persistent database storage  
- ⏳ Admin moderation controls  

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create a new branch  
3. Commit your changes  
4. Push and create a Pull Request  

---
<!--
## 📜 License

This project is licensed under the MIT License.

---
-->


<!--
## 🌐 Live Demo (If Hosted)

If hosted locally on LAN:

```
http://<your-local-ip>:8000
```

If deployed online:

```
https://your-live-url.com
```

-->

---

## 👨‍💻 Author

Developed with ❤️ by **Subodh Kumar Agrahari**

---

### ⭐ If you like this project, don’t forget to star the repository!
