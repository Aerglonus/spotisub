import os
import sys
import logging
from dotenv import load_dotenv
from os.path import dirname
from os.path import join
import re
from ..constants import constants

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=int(os.environ.get(constants.LOG_LEVEL, constants.LOG_LEVEL_DEFAULT_VALUE)),
        datefmt='%Y-%m-%d %H:%M:%S')
        
        
def print_logo(version):
        version_len = len(version)
        print(
            """
███████╗██████╗  ██████╗ ████████╗██╗███████╗██╗   ██╗██████╗ 
██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝██║   ██║██╔══██╗
███████╗██████╔╝██║   ██║   ██║   ██║███████╗██║   ██║██████╔╝
╚════██║██╔═══╝ ██║   ██║   ██║   ██║╚════██║██║   ██║██╔══██╗
███████║██║     ╚██████╔╝   ██║   ██║███████║╚██████╔╝██████╔╝
╚══════╝╚═╝      ╚═════╝    ╚═╝   ╚═╝╚══════╝ ╚═════╝ ╚═════╝ 
"""
            + "                                     "[: -(version_len + 2)]
            + "v{} ".format(version
            + "\n")
        )

def write_exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logging.error("%s %s %s", exc_type, fname, exc_tb.tb_lineno, exc_info=1)



def generate_compare_array(strings):
    strings = strings.strip().lower()
    compare_array_values = []
    compare_array_values.append(strings)
    compare_array_values.append(re.sub(r'[^\w\s]','',strings).strip())
    for token in constants.SPLIT_TOKENS:
        compare_array_values.append(strings.split(token, 1)[0].strip())
        compare_array_values.append(re.sub(r'[^\w\s]','',strings.split(token, 1)[0]).strip())

    return list(set(compare_array_values))

def compare_strings(a, b):
    return compare(generate_compare_array(a), generate_compare_array(b))

def compare_string_to_exclusion(a, stringb):
    if a is not None and a.strip() != '':
        words_no_punctuation = []
        for word in a.split():
            words_no_punctuation.append(re.sub(r'[^\w\s]','',word).strip().lower())
    return compare_exact_word(list(set(words_no_punctuation)), stringb)

def compare_exact_word(stringsa, stringsb):
    for stringa in stringsa:
        for stringb in stringsb:
            if stringa != '' and stringb !='' and stringa == stringb:
                logging.warning("Found excluded word: %s. Skipping...", stringb)
                return True    
    return False

def compare(stringsa, stringsb, log_excluded=False):
    for stringa in stringsa:
        for stringb in stringsb:
            if stringa == stringb or stringb in stringa or stringa in stringb:
                if log_excluded is True:
                    logging.warning("Found excluded word: %s. Skipping...", stringb)
                return True    
    return False

def get_excluded_words_array():
    excluded_words = []
    excluded_words_string = os.environ.get(constants.EXCLUDED_WORDS, constants.EXCLUDED_WORDS_DEFAULT_VALUE).replace("\"","")
    if excluded_words_string is not None and excluded_words_string != "":
        excluded_words = excluded_words_string.split(",")

    return excluded_words