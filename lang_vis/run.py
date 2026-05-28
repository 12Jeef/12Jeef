import os
import subprocess
import re
import matplotlib.pyplot as plt

this_path = os.path.abspath(__file__)
dir_path = os.path.dirname(this_path)
repo_path = os.path.dirname(dir_path)
projs_path = os.path.dirname(repo_path)

out = subprocess.run(
    [
        "scc",
        ".",
        '--exclude-dir=".git,node_modules,dist,build"',
        '--exclude-ext="out,opt,inp,svg,md,json,js,html"',
        "--wide",
    ],
    capture_output=True,
    text=True,
    cwd=projs_path,
).stdout

lines = out.split("\n")

header = re.split("\\s+", lines[1])
lines = [
    [
        float(value) if i == len(header) - 1 else int(value) if i > 0 else value
        for i, value in enumerate(re.split("\\s{2,}", line))
    ]
    for line in lines[3:-10]
]

lang_i = header.index("Language")

i = 0
while i < len(lines):
    if lines[i][lang_i] in (
        "Plain Text",
        "SVG",
        "Markdown",
        "JSON",
        "JavaScript",
        "HTML",
    ):
        lines.pop(i)
    else:
        i += 1

n = 7

langs = [line[lang_i] for line in lines[:n]]
code_i = header.index("Code")
codes = [line[code_i] for line in lines[:n]]

langs.append("Other")
codes.append(sum(line[code_i] for line in lines[n:]))

fig, ax = plt.subplots()
ax.pie(codes, labels=langs)

plt.show()
