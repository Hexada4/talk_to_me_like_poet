import argparse
import json
import os
import pickle

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text

from lyrics import util
from flask import Flask, request

# here I`m compelled to copy code from cli to implement my own algorithm to work with model
# and already exisiting file cli.py can help me with it
model = 'export/2023-10-02T110043/model.h5'
tokenizer = 'export/2023-10-02T110043/tokenizer.pickle'

def softmax_sampling(probabilities, randomness, seed=None):
    """Returns the index of the highest value from a softmax vector,
    with a bit of randomness based on the probabilities returned.

    """
    if seed:
        np.random.seed(seed)
    if randomness == 0:
        return np.argmax(probabilities)
    probabilities = np.asarray(probabilities).astype("float64")
    probabilities = np.log(probabilities) / randomness
    exp_probabilities = np.exp(probabilities)
    probabilities = exp_probabilities / np.sum(exp_probabilities)
    return np.argmax(np.random.multinomial(1, probabilities, 1))


def generate_lyrics(model, tokenizer, text_seed, song_length, randomness=0, seed=None):
    """Generate a new lyrics based on the given model, tokenizer, etc.

    Returns the final output as both a vector and a string.

    """
    # The sequence length is the second dimension of the input shape. If the
    # input shape is (None,), the model uses the transformer network which
    # takes a string as input!
    input_shape = model.inputs[0].shape
    seq_length = -1
    if len(input_shape) >= 2:
        print("Using integer sequences")
        seq_length = int(input_shape[1])
    else:
        print("Using string sequences")

    # Create a reverse lookup index for integers to words
    rev = {v: k for k, v in tokenizer.word_index.items()}

    spacer = "" if tokenizer.char_level else " "

    text_output = tokenizer.texts_to_sequences([text_seed])[0]
    text_output_str = spacer.join(rev.get(word) for word in text_output)
    while len(text_output) < song_length:
        if seq_length != -1:
            padded = tf.keras.preprocessing.sequence.pad_sequences(
                [text_output], maxlen=seq_length, padding="post"
            )
        else:
            padded = np.array([text_output_str])
        next_word = model.predict_on_batch(padded)
        next_word = softmax_sampling(next_word[0], randomness, seed=seed)
        text_output.append(next_word)
        text_output_str += f"{spacer}{rev.get(next_word)}"
    return text_output, text_output_str


def load_model(model_filename):
    return tf.keras.models.load_model(
        model_filename, custom_objects={"KerasLayer": hub.KerasLayer}
    )


def lyrics(model, tokenizer, text, length):
    model = load_model(model)

    tokenizer = util.load_tokenizer(tokenizer)

    print(f'Generating lyrics from "{text}"...')
    seed = (np.random.randint(np.iinfo(np.int32).max)
    )

    raw, text = generate_lyrics(
        model, tokenizer, text, length, 0.0, seed=seed # randomness I took from cli func as default value
    )

    return text


# initialize app
app = Flask(__name__)


@app.route('/')
def index_page():
    """
    Generates first page to get rid of error on the first page
    :return: text
    """
    return 'Hi! It is api of model "talk to me like a poet" '


@app.route('/predict')
def predict():
    """
    this function gets no arguments. It runs the model and get predict from it
    :return: prediction
    """
    text = request.args['text']
    length = request.args['length']
    answer = lyrics(model, tokenizer, text, length) # predicting...
    print('Generated', answer) # just logging, in future may be rewritten
    return answer


app.run(host='0.0.0.0', port=8000)
