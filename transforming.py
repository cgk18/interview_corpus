import os
import glob
import pandas as pd
'''
def read_all_csv_from_folder(folder_path):
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    dataframes = []
    
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
        
    return dataframes

folder_path = "df_tagged"
dfs = read_all_csv_from_folder(folder_path)
# print(dfs[0].head)
'''
'''
Testing 
'''
interview_1 = pd.read_csv('df_tagged/Interview 01 Transcript tagged.csv')

def combine_chunks(df, speaker_col='Speaker', text_col='Dialogue'):
    # Remove rows where speaker is 'Unknown'
    df = df[~df[speaker_col].str.contains('Unknown', na=False)]
    
    chunked_rows = []
    current_speaker = None
    current_text_list = []

    for _, row in df.iterrows():
        speaker = row[speaker_col]
        text = row[text_col]

        if speaker != current_speaker:
            # If we already have a chunk, append it before starting a new one.
            if current_text_list:
                combined_text = " ".join(current_text_list)
                chunked_rows.append([current_speaker, combined_text])
            # Update to the new speaker and start a new text list.
            current_speaker = speaker
            current_text_list = [text]
        else:
            # Same speaker, just append the text.
            current_text_list.append(text)

    # Append the final chunk after the loop
    if current_text_list:
        combined_text = " ".join(current_text_list)
        chunked_rows.append([current_speaker, combined_text])

    return pd.DataFrame(chunked_rows, columns=[speaker_col, text_col])

print(combine_chunks(interview_1)) # works well! 


'''
Rule-Based Classification
'''

topic_keywords = {
    "Background": ["introduce", "from", "education", "upbringing"],
    "Current Job": ["job", "role", "position", "work", "coworker", "client"],
    "Race and Gender Dynamics": ["race", "gender", "diverse", "discrimination", "stereotype"],
    "Emotionality": ["feel", "emotion", "burnout", "stress", "exhausted"],
    "Specific Scenarios": ["example", "instance", "describe a time", "scenario"],
    "Covid": ["COVID", "pandemic", "lockdown", "virus"],
    "Closing Questions": ["anything else", "thank you", "recommend", "closing"]
}

def classify_chunk_rule_based(chunk_text):
    scores = {topic: 0 for topic in topic_keywords}
    lower_text = chunk_text.lower()

    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in lower_text:
                scores[topic]+=1
    
    return max(scores, key=scores.get) if any(scores.values()) else "Uncategorized"


'''
Trial of the rule based approach
'''

chunked_df = combine_chunks(interview_1)
chunked_df['Topic'] = chunked_df.apply(
    lambda row: classify_chunk_rule_based(row['Dialogue']) if row['Speaker'] == 'Interviewer' else None, 
    axis=1
)
print(chunked_df)

chunked_df.to_csv("topic_modeling_test/chunked_df.csv",index=False)



'''
Zero-shot classification
'''


'''
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

candidate_labels = [
    "Background", "Current Job", "Race and Gender Dynamics",
    "Emotionality", "Specific Scenarios", "Covid", "Closing Questions"
]

def classify_chunk_zero_shot(chunk_text):
    result = classifier(chunk_text, candidate_labels)
    return result["labels"][0]'''