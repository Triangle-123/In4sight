"""
유사도 검증 함수 패키지
"""

import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess_text(text):
    """텍스트 전처리 함수: 소문자 변환, 특수문자 제거 등"""
    # 한글, 영문, 숫자만 남기고 나머지는 공백으로 변환
    text = re.sub(r"[^\w\s가-힣]", " ", text)
    # 여러 공백을 하나로 치환
    text = re.sub(r"\s+", " ", text).strip()
    return text


def keyword_match_score(query, title):
    """키워드 매칭 기반 유사도 계산"""
    # 텍스트 전처리
    query = preprocess_text(query)
    title = preprocess_text(title)

    # 단어 집합 생성
    query_words = set(query.split())
    title_words = set(title.split())

    if not query_words or not title_words:
        return 0.0

    # 공통 단어 찾기
    common_words = query_words.intersection(title_words)

    # 자카드 유사도 계산: 교집합 / 합집합
    jaccard = len(common_words) / len(query_words.union(title_words))

    # 쿼리 단어가 제목에 포함된 비율 계산
    query_coverage = len(common_words) / len(query_words) if query_words else 0

    # 가중 평균 반환 (자카드 유사도와 쿼리 커버리지의 조합)
    return 0.4 * jaccard + 0.6 * query_coverage


def tfidf_similarity(query, title, vectorizer=None):
    """TF-IDF 기반 유사도 계산"""
    if vectorizer is None:
        vectorizer = TfidfVectorizer(min_df=1)
        corpus = [query, title]
        vectorizer.fit(corpus)

    # 벡터 변환
    query_vec = vectorizer.transform([query])
    title_vec = vectorizer.transform([title])

    # 코사인 유사도 계산
    dot_product = query_vec.dot(title_vec.T).toarray()[0][0]
    query_norm = np.sqrt(query_vec.multiply(query_vec).sum())
    title_norm = np.sqrt(title_vec.multiply(title_vec).sum())

    # 0으로 나누는 것 방지
    if query_norm == 0 or title_norm == 0:
        return 0.0

    return dot_product / (query_norm * title_norm)


def embedding_similarity(query_embedding, title_embedding):
    """임베딩 기반 코사인 유사도 계산"""
    return np.dot(query_embedding, title_embedding) / (
        np.linalg.norm(query_embedding) * np.linalg.norm(title_embedding)
    )


def hybrid_similarity(
    query_text,
    title,
    query_embedding,
    title_embedding,
    embedding_weight=0.5,
    keyword_weight=0.3,
    tfidf_weight=0.2,
    vectorizer=None,
):
    """하이브리드 유사도 계산 함수"""
    # 1. 임베딩 기반 코사인 유사도
    emb_sim = embedding_similarity(query_embedding, title_embedding)

    # 2. 키워드 매칭 유사도
    key_sim = keyword_match_score(query_text, title)

    # 3. TF-IDF 기반 유사도
    tf_sim = tfidf_similarity(query_text, title, vectorizer)

    # 가중치를 적용한 최종 유사도 계산
    final_similarity = (
        embedding_weight * emb_sim + keyword_weight * key_sim + tfidf_weight * tf_sim
    )

    return final_similarity
