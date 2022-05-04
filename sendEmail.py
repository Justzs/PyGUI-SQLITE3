import yagmail #pip install yagmail

# เผื่อกลับมาดูโค้ดอีกทีแล้วจำไม่ได้ (:
# สามารถเปลี่ยน oauth2_file เป็น password
# หรือสามารถเอา oauth2_file มาจาก 
# - เข้าไปที่ Google cloud platform
# - สร้างโปรเจค เช่น MyProject 
# - สลับเข้ามาที่โปรเจคใหม่้่
# - เลือก APIs & Services
# - เลือก OAuth consent screen
# - เลือก External และ กรอกชื่อแอปของเรา  "SendEmail"
# - กรอก Email ของคุณในช่อง Developer contact informaiton 
# - กด Save หน้าต่อไปก็กด Save อีกรอบ
# - เพิ่ม Test user กด save
# - กด Back to dashboard แล้วไปที่ เมนู Credentials
# - Create credentials เลือก OAuth client ID
# - เลือก Application type เป็น Desktop app
# - จะมี Popup แสดงขึ้นมา กด Download Json
# - กดรับไฟล์นี้แล้วทำตาม Command เลย
# - ref. https://www.youtube.com/watch?v=UJCYWEIE41w


def sendEmail(body, recipient, pic=''):

    yag = yagmail.SMTP(user='justzs.dev@gmail.com',oauth2_file="client_secret_674417863199-357fmumeqpo0uolf8lruf6fg4vt4vscu.apps.googleusercontent.com")

    # recipient = {'narongsak56000@gmail.com':'Employee'}
    # name = 'Narongsak'
    # body = f'Dear {name}\n\tHi there'
    # email_attachment = ''

    img =  yagmail.inline(pic)
    subject = "ข้อความตอบกลับอัตโนมัติ"
    yag.useralias = 'Justzs.dev'

    yag.send(to=recipient, subject=subject, contents=[body,img])

    return True