# Prompt Code Assistant

> A desktop application that generates structured, token-aware prompts from any codebase — designed to streamline developer workflows with AI assistants like ChatGPT, Claude, and Copilot.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Why This Project Exists

Working with AI coding assistants requires **well-structured context**: folder trees, file contents, and clear instructions — all within token limits. Manually assembling this context is tedious and error-prone.

**Prompt Code Assistant** solves this by providing a visual interface to select project files, automatically generate directory structures, count tokens in real time, and split large prompts into manageable chunks — all with one click to clipboard.

---

## Key Features

- **Visual Project Explorer** — Interactive tree-view file selector with extension-based filtering and folder scoping.
- **Automatic Directory Structure Generation** — Generates a clean text representation of any project's folder hierarchy.
- **File Content Extraction** — Reads and formats selected source files, ready for inclusion in AI prompts.
- **Prompt Composition Engine** — Combines base prompt templates + folder structure + file contents into a single structured output.
- **Real-Time Token Counter** — Uses OpenAI's `tiktoken` (cl100k_base encoding) to display live token counts.
- **Smart Prompt Splitting** — Automatically splits large prompts into configurable token-sized chunks for models with context limits.
- **One-Click Clipboard Copy** — Copy full prompts or individual parts directly to clipboard.
- **Multi-Language UI** — Full internationalization system supporting English, Spanish, and Icelandic with runtime language switching.
- **Theme System** — Switchable Dark (Modern) and Light themes with dynamic style propagation across all panels.
- **Persistent Settings** — Save/load ignore lists, extension filters, and folder scopes via `settings.json`.
- **Path Comment Injection** — Batch-insert relative path comments (`# Path: ...`) into selected source files for better AI context.
- **Contextual Help System** — Middle-click any UI element to get an in-context tooltip explaining its purpose.

---

## Architecture & Design Principles

This project follows a clean **MVC (Model-View-Controller)** architecture with strict separation of concerns:

```
src/
├── controller/              # Application logic & user action handlers
│   └── prompt_controller.py # Orchestrates UI ↔ Core interactions
├── core/                    # Business logic (zero UI dependencies)
│   ├── file_manager.py      # File system traversal, filtering & content extraction
│   └── prompt_generator.py  # Prompt composition with template injection
├── ui/                      # Presentation layer (CustomTkinter)
│   ├── main_window.py       # App entry point, layout & theme/language selectors
│   ├── panel_left.py        # Controls panel: buttons, filters, ignore lists
│   ├── panel_center.py      # Context view: prompt base, structure, file contents
│   ├── panel_right.py       # Output panel: final prompt, token count, split/copy
│   ├── prompt_assistant_gui.py  # File dialog & tree-view selection modal
│   └── themes/              # Pluggable theme system
│       ├── theme_manager.py
│       ├── modern_theme.py
│       ├── light_theme.py
│       └── classic_theme.py
└── utils/                   # Cross-cutting concerns
    ├── i18n.py              # Internationalization engine
    ├── translations_en.py
    ├── translations_es.py
    └── translations_is.py
```

### Engineering Highlights

| Principle | Implementation |
|---|---|
| **Separation of Concerns** | UI panels have no business logic; `PromptController` mediates all interactions between views and core modules. |
| **Pluggable Theme System** | Themes are independent modules returning style dictionaries — adding a new theme requires only a single new file. |
| **Internationalization** | A lightweight `i18n` module with dictionary-based translations and runtime language switching without external dependencies. |
| **Configurable Filtering** | Ignore lists, extension filters, and folder scopes are all user-configurable and persistable. |
| **Token Awareness** | Integrated `tiktoken` for accurate GPT-compatible token counting and intelligent prompt chunking. |
| **Clean Entry Point** | Single `run.py` entry point delegates to `src.main`, which initializes the `MainWindow` — no logic in the runner. |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Desktop UI** | CustomTkinter (modern Tkinter wrapper) |
| **Tokenization** | tiktoken (OpenAI's BPE tokenizer) |
| **Testing** | pytest |
| **Styling** | colorama (terminal output) |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher

### Installation

```bash
git clone https://github.com/gabriel-klettur/Prompt-Projects-Assistant.git
cd Prompt-Projects-Assistant
pip install -r requirements.txt
```

### Run

```bash
python run.py
```

---

## Usage Workflow

1. **(Optional) Select a Prompt Base** — Load a `.md` or `.txt` template as the starting instructions for your AI prompt.
2. **Select Project Folder** — Choose your codebase root. The app generates the folder structure automatically.
3. **Select Files** — Use the interactive tree-view to pick specific files. Filter by extension or scope to specific folders.
4. **Review & Edit** — The center panel shows each component; the right panel shows the composed final prompt with live token count.
5. **Copy or Split** — Copy the full prompt to clipboard, or split it into token-sized parts for models with context limits.

---

## Screenshots

> *Coming soon — the application features a modern dark-themed UI with three-panel layout.*

---

## Project Status

This is an actively developed tool that I use daily in my own workflow. Planned improvements include:

- [ ] Export prompts to file (`.md`, `.txt`)
- [ ] Prompt templates library
- [ ] Git diff integration (prompt only changed files)
- [ ] Drag-and-drop file selection
- [ ] Automated tests for core modules

---

## About the Author

I'm a software developer passionate about building tools that improve developer productivity. This project demonstrates my ability to:

- **Design and implement clean architectures** (MVC, separation of concerns)
- **Build desktop applications** with modern UI frameworks
- **Create internationalized software** with runtime language switching
- **Implement pluggable systems** (themes, filters, settings persistence)
- **Work with tokenization and AI tooling** (tiktoken, prompt engineering)
- **Write maintainable, well-structured Python** following SOLID principles

I'm currently looking for opportunities in software engineering. If you're interested in my work, feel free to reach out.

📧 **Contact**: [GitHub Profile](https://github.com/gabriel-klettur)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Requirements

- **Python 3.10+**

### Python Dependencies

- `customtkinter` — Modern desktop UI framework
- `tiktoken` — OpenAI token counting
- `colorama` — Terminal color output
- `pytest` — Testing framework
