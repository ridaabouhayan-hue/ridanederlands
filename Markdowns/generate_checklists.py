# -*- coding: utf-8 -*-
import json
import os

# Paths
workspace_dir = r"c:\Users\Rabou\Mijn Drive\HTML FILES"
opmaat_path = os.path.join(workspace_dir, "checklist_de_opmaat.html")

# Import the data
import sys
sys.path.append(os.path.join(workspace_dir, "Markdowns"))
from taalcompleet_a1_data import a1_topics, a1_quizzes
from taalcompleet_a2_data import a2_topics, a2_quizzes

# Load template
with open(opmaat_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Let's find the start of grammarTopics and end of topicQuizData in the template
# The template has:
#    const grammarTopics = [ ...
#    ];
#
#    const topicQuizData = { ...
#    };
#
#    let quizState = {};

start_topics_marker = "const grammarTopics = ["
end_topics_marker = "];"
start_quiz_marker = "const topicQuizData = {"
end_quiz_marker = "};"

# We will cut the template into three parts:
# Part 1: everything before "const grammarTopics = ["
# Part 2: everything between "const topicQuizData = {" and "let quizState = {};"
# (Wait, actually we can just split at "const grammarTopics = [" and "let quizState = {};")

split_idx1 = template.find("const grammarTopics = [")
split_idx2 = template.find("let quizState = {};")

if split_idx1 == -1 or split_idx2 == -1:
    print("Error: could not find script boundaries in template!")
    sys.exit(1)

part_header = template[:split_idx1]
part_footer = template[split_idx2:]

def generate_checklist(filename, title, book_name, total_topics, topics_list, quizzes_dict, storage_prefix, color_gradient):
    # Prepare header
    header = part_header
    
    # Replace titles and meta
    header = header.replace(
        "<title>Grammatica Checklist & Zinnenbouwer (De Opmaat) — NT2</title>",
        f"<title>Grammatica Checklist ({book_name}) — NT2</title>"
    )
    header = header.replace(
        "<h1>📋 Grammatica Checklist (De Opmaat)</h1>",
        f"<h1>📋 Grammatica Checklist ({book_name})</h1>"
    )
    header = header.replace(
        "Volg je voortgang door alle 31 grammaticasystemen van De Opmaat af te vinken. Gebruik onderaan de zinnenbouwer om te oefenen!",
        f"Volg je voortgang door alle {total_topics} grammaticasystemen van {book_name} af te vinken. Klik op een onderwerp om te oefenen!"
    )
    header = header.replace(
        '<span id="completed-count">0</span> van de 31 onderwerpen beheerst',
        f'<span id="completed-count">0</span> van de {total_topics} onderwerpen beheerst'
    )
    
    # Replace category tabs
    opmaat_tabs = """    <div class="tabs" id="category-tabs">
        <button class="tab-btn active" onclick="switchCategory('all')">Alles tonen</button>
        <button class="tab-btn" onclick="switchCategory('cat1')">Thema 1 & 2</button>
        <button class="tab-btn" onclick="switchCategory('cat2')">Thema 3 & 4</button>
        <button class="tab-btn" onclick="switchCategory('cat3')">Thema 5 & 6</button>
        <button class="tab-btn" onclick="switchCategory('cat4')">Thema 7 & 8</button>
        <button class="tab-btn" onclick="switchCategory('cat5')">Thema 9 & Werk</button>
    </div>"""
    
    new_tabs = f"""    <div class="tabs" id="category-tabs">
        <button class="tab-btn active" onclick="switchCategory('all')">Alles tonen</button>
        <button class="tab-btn" onclick="switchCategory('cat1')">Thema 1 & 2</button>
        <button class="tab-btn" onclick="switchCategory('cat2')">Thema 3 & 4</button>
        <button class="tab-btn" onclick="switchCategory('cat3')">Thema 5 & 6</button>
        <button class="tab-btn" onclick="switchCategory('cat4')">Thema 7 & 8</button>
    </div>"""
    
    header = header.replace(opmaat_tabs, new_tabs)
    
    # Apply color gradient overrides if needed
    if color_gradient:
        # opmaat has: radial-gradient(ellipse at 10% 10%, rgba(59, 130, 246, 0.06) 0%, transparent 50%), radial-gradient(ellipse at 90% 90%, rgba(230, 126, 34, 0.06) 0%, transparent 50%)
        # background: linear-gradient(90deg, var(--accent-blue), var(--accent-green));
        header = header.replace("rgba(59, 130, 246, 0.06)", color_gradient[0])
        header = header.replace("rgba(230, 126, 34, 0.06)", color_gradient[1])
        header = header.replace("linear-gradient(135deg, var(--accent-blue), var(--accent-purple))", f"linear-gradient(135deg, {color_gradient[2]}, {color_gradient[3]})")
        header = header.replace("linear-gradient(90deg, var(--accent-blue), var(--accent-green))", f"linear-gradient(90deg, {color_gradient[2]}, {color_gradient[4]})")
        header = header.replace("var(--accent-blue)", color_gradient[2])

    # Prepare footer
    footer = part_footer
    footer = footer.replace("opmaat_topic_", storage_prefix)
    
    # Format data lists
    topics_js = "const grammarTopics = " + json.dumps(topics_list, indent=4, ensure_ascii=False) + ";\n\n"
    quizzes_js = "const topicQuizData = " + json.dumps(quizzes_dict, indent=4, ensure_ascii=False) + ";\n\n"
    
    full_html = header + topics_js + quizzes_js + footer
    
    output_path = os.path.join(workspace_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated {filename} successfully.")

# Colors for A1: Green theme
# 1. rgba(16, 185, 129, 0.06) (green shadow)
# 2. rgba(139, 92, 246, 0.06) (purple shadow)
# 3. #10b981 (accent green/teal)
# 4. #8b5cf6 (accent purple)
# 5. #3b82f6 (accent blue)
a1_gradient = ["rgba(16, 185, 129, 0.06)", "rgba(139, 92, 246, 0.06)", "#10b981", "#8b5cf6", "#3b82f6"]

# Colors for A2: Violet/Rose theme
# 1. rgba(139, 92, 246, 0.06) (purple shadow)
# 2. rgba(244, 63, 94, 0.06) (rose shadow)
# 3. #8b5cf6 (accent purple/violet)
# 4. #f43f5e (accent rose)
# 5. #10b981 (accent green)
a2_gradient = ["rgba(139, 92, 246, 0.06)", "rgba(244, 63, 94, 0.06)", "#8b5cf6", "#f43f5e", "#10b981"]

generate_checklist(
    filename="checklist_taalcompleet_a1.html",
    title="Grammatica Checklist (TaalCompleet A1) — NT2",
    book_name="TaalCompleet A1",
    total_topics=29,
    topics_list=a1_topics,
    quizzes_dict=a1_quizzes,
    storage_prefix="taalcompleet_a1_topic_",
    color_gradient=a1_gradient
)

generate_checklist(
    filename="checklist_taalcompleet_a2.html",
    title="Grammatica Checklist (TaalCompleet A2) — NT2",
    book_name="TaalCompleet A2",
    total_topics=31,
    topics_list=a2_topics,
    quizzes_dict=a2_quizzes,
    storage_prefix="taalcompleet_a2_topic_",
    color_gradient=a2_gradient
)
