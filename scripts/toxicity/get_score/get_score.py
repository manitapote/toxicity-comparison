import pandas as pd
import time
from googleapiclient import discovery
import json
    
def test_toxicity(text, client):
    analyze_request = {
      'comment': { 
          'text': f'{text}'},
      'requestedAttributes': {'TOXICITY': {},
                              'SEVERE_TOXICITY': {},
                              'IDENTITY_ATTACK': {},
                              'INSULT': {},
                              'PROFANITY': {},
                              'THREAT': {}
                             }
    }
    
    response = client.comments().analyze(body=analyze_request).execute()

    return response


def get_all_scores(df_need, client, save_file):
    all_row = []
    i = 0
    for index, row in df_need.iterrows():
        try:
            score = test_toxicity(row['text'], client)
            score = score['attributeScores']
            
            row['INSULT'] = score['INSULT']['summaryScore']['value']
            row['THREAT'] = score['THREAT']['summaryScore']['value']
            row['TOXICITY'] = score['TOXICITY']['summaryScore']['value']
            row['SEVERE_TOXICITY'] = score['SEVERE_TOXICITY']['summaryScore']['value']
            row['PROFANITY'] = score['PROFANITY']['summaryScore']['value']
            row['IDENTITY_ATTACK'] = score['IDENTITY_ATTACK']['summaryScore']['value']
        except Exception as e:
            print(e)
            row['INSULT'] = None
            row['THREAT'] = None
            row['TOXICITY'] = None
            row['SEVERE_TOXICITY'] = None
            row['PROFANITY'] = None
            row['IDENTITY_ATTACK'] = None

        all_row.append(row)

        i += 1
        print(len(all_row))
        
        if i == 199:
        
            time.sleep(1)
            i = 0

            print(len(all_row))

    df_scores = pd.DataFrame(all_row)
    
    df_scores.to_pickle(save_file)

    print(df_scores)

def main():
    source_file='/N/slate/potem/project/narrativez/scripts/toxicity/data/remain/remain.pkl.gz'
    save_file = 
    '/N/slate/potem/project/narrativez/scripts/toxicity/data/scores/remain_score.pkl.gz'
    df_need = pd.read_pickle(source_file)

    API_KEY = 'XXX'
    client = discovery.build(
      "commentanalyzer",
      "v1alpha1",
      developerKey=API_KEY,
      discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
      static_discovery=False,
    )

    get_all_scores(df_need, client, save_file)


main()

