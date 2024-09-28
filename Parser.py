from GoogleOCR import OCR
import re
from itertools import product


words = []


def select_with_query(query):
    # Regular expression to match multiple 'with' clauses and a complex 'where' condition
    m = re.match(r"select (.*) from (.*) as (.*) with (.*) where (.*)", query)

    if m:
        groups = m.groups()

        fields = groups[0]
        collection = groups[1]
        alias = groups[2]

        with_many = groups[3].split(",")

        with_aliases = []
        with_collections = []
        for w in with_many:
            w_col, w_alias = w.strip().split(" as ")
            with_collections.append(w_col.strip())  # e.g., 'keys', 'prices'
            with_aliases.append(w_alias.strip())  # e.g., 'key', 'price'

        filter_condition = groups[4]  # e.g., '1400 < word.center.x < 1500'

        zip_statement = (
            f"({alias}, {', '.join(with_aliases)})"  # e.g., '(word, key, price)'
        )
        product_statement = f"({collection}, {', '.join(with_collections)})"  # e.g., '(words, keys, prices)'

        exec_query = (
            f"from itertools import product\ndef query():\n\tglobal {fields}\n\t"
            f"{fields} = [{alias} for {zip_statement} in product{product_statement} "
            f"if {filter_condition}]\nquery()"
        )

        execute(exec_query)
        return


def select_query(query):
    if "with" in query:
        select_with_query(query)
        return

    m = re.match(
        "select (.*) from (.*) as (.*) where (.*)",
        query,
    )
    if not m:
        return
    groups = m.groups()
    exec_query = f"def query():\n\tglobal {groups[0]}\n\t{groups[0]} = [{groups[2]} for {groups[2]} in {groups[1]} if {groups[3]}]\nquery()"
    execute(exec_query)
    return None


def export_query(query):
    m = re.match(
        "export (.*) as (.*)",
        query,
    )
    if m:
        groups = m.groups()
        exec_query = f"def query():\n\tglobal output\n\toutput['{groups[1]}'] = [word for word in {groups[0]}]\nquery()"
        execute(exec_query)
        return None


def end_query(string):
    if string == "end":
        execute(
            "import json\nwith open('output.json', 'w+') as file:\n\tfile.write(json.dumps(output))"
        )
        return


def set_query(string):
    m = re.match(
        "set (.*)",
        string,
    )
    if not m:
        return
    groups = m.groups()
    exec_query = (
        f"def query():\n\tglobal {groups[0].split()[0]}\n\t{groups[0]}\nquery()"
    )
    execute(exec_query)
    return


queries = [
    {"keyword": "select", "function": select_query},
    {"keyword": "export", "function": export_query},
    {"keyword": "set", "function": set_query},
    {"keyword": "end", "function": end_query},
]


pdf_file = ""


def set_pdf(pdf_file_path):
    global pdf_file
    global words

    ocr = OCR(pdf_file_path)
    words = ocr.get_words()
    pdf_file = pdf_file_path


def get_pdf_file_path():
    return pdf_file


def get_words():
    return words


output = {}


def execute(string):
    global output
    exec(string)
    return output


def decode(string):
    keyword = string.split()[0]
    for query in queries:
        if query["keyword"] == keyword:
            return query["function"](string)
    return None


def query(query):
    exec_query = f"def query():\n\tglobal output\n\ttry: print(output)\n\texcept: output = dict()\nquery()"
    execute(exec_query)
    decode(query)
