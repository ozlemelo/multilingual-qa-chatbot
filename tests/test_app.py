import pytest
from app import read_file, answer_question

def test_read_file_txt():
    class DummyFile:
        def read(self):
            return b"This is a test."
    file_obj = DummyFile()
    result = read_file(file_obj)
    assert result == "This is a test."

def test_answer_question_basic():
    context = "Python is a programming language."
    question = "What is Python?"
    # answer_question fonksiyonu model üzerinden cevabı döndürüyor
    answer = answer_question(context, question)
    assert isinstance(answer, str)
    assert len(answer) > 0
