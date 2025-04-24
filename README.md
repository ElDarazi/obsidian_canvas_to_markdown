Here’s the cleaned-up version of your README-friendly description:

---

# Canvas to Markdown Converter

This Python script converts Obsidian `.canvas` files (in JSON format) into readable Markdown documents. It extracts nodes and edges from the canvas file, converting them into a linear document format while preserving the hierarchy.

## Features

- Converts `.canvas` nodes into headers, lists, and embeds.
- Preserves markdown formatting within canvas nodes.
- Supports embedding images, files, and URLs.
- Outputs a `.md` file alongside the original `.canvas` file.

---

## 🧩 How It Works

1. **Prompt the user** for the `.canvas` file path.
2. **Parse the file** and extract all nodes and edges.
3. **Identify root nodes** (nodes without parents).
4. **Recursively convert** each node to Markdown:
    - Headers for nesting levels (up to H6).
    - List items for deeper levels beyond H6.
    - Embeds for file/image links.
    - Markdown links for web URLs.
5. **Output the final document** to a `.md` file alongside the original `.canvas` file.

---

## 🔧 Main Functions

### `prompt_for_file()`
- Prompts the user for a `.canvas` file path.
- Cleans the input (e.g., strips quotes or ampersands).
- Returns a clean file path.

---

### `parse_canvas_file(file_path)`
- Opens the `.canvas` file.
- Parses the JSON and extracts:
    - `nodes`: The content blocks.
    - `edges`: Relationships between nodes.

---

### `generate_markdown(nodes, edges)`
- Converts nodes into readable Markdown:
    - `#` headers for levels 1–6.
    - `-` list items for levels beyond 6.
- Supports:
    - Text content.
    - Internal file embeds: `[[filename]]`.
    - Image embeds: `![[image.png]]`.
    - Web URLs: `[webpage](url)`.
- Uses a recursive function to maintain hierarchy via indentation.

---

### `write_markdown_to_file(markdown, original_file_path)`
- Creates a `.md` file using the original `.canvas` file name.
- Writes the converted Markdown to disk.

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

## ✅ Example Usage

```bash
$ python canvas_to_markdown.py
Please provide the path to your .canvas file: canvas_files/your-file.canvas
```

---

## 💡 Tips for Canvas Note-Taking

- Use **clear first lines** in each node (they become headings).
- Avoid using headers inside node content, as Markdown already uses levels for this.
- Images and internal links will auto-convert if marked properly:
    - `[[Home.md]]` → internal link.
    - `![[image.png]]` → image embed.
    - `https://...` → link embed.
- Node depth controls indentation/heading level.

---

## 📌 Known Features

- ✅ Supports H1 to H6 headings.
- ✅ Converts beyond H6 to indented bullet lists.
- ✅ Auto-detects image and file types.
- ✅ Handles blank nodes.
- ✅ Properly embeds URLs and Obsidian links.

---

## Optional Tweaks for Embed Behavior

To adjust how file links are handled, you can tweak the code below:

```python
# Embed content after header
if 'type' in node_data:
    node_type = node_data['type']
    if node_type == 'file' and 'file' in node_data:
        file_name = node_data['file']
        name = os.path.splitext(os.path.basename(file_name))[0]
        if file_name.endswith(('png', 'jpg', 'jpeg', 'gif')):
            embed_line = f"![[{file_name}]]\n"  # For image embeds
        else:
            embed_line = f"[[{file_name}|{name}]]\n"  # For regular file links
    elif node_type == 'link' and 'url' in node_data:
        url = node_data['url']
        match = re.search(r'www\.([a-zA-Z0-9\-]+)\.', url)
        name = match.group(1) if match else "webpage"
        embed_line = f"[{name}]({url})\n"  # For link embeds
```

If you prefer files to be **embedded** rather than **linked**, modify this line:

```python
embed_line = f"![[{file_name}|{name}]]\n"
```

This will embed the file instead of linking to it.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let me know if you'd like any further changes or additions!
