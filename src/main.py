import os
import shutil

from markdownblock import markdown_to_html_node, extract_title


def main():
    copy_static_to_public()
    generate_pages_recursive("content/", "template.html", "public/")


def copy_static_to_public():
    public_path = "./public/"
    static_path = "./static/"

    if not os.path.exists(static_path):
        raise Exception("Error: The static folder doesn't exist")

    shutil.rmtree(public_path)
    os.mkdir(public_path)

    copy_dir_to_dir(static_path, public_path)


def copy_dir_to_dir(source: str, destination: str):

    for item in os.listdir(source):
        src_joined_path = os.path.join(source, item)
        tgt_joined_path = os.path.join(destination, item)

        if os.path.isfile(src_joined_path):
            shutil.copy(src_joined_path, tgt_joined_path)
        else:
            os.mkdir(tgt_joined_path)
            copy_dir_to_dir(src_joined_path, tgt_joined_path)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if from_path is None or template_path is None or dest_path is None:
        raise Exception("Error: All paths must have a value")

    with open(from_path) as f:
        file_contents = f.read()
        f.close()

    html_node = markdown_to_html_node(file_contents)
    title = extract_title(html_node)

    with open(template_path) as f:
        template_contents = f.read()
        f.close()

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_node.to_html())

    dest_path_split = dest_path.split("/")
    if not os.path.isfile(dest_path_split[0]):

        if dest_path_split[0] == ".":
            dest_path_split = dest_path_split[1:]

        path = ""
        for i in range(len(dest_path_split) - 1):
            path = os.path.join(path, dest_path_split[i])
            if not os.path.exists(path):
                os.mkdir(path)

    with open(dest_path, "w+") as f:
        f.write(template_contents)
        f.close()


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):

    for item in os.listdir(dir_path_content):

        path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(path):
            generate_pages_recursive(path, template_path, dest_path)
        elif os.path.isfile(path) and ".md" in path:
            generate_page(path, template_path, dest_path[:-3] + ".html")


main()
