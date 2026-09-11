# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 4 tiếng
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.5, 1.0 và 1.5 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> ở 0.0 câu văn khuôn mẫu, lặp lại gần như y hệt nếu chạy lại. Từ 0.5 trở lên xuất hiện thêm chi tiết ngẫu nhiên hơn (số liệu khác nhau về thể tích/kích thước, cách diễn đạt phong phú hơn). Temperature cao tăng tính đa dạng nhưng cũng tăng rủi ro sai lệch chi tiết.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> 0.0 hoặc 0.5 để đảm bảo phản hồi ổn định, chính xác và ít rủi ro sai lệch chi tiết. Temperature cao hơn có thể làm phản hồi đa dạng hơn nhưng không phù hợp cho môi trường hỗ trợ khách hàng, nơi cần thông tin nhất quán và đáng tin cậy.

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> GPT-4o đắt hơn GPT-4o-mini khoảng 4–5 lần cho workload này. GPT-4o xứng đáng với chi phí khi cần phản hồi chất lượng cao, chính xác và phức tạp, ví dụ phân tích tài chính hoặc y tế. Trường hợp nên dùng mini là khi cần phản hồi nhanh, chi phí thấp và nội dung không quá phức tạp, ví dụ chatbot hỗ trợ khách hàng cơ bản.

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> Hai phản hồi khác nhau về độ dài, từ vựng và cách diễn giải. Bản "giáo viên tiểu học" dùng câu chuyện ẩn dụ đời thường, câu văn ngắn, từ ngữ đơn giản, có emoji/liệt kê để trẻ dễ hình dung, và giải thích khái niệm bằng ví dụ cụ thể thay vì thuật ngữ. Bản "chuyên gia tài chính" dùng ngôn ngữ học thuật, chèn thuật ngữ chuyên ngành, cấu trúc theo dạng phân tích kỹ thuật với đề mục rõ ràng, và đi sâu vào cơ chế hoạt động thay vì dùng ẩn dụ. System prompt ảnh hưởng đến giọng văn, mức độ chuyên môn lẫn cách tổ chức nội dung của model.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> Hai con số chênh nhau khoảng 10–20% tùy đoạn văn. Tiếng Việt thường tốn nhiều token hơn tiếng Anh cùng độ dài vì tiếng Việt có nhiều từ đa âm tiết, dấu câu và ký tự đặc biệt, trong khi tiktoken đếm token dựa trên byte pair encoding, dẫn đến số token tăng lên so với ước lượng số từ.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất khi người dùng cần phản hồi gần như tức thì, ví dụ trong chat trực tiếp hoặc ứng dụng tương tác thời gian thực. Non-streaming phù hợp hơn khi độ trễ không phải vấn đề lớn, và muốn xử lý toàn bộ phản hồi cùng lúc, ví dụ khi sinh văn bản dài hoặc batch processing.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> Exponential backoff giúp giảm tải cho API bằng cách tăng dần thời gian chờ giữa các lần retry, tránh tình trạng "thundering herd" khi nhiều client cùng retry đồng thời. Nếu tất cả client đều retry với delay cố định giống nhau, API sẽ tiếp tục bị quá tải và nhiều request sẽ thất bại, dẫn đến hiệu suất tổng thể kém hơn.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> Tôi chọn persona là một thư ký giám đốc, luôn trả lời ngắn gọn, rõ ràng và bằng tiếng Việt. Lý do tôi yêu cầu "trả lời ngắn gọn" là để người dùng nhận được thông tin nhanh chóng mà không bị loãng bởi các chi tiết không cần thiết. Việc chỉ định ngôn ngữ là tiếng Việt giúp đảm bảo trợ lý luôn sử dụng ngôn ngữ phù hợp với người dùng.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> Hạn chế lớn nhất của trợ lý hiện tại là chưa có bộ nhớ dài hạn, nên không thể ghi nhớ thông tin từ các phiên chat trước. Một cải thiện cụ thể là triển khai một cơ chế lưu trữ và truy xuất thông tin người dùng từ các phiên trước, ví dụ sử dụng cơ sở dữ liệu hoặc file lưu trữ, và cập nhật lịch sử chat khi cần thiết.

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên fork và dán link trên trang bài Lab ở VLearn trước 23:59 ngày 11/09/2026
