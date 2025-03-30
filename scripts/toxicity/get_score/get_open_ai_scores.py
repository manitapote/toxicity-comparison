from openai import OpenAI
import pandas as pd

client = OpenAI(
  organization='xxx',
  project='xxx',
)

def get_open_ai_scores(text):
    try:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=f"{text}",
        )
        
        api_score = response.results[0].category_scores
    
        scores = {
            'harassment': api_score.harassment,
            'harassment_threatening': api_score.harassment_threatening,
            'hate':  api_score.hate,
            'hate_threatening': api_score.hate_threatening,
            'illicit': api_score.illicit,
            'illicit_violent': api_score.illicit_violent,
            'self_harm': api_score.self_harm,
            'self_harm_instructions': api_score.self_harm_instructions,
            'self_harm_intent': api_score.self_harm_intent,
            'sexual': api_score.sexual,
            'sexual_minors': api_score.sexual_minors,
            'violence': api_score.violence,
            'violence_graphic': api_score.violence_graphic,
            'harassment_threatening': api_score.harassment_threatening,
            'hate_threatening': api_score.hate_threatening,
            'illicit_violent': api_score.illicit_violent,
            'self_harm_intent': api_score.self_harm_intent,
            'self_harm_instructions': api_score.self_harm_instructions,
            'self_harm': api_score.self_harm,
            'sexual_minors': api_score.sexual_minors,
            'violence_graphic': api_score.violence_graphic
        }
    except Exception as e:
        scores = {
            'harassment': None,
            'harassment_threatening': None,
            'hate': None,
            'hate_threatening': None,
            'illicit': None,
            'illicit_violent': None,
            'self_harm': None,
            'self_harm_instructions': None,
            'self_harm_intent': None,
            'sexual': None,
            'sexual_minors': None,
            'violence': None,
            'violence_graphic': None,
            'harassment_threatening': None,
            'hate_threatening': None,
            'illicit_violent': None,
            'self_harm_intent': None,
            'self_harm_instructions': None,
            'self_harm': None,
            'sexual_minors': None,
            'violence_graphic': None
        }
        
    return scores


def get_openai_scores(df_rt_org):
    all_row = []
    for index, row in df_rt_org.iterrows():
        scores = get_open_ai_scores(row['text'])
        
        scores['linked_tweet'] = row['linked_tweet']
        scores['data_lang'] = row['data_lang']
        
        all_row.append(scores)

        print(len(all_row))
    
    df_scores = pd.DataFrame(all_row)
  
    df_scores.to_pickle(
        './../data/scores/control_open_ai_scores.pkl.gz'
    )


def main():
    df_rt_org = pd.read_pickle(
        './../data/posts/control_retweet_original.pkl.gz'
    )
    print(len(df_rt_org))
    
    get_openai_scores(df_rt_org)

main()