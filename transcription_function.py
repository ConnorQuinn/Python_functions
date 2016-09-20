# -*- coding: utf-8 -*-

###############################################################################
"""
@author: Connor Quinn

Transcription script:

This script takes a list of folders (participants) where each folder contains
 sound files. It makes use of the speech_recognition module.
 For each folder the script tries to recognise the words in the
 .wav files and outputs the text results.

USE:
You should save this script in a folder, e.g.,
'/speech_data/transcription_function.py'
You should also have subfolders for each of your participants:
/speech_data/transcription_function.py
/speech_data/01
/speech_data/02
/speech_data/03

Probably easiest if the folder (e.g., participant) names are numerical, but no
problem if not. Within each participant folder you should have the .wav files:
/speech_data/01/file1.wav
/speech_data/01/file2.wav
/speech_data/01/file3.wav

The only thing you should have to change in this script is the list of
participants (par_list). The elements in this list must match the names
 you have given to the participants' folders; the '01' in par_list
corresponds to the folder /speech_data/01/

Note: at the moment the script uses the default google speech recognition
api. This may stop working without notice. A better approach is to use the
Pocketsphinx speech recogniser, also supported by the speech_recognition
module.
"""


# Here we specify which libraries to import.
import speech_recognition as sr  # Really useful module
import os
from os import path

par_list = ["01", "02", "03", "04"]  # change this to match folder structure

'''
Before running any code first set up the functions that we will use:
You shouldn't need to change any of the functions.
'''


def recog_wav(wav_file):
    '''
    Reads in one wav file at a time and passes out the resulting text.
    This is the critical piece of code
    '''
    r = sr.Recognizer()
    with sr.WavFile(str(wav_file)) as source:
        audio = r.record(source)  # read the entire WAV file
    try:
        #  for testing purposes, we're just using the default API key
        #  to use another API key, use
        #  `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return r.recognize_google(audio).encode("utf8")
        # r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
    except sr.UnknownValueError:
        print "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        print "Could not request results from Google Speech\
 Recognition service; {0}".format(e)


def recog_files(list, file_out_path):
    '''
    Read in a list of .wav files and output the text to a txt.file
    This function calls the 'recog_files' function for each .wav file.
    '''
    for wav_file in list:
        out_text = recog_wav(wav_file)
        with open(str(file_out_path), 'a') as out_doc:
            out_doc.write('\t'.join(map(str, [wav_file, out_text])))
            out_doc.write('\n')
            out_doc.close()


def set_out_file(file_out_path):
    '''
    Create an output file and set the column headings
    '''
    f_out = open(file_out_path, 'a')
    f_out.write('\t'.join(['Filename', 'Output', ]))
    f_out.write('\n')
    f_out.close()


# All of the action happens below here.
# Gets the path to whereever you are running this script
DIR = path.dirname(path.realpath(__file__))


for par in par_list:  # for each participant
    PAR_DIR = os.path.join(DIR, par)  # find their folder
    print PAR_DIR
    # set the path for the output file
    file_out_path = os.path.join(PAR_DIR, 'Par_{}_output.txt'.format(par))
    # create the output file
    set_out_file(file_out_path)
    # make a list of all .wav files in that folder.
    wav_list = [file for file in os.listdir(PAR_DIR) if file.endswith(".wav")]
    # recognise each file in that list and output results
    recog_files(wav_list, file_out_path)
