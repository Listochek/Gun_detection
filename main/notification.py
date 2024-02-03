import smtplib
from email.mime.text import MIMEText



def send_email():

    ''' 
    ФУНКЦИЯ ОПОВЕЩЕНИЯ
    высылаент email на определенную почту
    '''

    # Настройки SMTP сервера
    sender = 'notificationgun@gmail.com' 

    password = 'zhhf semu rcdm yfis'
    message = f'Обнаржено оружие\nПожалуйста приймите меры, будте осторожны\nКамера - 1'

    # Создание объекта SMTP

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg['Subject'] = 'Нейронная сеть обнаружила оружие'
        server.sendmail(sender, sender, msg.as_string())
        print(msg.as_string())
        return 'Сообщение об угрозе отправлено' 
    
    except Exception as _ex:
        print(f'{_ex}')
        return f'Что то пошло не так, уведомление не отправлено'
        
        

if __name__ == "__main__":
    send_email()
