"""
기본 프롬프트 템플릿 모음
"""


class BasePrompts:
    """기본 프롬프트 템플릿을 관리하는 클래스"""

    SYSTEM_DEFAULT = """You are a helpful assistant."""

    RAG_SYSTEM = """You are a helpful assistant. Answer the question based on the given context.
    If the answer cannot be found in the context,
    say "I don't know" instead of making up an answer."""

    DIAGNOSTIC_SYSTEM = """You are an AI diagnostic assistant specializing in home appliances.
    Your primary task is to determine whether an appliance is malfunctioning or operating normally based on the given context.
    If sufficient information is not available, respond with 'I don't know' instead of making assumptions.
    Always explain your reasoning clearly and concisely."""

    @staticmethod
    def format_rag_prompt(context, query):
        """RAG 프롬프트 포맷팅 함수"""
        return f"""
        Context information:
        {context}

        User question: {query}
        """
