import os
import requests
from bs4 import BeautifulSoup
import smtplib
from lxml import html

sender_email = receiver_email = os.environ.get("EMAIL_USERNAME")
sender_password = os.environ.get("EMAIL_PASSWORD")
smtp_server = "smtp.gmail.com"
smtp_port = 587

url_to_monitor = "https://www.ceitec.eu/letni-skola-ceitec-student-talent/t10765"


def send_email(link):
    with smtplib.SMTP(smtp_server) as connection:
        connection.starttls()
        # this was a tricky part, since Google discontinued using only email and password to log in when using
        # third parties. So I had to create an app password.
        connection.login(user=sender_email, password=sender_password)
        connection.sendmail(from_addr=sender_email, to_addrs=receiver_email,
                            msg=f"Subject: CEITEC Summer school\n\n"
                                f"Registration is now open\n"
                                f"The registration for the CEITEC Summer school 2024 is now open here: "
                                f"{link}")


def check_for_new():
    response = requests.get(url_to_monitor)
    soup = BeautifulSoup(response.text, 'html.parser')

    # locates the element using xpath, I commented it out, because I realised I don't really need it :(
    # root = html.fromstring(str(soup))
    # div_elements = root.xpath("/html/body/div[6]/a[1]")
    # print(div_elements[0].get('class', []))

    a_elements = soup.find_all('a')

    if len(a_elements) > check_for_new.last_count:
        # new_div_count = len(a_elements) - check_for_new.last_count
        link = a_elements[45].get('href')
        send_email(link)

    check_for_new.last_count = len(a_elements)


# check_for_new.last_count = 0  just to try it out
check_for_new.last_count = 55

check_for_new()
