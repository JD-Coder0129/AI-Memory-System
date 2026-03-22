from abc import ABC, abstractmethod
import json
import os

try:
    import colorama
    colorama.init(autoreset=True)
    USE_COLORAMA = True
except Exception:
    USE_COLORAMA = False

MEMORY_FILE = "jarvis_memory.json"


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"

    @staticmethod
    def wrap(text: str, code: str) -> str:
        return f"{code}{text}{Colors.ENDC}"


def c(text: str, style: str) -> str:
    return Colors.wrap(text, style)


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
            print(c(f"Memory unit '{name}' does not exist.", Colors.FAIL))

    def load_from_file(self, name: str, query: str) -> str:
        if name in self.memory_units:
            return self.memory_units[name].retrieve(query)
        else:
            print(c(f"Memory unit '{name}' does not exist.", Colors.FAIL))
            return None

    def delete_from_file(self, name: str, data: str) -> None:
        if name in self.memory_units:
            self.memory_units[name].delete(data)
            self.save_memory_units()
        else:
            print(c(f"Memory unit '{name}' does not exist.", Colors.FAIL))

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
        summary_lines = []
        for name, unit in self.memory_units.items():
            entries = unit.get_entries()
            header = c(f"{name.capitalize()}s ({len(entries)}):", Colors.HEADER + Colors.BOLD)
            summary_lines.append(header)
            if entries:
                for idx, entry in enumerate(entries, 1):
                    line = c(f"  {idx}. ", Colors.OKBLUE) + c(entry, Colors.OKGREEN)
                    summary_lines.append(line)
            else:
                summary_lines.append(c("  (none)", Colors.WARNING))
        return "\n".join(summary_lines)


class JarvisCore:
    def __init__(self):
        self.memory_manager = MemoryManager()

    def start(self):
        start_banner = c("\n~~~~~~~~~Jarvis System is online! 🤖~~~~~~~~~", Colors.OKCYAN + Colors.BOLD)
        print(start_banner)
        while True:
            try:
                user_prompt = c("User:", Colors.OKBLUE + Colors.BOLD)
                user_input = input(f"\n{user_prompt} ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                print(c("\n~~~~~~~~~Jarvis System is offline! 🤖~~~~~~~~~", Colors.OKCYAN + Colors.BOLD))
                break

            lowered = user_input.lower().strip()
            if lowered.startswith("add note"):
                data = user_input[len("add note"):].strip()
                self.memory_manager.save_to_file("note", data)
                print(c("Jarvis: ", Colors.OKCYAN) + c("Note saved 📝", Colors.OKGREEN))
            elif lowered.startswith("add reminder"):
                data = user_input[len("add reminder"):].strip()
                self.memory_manager.save_to_file("reminder", data)
                print(c("Jarvis: ", Colors.OKCYAN) + c("Reminder set ⏰", Colors.OKGREEN))
            elif lowered.startswith("add preference"):
                data = user_input[len("add preference"):].strip()
                self.memory_manager.save_to_file("preference", data)
                print(c("Jarvis: ", Colors.OKCYAN) + c("Preference updated ⚙️", Colors.OKGREEN))
            elif lowered.startswith("find note"):
                query = user_input[len("find note"):].strip()
                result = self.memory_manager.load_from_file("note", query)
                if result:
                    print(c("Jarvis: ", Colors.OKCYAN) + c(result, Colors.OKGREEN))
                else:
                    print(c("Jarvis: ", Colors.OKCYAN) + c("Note not found.", Colors.WARNING))
            elif lowered.startswith("find reminder"):
                query = user_input[len("find reminder"):].strip()
                result = self.memory_manager.load_from_file("reminder", query)
                if result:
                    print(c("Jarvis: ", Colors.OKCYAN) + c(result, Colors.OKGREEN))
                else:
                    print(c("Jarvis: ", Colors.OKCYAN) + c("Reminder not found.", Colors.WARNING))
            elif lowered.startswith("find preference"):
                query = user_input[len("find preference"):].strip()
                result = self.memory_manager.load_from_file("preference", query)
                if result:
                    print(c("Jarvis: ", Colors.OKCYAN) + c(result, Colors.OKGREEN))
                else:
                    print(c("Jarvis: ", Colors.OKCYAN) + c("Preference not found.", Colors.WARNING))
            elif lowered.startswith("delete note"):
                data = user_input[len("delete note"):].strip()
                self.memory_manager.delete_from_file("note", data)
                print(c("Jarvis: ", Colors.OKCYAN) + c("Note deleted 🗑️", Colors.FAIL))
            elif lowered.startswith("delete reminder"):
                data = user_input[len("delete reminder"):].strip()
                self.memory_manager.delete_from_file("reminder", data)
                print(c("Jarvis: ", Colors.OKCYAN) + c("Reminder deleted 🗑️", Colors.FAIL))
            elif lowered.startswith("delete preference"):
                data = user_input[len("delete preference"):].strip()
                self.memory_manager.delete_from_file("preference", data)
                print(c("Jarvis: ", Colors.OKCYAN) + c("Preference deleted 🗑️", Colors.FAIL))
            elif lowered == "save memory":
                self.memory_manager.save_memory_units()
                print(c("Jarvis: Memory saved.", Colors.OKGREEN))
            elif lowered == "load memory":
                self.memory_manager.load_memory_units()
                print(c("Jarvis: Memory loaded.", Colors.OKGREEN))
            elif lowered == "summarize memory":
                summary = self.memory_manager.summarize_memory()
                print(c("Jarvis:\n", Colors.OKCYAN) + summary)
            elif lowered == "thank you":
                print(c("Jarvis: You are welcome!", Colors.OKGREEN))
                print(c("\n~~~~~~~~~Jarvis System is offline! 🤖~~~~~~~~~", Colors.OKCYAN + Colors.BOLD))
                break
            else:
                print(c("Jarvis: Invalid command.", Colors.WARNING))


if __name__ == "__main__":
    jarvis = JarvisCore()
    jarvis.start()
