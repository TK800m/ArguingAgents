import pandas as pd
from detect_and_score import *
from scraper import *


def test_on_reddit(detect_model, threshold, score_model, word2vec, reddit_data, print_results=False):
    topic_accuracies = []
    all_topics = []
    for i in range(len(reddit_data)):
        print("---------------------------Processing topic: {0}-----------------------------------".format(i))
        # get the delta posts
        delta_posts = reddit_data[i][3]
        normal_posts = reddit_data[i][2]
        n_delta_posts = len(delta_posts)
        # get the normal posts, WITHOUT the delta posts
        normal_posts_filtered = []
        for normal_post in normal_posts:
            is_delta = False
            for delta_post in delta_posts:
                if (normal_post == delta_post):
                    is_delta = True

            if (is_delta == False):
                normal_posts_filtered.append(normal_post)

        n_normal_posts = len(normal_posts_filtered)

        # get topic and store for later
        topic = reddit_data[i][0]
        # score normal posts
        normal_scores = []

        for post in normal_posts_filtered:
            score = detect_and_score(detect_model, threshold, score_model, post, topic, word2vec, print_results)
            normal_scores.append(score)

        print("Normal post scores:", normal_scores)

        # score delta posts
        delta_scores = []
        for post in delta_posts:
            score = detect_and_score(detect_model, threshold, score_model, post, topic, word2vec, print_results)
            delta_scores.append(score)

        print("Delta post scores:", delta_scores)

        # check for each delta post how many normal scores are lower than its own score
        total_accuracy = 0
        for delta_score in delta_scores:
            correct = 0
            for normal_score in normal_scores:
                if (delta_score > normal_score):
                    correct += 1

            accuracy = correct / n_normal_posts

            total_accuracy += accuracy
        total_accuracy /= n_delta_posts

        print("Topic", i, ":", total_accuracy)
        all_topics.append(topic)
        topic_accuracies.append(total_accuracy)
    return topic_accuracies, all_topics


# run the argument mining pipeline
def run():
    print("Thanks for using the argument miner.")
    print("The Word2vec model will now be loaded. This can take a while.")
    print("Loading Word2vec model...")
    # load the word2vec model
    word2vec = gensim.models.KeyedVectors.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True)
    print("Word2vec model loaded!")
    print("Now loading the detection and quality LSTM's...")
    # Load the LSTM models
    score_model = keras.models.load_model("models/argument_quality.h5")
    detect_model = keras.models.load_model("models/bilstm_cos.h5")
    print("LSTM models loaded!")
    print("Please enter the amount of Reddit CMV topics that you want to process.")
    n_topics = int(input("> "))
    # extract reddit topics with posts
    reddit_data = makeDF(range(0, n_topics, 1))
    print("Amount of topics scraped:", len(reddit_data))

    print("Topics will now be processed by the pipeline.")
    test_on_reddit(detect_model, 0.1, score_model, word2vec, reddit_data, True)




if __name__ == "__main__":
    run()


