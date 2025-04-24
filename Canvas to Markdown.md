![[Canvas to Markdown.py]]

# Canvas to Markdown: Canvas Guide

## Headers
- Each node becomes a section in Markdown.
- Nodes are treated as H1 to H6.
- Beyond H6, nodes are treated as lists and sub-lists.

## Markdown
- Canvas nodes support markdown. When converted, markdown will be preserved as-is.

> [!warning] Headers Inside a Node
> Headers inside a node are considered regular markdown. Using them will create a break in the node flow once converted.

## Header Titles
- The first line in a node is used as the header title.
- File name and image name are used as header titles for embeds.
- Domain names are used as header titles for links.

## Optional Tweak

To adjust the embed behavior in the code section, you can tweak how file links are handled. Here’s the relevant code:

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

If you prefer files to be **embedded** rather than **linked**, add `!` to this line:

```
embed_line = f"![[{file_name}|{name}]]\n"
```

This will embed the file instead of linking to it.


# Canvas to Markdown Converter Guide

This script converts Obsidian `.canvas` files (JSON format) into readable markdown documents by extracting nodes and edges, then converting them into a linear document format while preserving hierarchy.

---

## 🧩 How It Works

1. **Prompt the user** for a `.canvas` file path.
    
2. **Parse the file** and extract all nodes and edges.
    
3. **Identify root nodes** (nodes without parents).
    
4. **Recursively convert** each node to Markdown using:
    
    - Headers for nesting levels (up to H6)
        
    - List items for deeper levels beyond H6
        
    - Embeds for file/image links
        
    - Markdown links for web URLs
        
5. **Output the final document** to a `.md` file alongside the original `.canvas` file.
    

---

## 🛠️ File Structure

```text
canvas_to_markdown.py
📂 canvas_files/
  └── your-file.canvas
  └── your-file.md
```

---

## 🔧 Main Functions

### `prompt_for_file()`

- Prompts user for the `.canvas` file path.
    
- Cleans the input (e.g., strips quotes or ampersands).
    
- Returns a clean file path.
    

---

### `parse_canvas_file(file_path)`

- Opens the `.canvas` file.
    
- Parses JSON and extracts:
    
    - `nodes`: The content blocks.
        
    - `edges`: Links showing relationships between nodes.
        

---

### `generate_markdown(nodes, edges)`

- Converts nodes into readable markdown using:
    
    - `#` headers for levels 1–6
        
    - `-` list items for levels beyond 6
        
- Supports:
    
    - Text content
        
    - Internal file embeds: `[[filename]]`
        
    - Image embeds: `![[image.png]]`
        
    - Web URLs: `[webpage](url)`
        
- Uses a recursive function to maintain hierarchy via indentation.
    

---

### `write_markdown_to_file(markdown, original_file_path)`

- Creates a `.md` file using the original `.canvas` file name.
    
- Writes the converted markdown to disk.
    

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

## ✅ Example Use

```bash
$ python canvas_to_markdown.py
Please provide the path to your .canvas file: canvas_files/your-file.canvas
```

---

## 💡 Tips for Canvas Note-Taking

- Use **clear first lines** in each node (they become headings).
    
- Avoid headers inside node content (Markdown already uses levels).
    
- Images and internal links will auto-convert if marked properly:
    
    - `[[Home.md]]` → internal link
        
    - `![[image.png]]` → image embed
        
    - `https://...` in Chrome-pasted format → link embed
        
- Node depth controls indentation/heading level.
    

---

## 📌 Known Features

- ✅ Supports H1 to H6 headings
    
- ✅ Converts beyond H6 to indented bullet lists
    
- ✅ Auto-detects image and file types
    
- ✅ Handles blank nodes
    
- ✅ Properly embeds URLs and Obsidian links
    
