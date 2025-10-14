# 🧠 Jarvis Memory System (v2)

> A modular, file-based AI memory management system built in Python — forming the foundation of my personal assistant project, **Jarvis** 🤖  

This system demonstrates **abstraction**, **composition**, and **persistence** through a clean and extensible architecture that allows Jarvis to “remember” notes, reminders, and user preferences — just like a real assistant.

---

## ⚙️ Features

- 🧩 **Abstract Memory Architecture** – defines a consistent interface using `ABC` for all memory types.  
- 📦 **Unified Memory Storage** – a single JSON file (`jarvis_memory.json`) to persist all entries.  
- 💾 **Auto-Load on Startup** – previously saved data loads automatically every time the program starts.  
- 🧠 **Multiple Memory Categories** – currently supports:
  - Notes  
  - Reminders  
  - Preferences  
- 🧽 **Easy CRUD Operations** – add, find, delete, summarize memories.  
- 🚀 **Extensible Design** – add new memory types in seconds by updating the memory dictionary.  
- 🎨 **Interactive CLI** – simple conversational interface with emoji feedback.

---

## 🧰 Tech Stack

- **Language:** Python 3.x  
- **Modules:**  
  - `abc` – for abstract base class implementation  
  - `json` – for serialization and persistence  
  - `os` – for file handling  

---

## 🧩 Class Architecture

```text
JarvisCore
 └── MemoryManager (composition)
       ├── ListMemoryUnit (inheritance from MemoryUnit)
       │     └── Handles notes, reminders, preferences
