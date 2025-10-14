from abc import ABC, abstractmethod
import json
import os

MEMORY_FILE = "jarvis_memory.json"

class MemoryUnit(ABC):
    @abstractmethod
    def store(self, data: str) -> None:
        pass

    @abstractmethod
    def retrieve(self, query: str) -> str:
        pass

    @abstractmethod
    def delete(self, data: str) -> None:
        pass

    @abstractmethod
    def get_entries(self) -> list:
        pass

    @abstractmethod
    def set_entries(self, entries: list) -> None:
        pass

class ListMemoryUnit(MemoryUnit):
    def __init__(self):
        self.entries = []

    def store(self, data: str) -> None:
        self.entries.append(data)

    def retrieve(self, query: str) -> str:
        return next((entry for entry in self.entries if query in entry), None)

    def delete(self, data: str) -> None:
        if data in self.entries:
            self.entries.remove(data)

    def get_entries(self) -> list:
        return self.entries

    def set_entries(self, entries: list) -> None:
        self.entries = entries

class MemoryManager:
    def __init__(self):
        self.memory_units = {
            "note": ListMemoryUnit(),
            "reminder": ListMemoryUnit(),
            "preference": ListMemoryUnit()
        }
        self.load_memory_units()

    def add_memory_unit(self, name: str, memory_unit: MemoryUnit) -> None:
        self.memory_units[name] = memory_unit

    def save_to_file(self, name: str, data: str) -> None:
        if name in self.memory_units:
            self.memory_units[name].store(data)
            self.save_memory_units()
        else:
            print(f"Memory unit '{name}' does not exist.")

    def load_from_file(self, name: str, query: str) -> str:
        if name in self.memory_units:
            return self.memory_units[name].retrieve(query)
        else:
            print(f"Memory unit '{name}' does not exist.")
            return None

    def delete_from_file(self, name: str, data: str) -> None:
        if name in self.memory_units:
            self.memory_units[name].delete(data)
            self.save_memory_units()
        else:
            print(f"Memory unit '{name}' does not exist.")

    def save_memory_units(self) -> None:
        data = {name: unit.get_entries() for name, unit in self.memory_units.items()}
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_memory_units(self) -> None:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for name, entries in data.items():
                if name in self.memory_units:
                    self.memory_units[name].set_entries(entries)

    def summarize_memory(self) -> str:
        summary = []
        for name, unit in self.memory_units.items():
            entries = unit.get_entries()
            summary.append(f"{name.capitalize()}s ({len(entries)}):")
            if entries:
                for idx, entry in enumerate(entries, 1):
                    summary.append(f"  {idx}. {entry}")
            else:
                summary.append("  (none)")
        return "\n".join(summary)

class JarvisCore:
    def __init__(self):
        self.memory_manager = MemoryManager()

    def start(self):
        print("\n~~~~~~~~~Jarvis System is online! 🤖~~~~~~~~~")
        while True:
            user_input = input("\nUser: ").strip().lower()
            if user_input.startswith("add note"):
                data = user_input[len("add note"):].strip()
                self.memory_manager.save_to_file("note", data)
                print("Note saved 📝")
            elif user_input.startswith("add reminder"):
                data = user_input[len("add reminder"):].strip()
                self.memory_manager.save_to_file("reminder", data)
                print("Reminder set ⏰")
            elif user_input.startswith("add preference"):
                data = user_input[len("add preference"):].strip()
                self.memory_manager.save_to_file("preference", data)
                print("Preference updated ⚙️")
            elif user_input.startswith("find note"):
                query = user_input[len("find note"):].strip()
                result = self.memory_manager.load_from_file("note", query)
                print(f"Jarvis: {result if result else 'Note not found.'}")
            elif user_input.startswith("find reminder"):
                query = user_input[len("find reminder"):].strip()
                result = self.memory_manager.load_from_file("reminder", query)
                print(f"Jarvis: {result if result else 'Reminder not found.'}")
            elif user_input.startswith("find preference"):
                query = user_input[len("find preference"):].strip()
                result = self.memory_manager.load_from_file("preference", query)
                print(f"Jarvis: {result if result else 'Preference not found.'}")
            elif user_input.startswith("delete note"):
                data = user_input[len("delete note"):].strip()
                self.memory_manager.delete_from_file("note", data)
                print("Note deleted 🗑️")
            elif user_input.startswith("delete reminder"):
                data = user_input[len("delete reminder"):].strip()
                self.memory_manager.delete_from_file("reminder", data)
                print("Reminder deleted 🗑️")
            elif user_input.startswith("delete preference"):
                data = user_input[len("delete preference"):].strip()
                self.memory_manager.delete_from_file("preference", data)
                print("Preference deleted 🗑️")
            elif user_input == "save memory":
                self.memory_manager.save_memory_units()
                print("Jarvis: Memory saved.")
            elif user_input == "load memory":
                self.memory_manager.load_memory_units()
                print("Jarvis: Memory loaded.")
            elif user_input == "summarize memory":
                summary = self.memory_manager.summarize_memory()
                print(f"Jarvis:\n{summary}")
            elif user_input == "thank you":
                print("Jarvis: You are welcome!")
                print("\n~~~~~~~~~Jarvis System is offline! 🤖~~~~~~~~~")
                break
            else:
                print("Jarvis: Invalid command.")

if __name__ == "__main__":
    jarvis = JarvisCore()
    jarvis.start()
