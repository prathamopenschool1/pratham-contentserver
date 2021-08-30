import os
import json
import requests
from pprint import pprint



class AssesmentHelper(object):

    def language_call(self):

        try:
            lang_url = "http://www.prathamassessment.org:8085/api/language/GetLanguage"
            lang_response = requests.get(lang_url)
            lang_result = json.loads(lang_response.content.decode('utf-8'))
            return lang_result
        except Exception as e:
            print("exception is ", e)
            return -1


    def subject_call(self, langId):
        try:
            subj_url = 'http://www.prathamassessment.org:8085/api/subject/GetSubjectv2?languageid={}'.format(langId)
            subj_response = requests.get(subj_url)
            subj_result = json.loads(subj_response.content.decode('utf-8'))
            return subj_result
        except Exception as e:
            print("exception is ", e)
            return -1


    def exam_call(self, langId, subjId):
        try:
            exam_url = 'http://www.prathamassessment.org:8085/api/subjectexam/GetExamV2?subjectid={}&languageid={}'.format(subjId, langId)
            exam_response = requests.get(exam_url)
            exam_result = json.loads(exam_response.content.decode('utf-8'))
            return exam_result
        except Exception as e:
            print("exception is ", e)
            return -1

    
    def pattern_call(self, examId):
        try:
            pattern_url = 'http://www.prathamassessment.org:8085/api/exampattern/GetExamPattern?examid={}'.format(examId)
            pattern_response = requests.get(pattern_url)
            pattern_result = json.loads(pattern_response.content.decode('utf-8'))
            return pattern_result
        except Exception as e:
            print("exception is ", e)
            return -1

    