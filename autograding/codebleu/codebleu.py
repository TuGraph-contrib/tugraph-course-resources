import os
from . import bleu, weighted_ngram_match, syntax_match, dataflow_match


def evaluate_per_example(
    reference: str, hypothesis: str, lang: str = "python", params="0.25,0.25,0.25,0.25"
):
    alpha, beta, gamma, theta = [float(x) for x in params.split(",")]

    if lang == "java":
        hypothesis = f"public class Wrapper {{\n{hypothesis}\n}}"
        reference = f"public class Wrapper {{\n{reference}\n}}"

    hypothesis = [hypothesis]
    pre_references = [[reference]]
    for i in range(len(pre_references)):
        assert len(hypothesis) == len(pre_references[i])
    references = []
    for i in range(len(hypothesis)):
        ref_for_instance = []
        for j in range(len(pre_references)):
            ref_for_instance.append(pre_references[j][i])
        references.append(ref_for_instance)
    assert len(references) == len(pre_references) * len(hypothesis)
    # calculate ngram match (BLEU)
    tokenized_hyps = [x.split() for x in hypothesis]
    tokenized_refs = [[x.split() for x in reference] for reference in references]
    ngram_match_score = bleu.corpus_bleu(tokenized_refs, tokenized_hyps)
    # calculate weighted ngram match
    root_dir = os.path.dirname(__file__)
    key_word_file = "c" if lang == "cpp" else lang
    keywords = [
        x.strip()
        for x in open(
            root_dir + "/keywords/" + key_word_file + ".txt", "r", encoding="utf-8"
        ).readlines()
    ]

    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2 for token in reference_tokens}

    tokenized_refs_with_weights = [
        [
            [reference_tokens, make_weights(reference_tokens, keywords)]
            for reference_tokens in reference
        ]
        for reference in tokenized_refs
    ]
    weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(
        tokenized_refs_with_weights, tokenized_hyps
    )
    # calculate syntax match
    syntax_match_score = syntax_match.corpus_syntax_match(references, hypothesis, lang)
    # calculate dataflow match
    dataflow_match_score = dataflow_match.corpus_dataflow_match(
        references, hypothesis, lang
    )
    # dataflow_match_score = dataflow_match.my_dataflow_match(references, hypothesis, lang)
    # print(
    #     'ngram match: {0}, weighted ngram match: {1}, syntax_match: {2}, dataflow_match: {3}'
    #     .format(ngram_match_score, weighted_ngram_match_score, syntax_match_score,
    #             dataflow_match_score))
    codebleu = (
        alpha * ngram_match_score
        + beta * weighted_ngram_match_score
        + gamma * syntax_match_score
        + theta * dataflow_match_score
    )
    return {
        "em": 1.0 if reference.strip() == hypothesis[0].strip() else 0.0,
        "bleu": ngram_match_score,
        "wbleu": weighted_ngram_match_score,
        "syntax": syntax_match_score,
        "dataflow": dataflow_match_score,
        "codebleu": codebleu,
    }


def get_codebleu(refs, hyp, lang="python", params="0.25,0.25,0.25,0.25"):
    if not isinstance(refs, list):
        refs = [refs]
    alpha, beta, gamma, theta = [float(x) for x in params.split(",")]

    # preprocess inputs
    pre_references = [
        [x.strip() for x in open(file, "r", encoding="utf-8").readlines()]
        for file in refs
    ]
    hypothesis = [x.strip() for x in open(hyp, "r", encoding="utf-8").readlines()]

    for i in range(len(pre_references)):
        assert len(hypothesis) == len(pre_references[i])

    references = []
    for i in range(len(hypothesis)):
        ref_for_instance = []
        for j in range(len(pre_references)):
            ref_for_instance.append(pre_references[j][i])
        references.append(ref_for_instance)
    assert len(references) == len(pre_references) * len(hypothesis)

    # calculate ngram match (BLEU)
    tokenized_hyps = [x.split() for x in hypothesis]
    tokenized_refs = [[x.split() for x in reference] for reference in references]

    ngram_match_score = bleu.corpus_bleu(tokenized_refs, tokenized_hyps)

    # calculate weighted ngram match
    root_dir = os.path.dirname(__file__)
    keywords = [
        x.strip()
        for x in open(
            root_dir + "/keywords/" + lang + ".txt", "r", encoding="utf-8"
        ).readlines()
    ]

    def make_weights(reference_tokens, key_word_list):
        return {token: 1 if token in key_word_list else 0.2 for token in reference_tokens}

    tokenized_refs_with_weights = [
        [
            [reference_tokens, make_weights(reference_tokens, keywords)]
            for reference_tokens in reference
        ]
        for reference in tokenized_refs
    ]

    weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(
        tokenized_refs_with_weights, tokenized_hyps
    )

    # calculate syntax match
    syntax_match_score = syntax_match.corpus_syntax_match(references, hypothesis, lang)

    # calculate dataflow match
    dataflow_match_score = dataflow_match.corpus_dataflow_match(
        references, hypothesis, lang
    )
    # dataflow_match_score = dataflow_match.my_dataflow_match(references, hypothesis, lang)

    print(
        "ngram match: {0}, weighted ngram match: {1}, syntax_match: {2}, dataflow_match: {3}".format(
            ngram_match_score,
            weighted_ngram_match_score,
            syntax_match_score,
            dataflow_match_score,
        )
    )

    codebleu = (
        alpha * ngram_match_score
        + beta * weighted_ngram_match_score
        + gamma * syntax_match_score
        + theta * dataflow_match_score
    )

    return codebleu
