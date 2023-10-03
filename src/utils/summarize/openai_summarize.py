from typing import List

import openai
import spacy
import tiktoken
from metaphor_python import Result

import utils.clients.openai_config

nlp = spacy.load("en_core_web_sm")


def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    number_of_tokens = len(encoding.encode(text))

    return number_of_tokens


def text_to_chunks(text, max_tokens):
    chunks = [[]]
    chunk_total_tokens = 0

    sentences = nlp(text)

    for sentence in sentences.sents:
        sentence_tokens = count_tokens(sentence.text)

        if chunk_total_tokens + sentence_tokens > max_tokens:
            chunks.append([])
            chunk_total_tokens = 0

        chunks[len(chunks) - 1].append(sentence.text)
        chunk_total_tokens += sentence_tokens

    return chunks


def summarize_findings(findings: List[Result]) -> str:
    text_to_summarize = "\n".join(
        [f"{result.title}\n{result.extract}" for result in findings if result.extract]
    )

    max_tokens_per_chunk = 1000  # Metaphor max, we will summarize a smaller amount at a time

    text_chunks = text_to_chunks(text_to_summarize, max_tokens_per_chunk)

    summaries = []
    for chunk in text_chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following information:\n{chunk}",
                },
            ],
            max_tokens=400,
        )
        generated_text = response["choices"][0]["message"]["content"]

        summaries.append(generated_text.strip())

    summarized_text = "\n".join(summaries)

    return summarized_text
