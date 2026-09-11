from template import chat_with_system_prompt

question = "Giải thích blockchain là gì?"

response1, cost1 = chat_with_system_prompt(
    system_prompt="Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi.",
    user_prompt=question,
)
print("=== Giáo viên tiểu học ===")
print(response1)

response2, cost2 = chat_with_system_prompt(
    system_prompt="Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật.",
    user_prompt=question,
)
print("=== Chuyên gia tài chính ===")
print(response2)
