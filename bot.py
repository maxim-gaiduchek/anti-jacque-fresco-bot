import cv2
import pytesseract
import telebot

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
bot = telebot.TeleBot("1940450587:AAFdzXtjXOVxPhNveqNB8eGCQXWBz0r0x_g")


@bot.message_handler(content_types=["text"])
def parse_message(message):
    chat = message.chat

    if chat.type == "private":
        bot.send_message(message.chat.id, "Привет. Я - бот, который борется с Жаком Фреско (@fresco_guard_bot). Добавь "
                                          "меня в чат с Жакой чтоб я решал за вас уравнения или пересылай мне его "
                                          "картинки")


@bot.message_handler(content_types=["photo"])
def parse_message(message):
    if message.from_user.username == "fresco_guard_bot" or message.forward_from.username == "fresco_guard_bot":
        tg_photo = bot.get_file(message.photo[-1].file_id)
        photo = bot.download_file(tg_photo.file_path)
        with open("photo.jpg", "wb") as f:
            f.write(photo)

        frame = cv2.imread("photo.jpg", cv2.IMREAD_GRAYSCALE)
        roi = frame[128:186, 40:333]

        cv2.imwrite("photo.jpg", roi)

        problem = pytesseract.image_to_string(roi)

        digits = ""
        for ch in str(problem):
            if 48 <= ord(ch) <= 57:
                digits += ch
        solving = str(int(digits[0]) + int(digits[1]) * int(digits[2]))

        bot.send_message(message.chat.id, solving)


if __name__ == "__main__":
    bot.polling()
