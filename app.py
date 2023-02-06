from ocr import utils
from non_exact_match import tools
from torchvision.utils import draw_bounding_boxes
import torchvision.transforms as transforms
import torchvision
import torch
import streamlit as st
from PIL import Image

if "user_input" not in st.session_state:
    st.session_state.user_input = "A"

if __name__ == '__main__':
    st.set_page_config(page_title="Detect Text in Image", layout="wide")
    left, right = st.columns(2)
    left.title("Busque um texto no documento desejado")
    right.header("Resultados")


    image_path = left.file_uploader("Faça o upload de uma imagem", type=['png', 'jpg', 'jpeg'])
    if image_path is not None:
        document_image = Image.open(image_path).convert("RGB")
        document_text, document_boxes, word_boxes = utils.get_text_from_image(document_image)
        user_input = left.text_input(label='Digite o texto que deseja buscar na imagem', key='user_input')
        left.markdown("Texto extraido da imagem")
        left.write(f"{document_text}")
        if user_input is not None and len(document_text)>10:
            match_result, final_metric = utils.match_text_in_image(user_input, document_text)
            user_input_2_normalized = tools.string_normalize(document_text)
            if final_metric > 0:
                left.markdown("### Texto encontrado")
                left.write(f"{match_result}")
                #left.write(f"Distancia entre texto buscado e o encontrado: {final_metric}")

                save_boxes = []
                match_result_splited = match_result.split()

                for word, box in word_boxes.items():
                    if match_result_splited:
                        if tools.string_normalize(word) in match_result_splited:
                            save_boxes.append(box)

                box_to_print = torch.tensor(save_boxes)

                transform = transforms.Compose([
                    transforms.PILToTensor()
                ])

                img_tensor = transform(document_image)
                img_tensor = draw_bounding_boxes(img_tensor, box_to_print, width=1, fill=True)
                img_tensor = torchvision.transforms.ToPILImage()(img_tensor)
                right.image(img_tensor)
