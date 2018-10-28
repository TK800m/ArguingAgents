import gensim
import keras
import numpy as np
import nltk
from sklearn.metrics.pairwise import cosine_similarity

def encode_post(sentences, topic, word2vec):
    # given a list of sentences and the topic that the sentences
    # are related to, encode the sentences using the word2vec model
    # and compute the similarity of each word to the topic as
    # an additional feature for each word
    encoded_sentences = []
    
    # compute the average word vector of the topic, so that each word
    # from the sentences can be compared to the topic
    topic_words = topic.split()
    topic_word_vectors = []
    for word in topic_words:
        # check if the word exists in the word2vec dictionary
        if(word in word2vec):
                word_vector = word2vec[word]
         # else, map the word to a random, 300-dimensional vector
        else:
            word_vector = np.random.uniform(low = -0.01, high = 0.01, size = (300))
        topic_word_vectors.append(word_vector)
    topic_word_vectors = np.asarray(topic_word_vectors)
    # the average topic vector is the average of all the words in it, along each f
    # the 300 dimensions
    avg_topic_vector = np.mean(topic_word_vectors, axis = 0)
      
    # for every sentence in the post...
    for i in range(len(sentences)):
        # get the words of the sentence by means of tokanization
        # discarding punctuation marks
        words = []
        tokens = nltk.word_tokenize(sentences[i])
        for token in tokens:
            # only append actual words
            if(token[0] not in ".,:;[](){}!?-_`'~\"^/1234567890"):
                words.append(token)
                
        # store the word vectors into a sentence list
        encoded_sentence = []
                
        # turn the words into word vectors
        for word in words:
            # check if the word exists in the word2vec dictionary
            if(word in word2vec):
                    word_vector = word2vec[word]
             # else, map the word to a random, 300-dimensional vector
            else:
                word_vector = np.random.uniform(low = -0.01, high = 0.01, size = (300))
        
            # compute similarity between word and topic, then add this as the 
            # 301-th feature
            similarity = cosine_similarity([word_vector], [avg_topic_vector])
            word_vector = np.append(word_vector, similarity) 
            # add word to sentence list
            encoded_sentence.append(word_vector)
        encoded_sentence = np.asarray(encoded_sentence)
        encoded_sentences.append(encoded_sentence)
    # add encoded sentence to list of sentences      
    encoded_sentences = np.asarray(encoded_sentences)
        
    return encoded_sentences
        

def detect_arguments(model, threshold, post, topic, word2vec):
    # split text into sentences
    post_sentences = post.split(".")
    # encode the sentences
    encoded_sentences = encode_post(post_sentences, topic, word2vec)
     
    # create lists to store the classified arguments and non-arguments
    arguments = []
    non_arguments = []
    
    #print(len(post_sentences), len(encoded_sentences))
    #print(encoded_sentences[0])
    #print(encoded_sentences[1])
    
    # feed sentences into LSTM and get prediction
    for i in range(len(encoded_sentences)):
        n_words = encoded_sentences[i].shape[0]
        # skip empty sentences
        if(n_words > 0):
            n_features = encoded_sentences[i].shape[1]
            prediction = model.predict(encoded_sentences[i].reshape(1, n_words, n_features), batch_size=1, verbose=0)
            if(prediction > threshold):
                arguments.append((i, prediction, post_sentences[i]))
            else:
                non_arguments.append((i, prediction, post_sentences[i]))
        else:
             non_arguments.append((i, 0, post_sentences[i]))
            
    return arguments, non_arguments, encoded_sentences

def get_argument_quality(model, arguments, sentences, encoded_sentences):
    sentences = sentences.split(".")
    argument_scores = []
    # score each argument
    for arg in arguments:
        # take the index from the tuple
        idx = arg[0]
        # take the encoded sentence corresponding to this
        # argument
        encoded_sentence = encoded_sentences[idx]
        n_words = encoded_sentence.shape[0]
        n_features = encoded_sentence.shape[1]
        score = model.predict(encoded_sentence.reshape(1, n_words, n_features), batch_size=1, verbose=0)
        
        # multiply the argument score by the probability of the argument being an argument
        score *= arg[1]
        
        argument_scores.append((score[0], sentences[idx]))
    return argument_scores

def print_results(arguments, argument_scores, non_arguments, total_post_score):
    print("----------Good arguments-----------:")
    for i in range(len(arguments)):
        print("Probability:", arguments[i][1])
        print("Quality:", argument_scores[i][0])
        print(arguments[i][2])
        print()
    
    print("Total post quality:", total_post_score)
    
    print("----------Bad arguments-----------:")
    for i in range(len(non_arguments)):
        print("Probability:", non_arguments[i][1])
        print(non_arguments[i][2])
        print()
        
        
        
    
        
def detect_and_score(detect_model, threshold, score_model, post, topic, word2vec, print_arguments = False):
    # encode the sentences in the post and separate the arguments from the non-arguments
    arguments, non_arguments, encoded_sentences = detect_arguments(detect_model, threshold, post, topic, word2vec)
    #print("Arguments:", arguments)
    #print("Non-arguments:", non_arguments)
    # score the arguments
    argument_scores = get_argument_quality(score_model, arguments, post, encoded_sentences)
    total_post_score = calculate_score(argument_scores)
    if(print_arguments):
        print_results(arguments, argument_scores, non_arguments, total_post_score)
    return total_post_score

def calculate_score(arguments):
    score = 0
    if(len(arguments) == 0):
        return 0
    for arg in arguments:
        score += arg[0]
    return (score / len(arguments))[0]
    
    
    
    
    