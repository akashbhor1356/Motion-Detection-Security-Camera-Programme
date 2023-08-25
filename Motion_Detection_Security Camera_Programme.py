import cv2
import winsound
import smtplib

def email_settings():



    sen_email = "sender email put here"
    rev_email = "reciver email put here"
    pw = 123456789
    message = "we Detected  Suspeciouss Movements "

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sen_email,str(pw))

    server.sendmail(sen_email,rev_email,message)
    print("email sent successfully")


cam = cv2.VideoCapture(0)
warning_count = 0

while cam.isOpened():

    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dialted = cv2.dilate(thresh, None, iterations=3)
    contorus, _ = cv2.findContours(dialted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contorus:
        if cv2.contourArea(c) < 4000:     #lower this value to capture slow movements
            continue

        else:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            warning_count += 1
            print("Detect some movements")
            winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

            if warning_count == 5:
                #send whats app & email
                email_settings()
                print("email send")


    if cv2.waitKey(30) == ord('e'):    #you can change the key  as your desire
        break

    cv2.imshow('Security Camera', frame1)


