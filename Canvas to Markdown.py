import json
import os
import re

def prompt_for_file():
    # Get the path to the canvas file from the user input
    file_path = input("Please provide the path to your .canvas file: ").strip()
    
    # Clean up the path by removing any surrounding single quotes and other unexpected characters
    file_path = file_path.replace("'", "").replace("&", "").strip()
    
    print(f"Input as received: {file_path}")
    
    # Return the cleaned-up file path
    return file_path


def parse_canvas_file(file_path):
    # Open and parse the .canvas file as JSON
    with open(file_path, 'r') as file:
        canvas_data = json.load(file)
    
    # Return nodes and edges (Ensure that 'nodes' and 'edges' are in the JSON spec as described)
    nodes = canvas_data.get('nodes', [])
    edges = canvas_data.get('edges', [])
    return nodes, edges


import os
import re

def generate_markdown(nodes, edges):
    markdown = ""
    node_dict = {node['id']: node.get('text', '') for node in nodes}

    edges_dict = {}
    for edge in edges:
        parent = edge['fromNode']
        child = edge['toNode']
        if parent not in edges_dict:
            edges_dict[parent] = []
        edges_dict[parent].append(child)

    def create_markdown_node(node_id, level=1):
        nonlocal markdown
        node_data = next((node for node in nodes if node['id'] == node_id), {})
        node_text = node_data.get('text', '').strip()
        embed_line = ""
        header_written = False

        # Determine indentation if needed
        indent = "  " * (level - 7) if level > 6 else ""

        if node_text:
            node_text = node_text.replace('\\n', '\n').replace('\\t', '\t')
            lines = node_text.split("\n")
            first_line = lines[0].strip()

            if level <= 6:
                markdown += "#" * level + " " + first_line + "\n"
            else:
                markdown += indent + "- " + first_line + "\n"
            header_written = True

            for line in lines[1:]:
                line = line.strip()
                if line:
                    if level > 6:
                        markdown += indent + "  " + line + "\n"
                    else:
                        markdown += line + "\n"
        else:
            # If no text, try to use the embed name as header
            if 'type' in node_data:
                node_type = node_data['type']
                if node_type == 'file' and 'file' in node_data:
                    file_name = node_data['file']
                    name = os.path.splitext(os.path.basename(file_name))[0]
                    if level <= 6:
                        markdown += "#" * level + " " + name + "\n"
                    else:
                        markdown += indent + "- " + name + "\n"
                    header_written = True
                elif node_type == 'link' and 'url' in node_data:
                    url = node_data['url']
                    match = re.search(r'www\.([a-zA-Z0-9\-]+)\.', url)
                    name = match.group(1) if match else "webpage"
                    if level <= 6:
                        markdown += "#" * level + " " + name.capitalize() + "\n"
                    else:
                        markdown += indent + "- " + name.capitalize() + "\n"
                    header_written = True
            else:
                if level <= 6:
                    markdown += "#" * level + " \n"
                else:
                    markdown += indent + "- \n"

        # Embed content after header
        if 'type' in node_data:
            node_type = node_data['type']
            if node_type == 'file' and 'file' in node_data:
                file_name = node_data['file']
                name = os.path.splitext(os.path.basename(file_name))[0]
                if file_name.endswith(('png', 'jpg', 'jpeg', 'gif')):
                    embed_line = f"![[{file_name}]]\n"
                else:
                    embed_line = f"[[{file_name}|{name}]]\n"
            elif node_type == 'link' and 'url' in node_data:
                url = node_data['url']
                match = re.search(r'www\.([a-zA-Z0-9\-]+)\.', url)
                name = match.group(1) if match else "webpage"
                embed_line = f"[{name}]({url})\n"

        if embed_line:
            markdown += embed_line

        if node_id in edges_dict:
            for child_id in edges_dict[node_id]:
                create_markdown_node(child_id, level + 1)

    all_children = [child for sublist in edges_dict.values() for child in sublist]
    root_nodes = [node['id'] for node in nodes if node['id'] not in all_children]

    for root_node in root_nodes:
        create_markdown_node(root_node)

    return markdown


def write_markdown_to_file(markdown, original_file_path):
    # Create an output file path with the .md extension
    output_file_path = os.path.splitext(original_file_path)[0] + ".md"
    
    # Write the markdown content to the output file
    with open(output_file_path, 'w') as file:
        file.write(markdown)
    
    print(f"Markdown file has been saved to: {output_file_path}")


def main():
    # Get the path to the .canvas file
    canvas_file_path = prompt_for_file()
    
    # Parse the canvas file
    nodes, edges = parse_canvas_file(canvas_file_path)
    
    # Generate markdown from the nodes and edges
    markdown_content = generate_markdown(nodes, edges)
    
    # Save the generated markdown to a file
    write_markdown_to_file(markdown_content, canvas_file_path)


if __name__ == "__main__":
    main()
