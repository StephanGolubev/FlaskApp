# use natural language toolkit
import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
import numpy as np
import time
stemmer = LancasterStemmer()


# 3 classes of training data

# 3 classes of training data
training_data = []
training_data.append({"class": "analis", "sentence": "UA auto send pageview google-analytics.com analytics.js"})
training_data.append({"class": "analis", "sentence": "window.GoogleAnalyticsObject new Date"})
training_data.append({"class": "analis", "sentence": "google-analytics.com analytics"})
training_data.append({"class": "analis", "sentence": "window Google Analytics Object push GoogleAnalyticsObject"})
training_data.append({"class": "analis", "sentence": "webvisor clickmap trackLinks accurateTrackBounce:true"})
training_data.append({"class": "analis", "sentence": "location protocol"})
training_data.append({"class": "analis", "sentence": "w.opera object Opera"})
training_data.append({"class": "analis", "sentence": "yandex.ru metrika watch.js"})
training_data.append({"class": "analis", "sentence": "yaCounter new Ya Metrika"})
training_data.append({"class": "analis", "sentence": "yandex.ru metrika watch"})

# training_data.append({"class": "import", "sentence": "see you later"})
# training_data.append({"class": "import", "sentence": "have a nice day"})
# training_data.append({"class": "import", "sentence": "talk to you soon"})

training_data.append({"class": "code", "sentence": "jquery document getElementsByTagName"})
training_data.append({"class": "code", "sentence": "typeof style font src warp vendor uikit"})
training_data.append({"class": "code", "sentence": "undefined script.js js var"})
training_data.append({"class": "code", "sentence": "scr gif jpg pic png url"})
training_data.append({"class": "code", "sentence": "async getElementById id url"})
training_data.append({"class": "code", "sentence": "chrome-extension components"})
training_data.append({"class": "code", "sentence": "templates getElementById results"})
training_data.append({"class": "code", "sentence": "social window alert"})
training_data.append({"class": "code", "sentence": "widget createTextNode appendChild"})
training_data.append({"class": "code", "sentence": "media nodeName window.onload console log element innerHTML"})
training_data.append({"class": "code", "sentence": "vkcom alert new now color vk_groups"})
# training_data.append({"class": "code", "sentence": "what's for lunch?"})
# print("%s sentences in training data" % len(training_data))



words = []
classes = []
documents = []
ignore_words = ['?', '</script>', '<script>', '(', ')', ',', '}', '{', '[', ']', ':', ';', '.', 'function','type',',','=']
# loop through each sentence in our training data
for pattern in training_data:
    # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

# remove duplicates
classes = list(set(classes))

# print(len(documents), "documents")
# print(len(classes), "classes", classes)
# print(len(words), "unique stemmed words", words)


# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

# sample training/output
i = 0
w = documents[i][0]
# print([stemmer.stem(word.lower()) for word in w])
# print(training[i])
# print(output[i])


# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative


def sigmoid_output_to_derivative(output):
    return output*(1-output)


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return(np.array(bag))


def think(sentence, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2




# # функция тренировки
#
# def train(X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):
#
#     print("Training with %s neurons, alpha:%s, dropout:%s %s" % (
#         hidden_neurons, str(alpha), dropout, dropout_percent if dropout else ''))
#     print("Input matrix: %sx%s    Output matrix: %sx%s" %
#           (len(X), len(X[0]), 1, len(classes)))
#     np.random.seed(1)
#
#     last_mean_error = 1
#     # randomly initialize our weights with mean 0
#     synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
#     synapse_1 = 2*np.random.random((hidden_neurons, len(classes))) - 1
#
#     prev_synapse_0_weight_update = np.zeros_like(synapse_0)
#     prev_synapse_1_weight_update = np.zeros_like(synapse_1)
#
#     synapse_0_direction_count = np.zeros_like(synapse_0)
#     synapse_1_direction_count = np.zeros_like(synapse_1)
#
#     for j in iter(range(epochs+1)):
#
#         # Feed forward through layers 0, 1, and 2
#         layer_0 = X
#         layer_1 = sigmoid(np.dot(layer_0, synapse_0))
#
#         if(dropout):
#             layer_1 *= np.random.binomial([np.ones((len(X), hidden_neurons))],
#                                           1-dropout_percent)[0] * (1.0/(1-dropout_percent))
#
#         layer_2 = sigmoid(np.dot(layer_1, synapse_1))
#
#         # how much did we miss the target value?
#         layer_2_error = y - layer_2
#
#         if (j % 10000) == 0 and j > 5000:
#             # if this 10k iteration's error is greater than the last iteration, break out
#             if np.mean(np.abs(layer_2_error)) < last_mean_error:
#                 print("delta after "+str(j)+" iterations:" +
#                       str(np.mean(np.abs(layer_2_error))))
#                 last_mean_error = np.mean(np.abs(layer_2_error))
#             else:
#                 print("break:", np.mean(np.abs(layer_2_error)),
#                       ">", last_mean_error)
#                 break
#
#         # in what direction is the target value?
#         # were we really sure? if so, don't change too much.
#         layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)
#
#         # how much did each l1 value contribute to the l2 error (according to the weights)?
#         layer_1_error = layer_2_delta.dot(synapse_1.T)
#
#         # in what direction is the target l1?
#         # were we really sure? if so, don't change too much.
#         layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
#
#         synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
#         synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))
#
#         if(j > 0):
#             synapse_0_direction_count += np.abs(
#                 ((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
#             synapse_1_direction_count += np.abs(
#                 ((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))
#
#         synapse_1 += alpha * synapse_1_weight_update
#         synapse_0 += alpha * synapse_0_weight_update
#
#         prev_synapse_0_weight_update = synapse_0_weight_update
#         prev_synapse_1_weight_update = synapse_1_weight_update
#
#     now = datetime.datetime.now()
#
#     # persist synapses
#     synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
#                'datetime': now.strftime("%Y-%m-%d %H:%M"),
#                'words': words,
#                'classes': classes
#                }
#     synapse_file = "synapses.json"
#
#     with open(synapse_file, 'w') as outfile:
#         json.dump(synapse, outfile, indent=4, sort_keys=True)
#     print("saved synapses to:", synapse_file)
#
#
#





print("go ...")


X = np.array(training)
y = np.array(output)



# # функция для запуска тренировки!

# start_time = time.time()
#
# train(X, y, hidden_neurons=400, alpha=0.001,
#       epochs=100000, dropout=False, dropout_percent=0.2)
#
# elapsed_time = time.time() - start_time
# print("processing time:", elapsed_time, "seconds")
#




# probability threshold
ERROR_THRESHOLD = 0.1
# load our calculated synapse values
synapse_file = 'synapses.json'
with open(synapse_file) as data_file:
    synapse = json.load(data_file)
    synapse_0 = np.asarray(synapse['synapse0'])
    synapse_1 = np.asarray(synapse['synapse1'])


def classify(sentence, show_details=True):
    results = think(sentence, show_details)

    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    for r in results:
        return_results = classes[r[0]]
        print("класс смотри -------------->: %s" % (return_results))
        if return_results == 'analis':
            return_results = 1
        else:
            return_results = 0
    # return_results = [classes[r[0]] for r in results]
    return return_results
