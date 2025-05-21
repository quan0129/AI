import openai

def get_sql_from_question(question: str, table_metadata: str) -> str:
    prompt = f"""
    Bạn là chuyên gia cơ sở dữ liệu. Hãy đọc hiểu cấu trúc của các bảng và lựa chọn các bảng dữ liệu phù hợp cho câu hỏi.
    Viết một câu SQL cho câu hỏi sau:
    
    Câu hỏi: {question}
    
    Cấu trúc các bảng trong database:
    {table_metadata}

    Chỉ trả lại câu SQL, không thêm bất cứ giải thích nào.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Bạn là một chuyên gia SQL"},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message['content'].strip()
