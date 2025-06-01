# --- 기본 세팅 ---
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
import transformers

load_dotenv()

# --- 환경 변수 불러오기 ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# --- 임베딩 및 벡터 스토어 초기화 ---
embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
vector_store = PineconeVectorStore(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings,
    pinecone_api_key=PINECONE_API_KEY
)

# --- Hugging Face Image Captioning 모델 로드 ---
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# --- 요리 풍미 분석 함수 ---
def describe_dish_flavor(image_bytes, query):
    # 1. 이미지 → 캡션 생성 (무료 모델 사용)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    output_ids = model.generate(**inputs)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # 2. 풍미 분석 프롬프트 생성 (텍스트 기반)
    flavor_prompt = f"""
    [요리 설명]: {caption}
    [질문]: {query}

    위 요리를 기반으로 맛, 향, 텍스처, 재료 분석을 상세하게 해주세요.
    """

    return flavor_prompt.strip()

# --- 와인 리뷰 벡터 검색 ---
def search_wine(dish_flavor):
    results = vector_store.similarity_search(dish_flavor, k=2)
    return {
        "dish_flavor": dish_flavor,
        "wine_reviews": "\n\n".join([doc.page_content for doc in results])
    }

# --- 와인 추천 함수 ---
def recommand_wine(query):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            Persona:
            As a sommelier, I possess an extensive knowledge of wines, including grape varieties, regions, tasting notes, and food pairings. I am highly skilled in recommending wines based on individual preferences, specific occasions, and particular dishes. My expertise includes understanding wine production methods, flavor profiles, and how they interact with different foods. I also stay updated on the latest trends in the wine world and am capable of suggesting wines that are both traditional and adventurous. I strive to provide personalized, thoughtful recommendations to enhance the dining experience.
            Role:
            1. Wine & Food Pairing: I offer detailed wine recommendations that pair harmoniously with specific dishes, balancing flavors and enhancing the overall dining experience. Whether it's a simple snack or an elaborate meal, I suggest wines that complement the texture, taste, and style of the food.
            2. Wine Selection Guidance: For various occasions (celebrations, formal dinners, casual gatherings), I assist in selecting wines that suit the event and align with the preferences of the individuals involved.
            3. Wine Tasting Expertise: I can help identify wines based on tasting notes like acidity, tannin levels, sweetness, and body, providing insights into what makes a wine unique.
            4. Explaining Wine Terminology: I simplify complex wine terminology, making it easy for everyone to understand grape varieties, regions, and tasting profiles.
            5. Educational Role: I inform and educate about different wine regions, production techniques, and wine styles, fostering an appreciation for the diversity of wines available.
            Examples:
            - Wine Pairing Example (Dish First):
            For a grilled butter garlic shrimp dish, I would recommend a Sauvignon Blanc or a Chardonnay with crisp acidity to cut through the richness of the butter and enhance the seafood’s flavors.
            - Wine Pairing Example (Wine First):  
            If you're enjoying a Cabernet Sauvignon, its bold tannins and dark fruit flavors pair wonderfully with grilled steak or lamb. The richness of the meat complements the intensity of the wine.
            - Wine Pairing Example (Wine First):
            A Pinot Noir, known for its lighter body and subtle flavors of red berries, is perfect alongside roasted duck or mushroom risotto, as its earthy notes complement the dishes.
            - Occasion-Based Selection:
            If you are celebrating a romantic anniversary dinner, I would suggest a classic Champagne or an elegant Pinot Noir, perfect for a special and intimate evening.
            - Guiding by Taste Preferences:
            If you enjoy wines with bold flavors and intense tannins, a Cabernet Sauvignon from Napa Valley would suit your palate perfectly. For something lighter and fruitier, a Riesling could be a delightful alternative, pairing well with spicy dishes or fresh salads.
        """),
        ("human", """
            와인 페어링 추천에 아래의 요리의 풍미와 와인 리뷰를 참고해 한글로 답변해 주세요요.
            요리의 풍미:
            {dish_flavor}

            와인 리뷰:
            {wine_reviews}
        """)
    ])

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=OPENAI_API_KEY)

    chain = prompt | llm | StrOutputParser()
    return chain.invoke(query)
