# Detect Text In Image

**Conteúdo da Disciplina**: Projeto Final<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 15/0122837  |  Davi Alves Bezerra |

## Sobre 
A principal ideia desse projeto é buscar um texto em uma imagem. Uma especie de Ctrl+f em uma imagem.
Foram usadas algumas funções do projeto de programação dinâmica para busca da string e distância. 
Há algumas limitações devido ao OCR tesseract não ter pré-processamentos nas imagens de input. E também o OCR não passou por um "Fine-tune" o que diminui sua qualidade.

## Screenshots
### Upload da imagem e texto de busca
![image](https://user-images.githubusercontent.com/34287081/217076933-377d63b9-362a-400b-8e54-e360adaa647b.png)
### Funcionamento
O OCR faz a extração do texto com uma baixa confiabilidade em seu texto, podendo ter erros ortograficos. É feita uma busca não exata, aceitando um limite de erros para devolver o texto buscado. 

## Instalação 
**Linguagem**: python 3.8.13<br>
**Framework**: tesseract, streamlit<br>

## Uso 
Instale todas as dependencias a partir do requirements
```
pip install -r requirements.txt
```

Por fim basta executar o comando do streamlit
```
streamlit run app.py
```

Geralmente a interface do streamlit abre no link
```
http://localhost:8501
```

## Outros 
Talvez seja necessario instalar o tesseract
```
sudo apt install tesseract-ocr -y
```



