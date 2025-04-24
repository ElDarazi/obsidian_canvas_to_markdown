# 📝 Canvas to Markdown Converter

Convert your Obsidian `.canvas` files into clean, readable Markdown documents while preserving structure and content.

---

## 📌 Features

- 🧠 Converts Canvas nodes to Markdown headings (up to H6)
- 📋 Uses lists for deeper hierarchies
- 🖼️ Supports embedded images, files, and web links
- 🔄 Auto-detects node structure from Canvas `.json`
- 💡 Preserves Markdown inside nodes

---

## 📂 File Structure

```
canvas_to_markdown.py
📁 canvas_files/
 ├── your-file.canvas
 └── your-file.md
```

---

## 🚀 How It Works

1. **Prompt** for the `.canvas` file path.
2. **Parse** the file and extract all `nodes` and `edges`.
3. **Identify root nodes** (nodes without incoming edges).
4. **Recursively convert** nodes to Markdown:
   - Headers (`#` to `######`) for depth 1–6
   - Bullet lists beyond H6
   - Embeds for files/images
   - Links for URLs
5. **Output** a `.md` file alongside the original `.canvas`.

---

## 🧠 Canvas Conversion Rules

### Headers

- Each **Canvas node** becomes a **Markdown section**
- Treated as `H1` to `H6` based on node depth
- Beyond `H6`, content becomes indented lists

> ⚠️ **Headers inside a node** are preserved as-is Markdown  
> These may cause flow breaks in the converted document

### Header Titles

- First line in each node → section header
- File/image nodes → name used as header
- Links → domain name becomes header

### Markdown Inside Nodes

- Markdown within nodes (bold, italic, lists, etc.) is preserved

---

## 🔧 Optional Tweak: Embed Behavior

To modify how file links are embedded, look for this code snippet:

```python
if node_type == 'file' and 'file' in node_data:
    file_name = node_data['file']
    name = os.path.splitext(os.path.basename(file_name))[0]
    if file_name.endswith(('png', 'jpg', 'jpeg', 'gif')):
        embed_line = f"![[{file_name}]]\n"  # image embed
    else:
        embed_line = f"[[{file_name}|{name}]]\n"  # file link
```

To **force embed** files instead of linking, change this line:

```python
embed_line = f"![[{file_name}|{name}]]\n"
```

---

## ⚙️ Key Functions

### `prompt_for_file()`

- Requests and cleans up the `.canvas` file path

### `parse_canvas_file(file_path)`

- Loads the `.canvas` JSON
- Extracts `nodes` and `edges`

### `generate_markdown(nodes, edges)`

- Recursively builds structured Markdown
- Supports headers, lists, file embeds, and URL links

### `write_markdown_to_file(markdown, original_file_path)`

- Creates a `.md` file alongside the original
- Writes the final Markdown output

---

## 🔄 Execution Flow

```python
def main():
    canvas_file_path = prompt_for_file()
    nodes, edges = parse_canvas_file(canvas_file_path)
    markdown_content = generate_markdown(nodes, edges)
    write_markdown_to_file(markdown_content, canvas_file_path)
```

---

## 💡 Usage Tips

- Use clear first lines for each node (they become headers)
- Avoid using multiple headers *inside* nodes
- Internal links and images are auto-detected:
  - `[[Note.md]]` → Markdown link
  - `![[image.png]]` → Image embed
  - `https://example.com` → Web link
- Node nesting controls indentation/heading level

---

## ✅ Supported Features

- [x] Markdown headings (`#` to `######`)
- [x] Indented bullet lists beyond H6
- [x] Auto file/image embed detection
- [x] Internal link + URL parsing
- [x] Handles blank or malformed nodes
