from wordcloud import WordCloud
import pandas as pd
from matplotlib import pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
import random

def get_wordcloud(text):
    # wordcloud = WordCloud(width=1000, height=500,
    #                       background_color="#ffffff",
    #                       font_step='NotoNaskhArabic-Regular.ttf').generate(text)

    wordcloud = WordCloud(width=3000, height=2000, background_color="#ffffff", font_path='NotoNaskhArabic-Regular.ttf').generate(text)
    
    wordcloud.to_file("arabic_example.png")
    fig, ax = plt.subplots()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.figure(facecolor='k')
    plt.tight_layout(pad=0)
    fig.padding = 0
    # plt.gcf().set_facecolor('red')
    # plt.margins(0)
    plt.tight_layout(pad=0)
    for pos in ['right', 'top', 'bottom', 'left']:
        plt.gca().spines[pos].set_visible(False)

    # Selecting the axis-X making the bottom and top axes False.
    plt.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)

    # Selecting the axis-Y making the right and left axes False
    plt.tick_params(axis='y', which='both', right=False,
                    left=False, labelleft=False)
    for item in [fig, ax]:
        item.patch.set_visible(False)

    plt.show()
    # return fig

df = pd.read_csv("5k_translated.csv")
bruuuuh = random.randrange(0, len(df))
text = df.iloc[bruuuuh]['body']
text = arabic_reshaper.reshape(text)
text = get_display(text)

print(df.iloc[bruuuuh]['body_tr'])

get_wordcloud(text)
