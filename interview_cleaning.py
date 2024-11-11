"""
Chris Kim
updated Nov 10, 2024
"""

# package importation
from docx import Document 
import re
import pandas as pd



test_doc = Document("/Users/grealish/Desktop/AS - Anon. Interview Transcripts/Interview 01 Transcript.docx")
test_text = [para.text for para in test_doc.paragraphs if para.text.strip()]

# Identify the speaker as an interviewer or a participant.
dialogues = []
for line in test_text:
    if line.startswith("Interviewer:"):
        dialogues.append(("Interviewer",line.replace("Interviewer:","").strip()))
    elif re.match(r"Participant \d+:", line):
        participant_label = re.match(r"(Participant \d+):", line).group(1)
        dialogues.append((participant_label, line.replace(f"{participant_label}:", "").strip()))
    else:
        dialogues.append(("Unknown",line.strip()))

dialogues


test_df = pd.DataFrame(dialogues, columns = ["Speaker","Dialogue"])
test_df.head