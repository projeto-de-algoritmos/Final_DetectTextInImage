from PIL import Image
import pytesseract

from non_exact_match import lcs, levenshtein_dist, tools


def apply_tesseract(image: "Image.Image", lang: "por"):
    data = pytesseract.image_to_data(image, lang=lang, output_type="dict")
    words, left, top, width, height = data["text"], data["left"], data["top"], data["width"], data["height"]

    irrelevant_indices = [idx for idx, word in enumerate(words) if not word.strip()]
    words = [word for idx, word in enumerate(words) if idx not in irrelevant_indices]
    left = [coord for idx, coord in enumerate(left) if idx not in irrelevant_indices]
    top = [coord for idx, coord in enumerate(top) if idx not in irrelevant_indices]
    width = [coord for idx, coord in enumerate(width) if idx not in irrelevant_indices]
    height = [coord for idx, coord in enumerate(height) if idx not in irrelevant_indices]

    actual_boxes = []
    for x, y, w, h in zip(left, top, width, height):
        actual_box = [x, y, x + w, y + h]
        actual_boxes.append(actual_box)

    image_width, image_height = image.size

    normalized_boxes = []
    for box in actual_boxes:
        normalized_boxes.append(normalize_box(box, image_width, image_height))

    if len(words) != len(normalized_boxes):
        raise ValueError("Não há tantas palavras quanto caixas delimitadoras")

    return words, normalized_boxes, actual_boxes


def get_text_from_image(image, lang="por"):
    document_text, document_boxes_normalized, document_boxes = apply_tesseract(image, lang)
    word_boxes = dict(zip(document_text, document_boxes))
    return " ".join(document_text), document_boxes, word_boxes


def normalize_box(box, width, height):
    return [
        int(1000 * (box[0] / width)),
        int(1000 * (box[1] / height)),
        int(1000 * (box[2] / width)),
        int(1000 * (box[3] / height)),
    ]


def match_text_in_image(user_input, user_input_2):
    user_input_2_normalized = tools.string_normalize(user_input_2)
    user_input_normalized = tools.string_normalize(user_input)

    user_input_lenth = len(user_input.split(" "))
    ngram_input = tools.generate_ngrams(user_input_2_normalized, ngram=user_input_lenth)

    less_dist = 999
    longest_lcs = 0
    for ngram in ngram_input:
        ngram_levenshtein_dist = levenshtein_dist.edit_distance(ngram, user_input_normalized)
        _, _, _, lcs_result = lcs.lcsubstring(user_input_normalized, ngram)
        if ngram_levenshtein_dist < less_dist:
            less_dist = ngram_levenshtein_dist
            ngram_result = ngram
        if lcs_result > longest_lcs:
            ngram_lcs_result = ngram
            longest_lcs = lcs_result
            #text_result_f, start_f, end_f, lcs_result_f = text_result, start, end, lcs_result
            err_lcs = levenshtein_dist.edit_distance(ngram_lcs_result, user_input_normalized)

    # alignments = pairwise2.align.localxx(ngram_result_lcs, user_input_normalized)
    # for a in alignments:
    #     print(format_alignment(*a))

    if ngram_lcs_result == ngram_result:
        return ngram_lcs_result
    else:
        if err_lcs > ngram_levenshtein_dist:
            return ngram_result
        else:
            return ngram_lcs_result
