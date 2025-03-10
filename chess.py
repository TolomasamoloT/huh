import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import (
    ConversationLimitException,
    DuckDuckGoSearchException,
    RatelimitException,
    TimeoutException,
)

url = "https://www.thechesswebsite.com/chess-openings/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


table = soup.select_one("body > div:nth-of-type(2) > section > div > div > div > div:nth-of-type(3) > div")

all_As = table.find_all("a")

imgs = []
names = []
for a in all_As:
    # Extract the link (href attribute)
    link = a["href"]

    # Extract the image URL (src attribute of <img>)
    image_src = a.find("img")["src"]

    # Extract the title text inside <h5>
    title = a.find("h5").text

    imgs.append(image_src)
    names.append(title)

ddgs = DDGS()

def opening(op_name):
    with open(f"openings/{op_name.replace(' ', '-')}.md", "w", encoding="utf-8") as file:
        file.write("---\n")
        file.write("layout: default\n")
        file.write(f"title: {op_name}\n")
        file.write("---\n")

        try:
            results = list(ddgs.text(op_name.lower(), max_results=3))

            file.write("# " + op_name + "\n")

            for result in results:
                page_title = result.get("title", "No title")
                href = result.get("href", "No link")
                snippet = result.get("body", "No description")

                file.write(f"- ## **{page_title}** \n")
                file.write("\n---\n")
                file.write(f"### Desc: \n {snippet} \n")
                file.write(f"### Read more : [here]({href}) \n")

            file.write("\n\n")
            # file.write("[← Back to the list](../chess-openings.md)")
        except DuckDuckGoSearchException as e:
            file.write("# " + op_name + "\n")
            file.write("\n ## duck error:\n")
            file.write(f"\n {e} \n")


def write_row_bttr(src_img, src_nam, start, f):
    for i in range(4):
        if start + i < len(src_nam):
            opening(src_nam[start + i])
            f.write(
                f'|[<img src="{src_img[start + i].replace(" ", "-")}" '
                f'alt="failed to load image" width="320">'
                f'<br>{src_nam[start + i]}](openings/{src_nam[start + i].replace(" ", "-")}.html)'
            )
            print("done " + src_nam[start + i])
        else:
            f.write('|')
    f.write('|\n')


from pathlib import Path

def to_md():

    directory = Path("openings")
    directory.mkdir(parents=True, exist_ok=True)

    with open("chess-openings.md", "w", encoding="utf-8") as file:
        file.write("---\n")
        file.write("layout: default\n")
        file.write("title: Chess Openings List\n")
        file.write("---\n")

        file.write("# Chess Openings List\n\n")
        file.write("[←  Back to Home](index.html) \n")
        file.write("\n---\n")

        write_row_bttr(imgs, names, 0, file)
        file.write('|:---:|:---:|:---:|:---:|\n')

        j = 4
        while j < len(imgs):
            write_row_bttr(imgs, names, j, file)
            j += 4


def make_index():
    with open("index.md", "w", encoding="utf-8") as file:
        file.write("---\n")
        file.write("layout: default\n")
        file.write("title: Chess Openings\n")
        file.write("---\n")

        file.write("# Chess Openings\n")
        file.write("\n---\n")

        result = DDGS().chat("Explain what a chess opening is and its importance in chess")

        file.write(f"\n{result} <br>\n\n")

        file.write("[→ Go to Chess Openings List](chess-openings.html)")


def to_md_crippled():

    # directory = Path("openings")
    # directory.mkdir(parents=True, exist_ok=True)

    with open("chess-openings.md", "w", encoding="utf-8") as file:
        file.write("---\n")
        file.write("layout: default\n")
        file.write("title: Chess Openings List\n")
        file.write("---\n")

        file.write("# Chess Openings List\n\n")
        file.write("[←  Back to Home](index.html) \n")
        file.write("\n---\n")

        file.write('<table>\n')

        j = 0
        while j < len(imgs):
            write_row_worse(imgs, names, j, file)
            j += 4
        file.write('</table>\n')

def write_row_worse(src_img, src_nam, start, f):
    f.write('    <tr>\n')
    for i in range(4):
        if start + i < len(src_nam):
            # opening(src_nam[start + i])
            f.write('        <td style="width:25%">')
            f.write(
                f'<a href="openings/{src_nam[start + i].replace(" ", "-")}.html"> <img src="{src_img[start + i].replace(" ", "-")}" '
                f'alt="failed to load image" width="320">'
                f'<br>{src_nam[start + i]} </a>'
            )
            f.write('</td>\n')
            print("done " + src_nam[start + i])
        else:
            f.write('        <td style="width:25%"></td>\n')
    f.write('    </tr>\n')


if __name__ == '__main__':
    # make_index()
    # to_md()
    to_md_crippled()