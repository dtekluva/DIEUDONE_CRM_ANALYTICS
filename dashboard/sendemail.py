# import smtplib, ssl

# class Mail:

#     def __init__(self):
#         self.port = 465
#         self.smtp_server_domain_name = "smtp.gmail.com"
#         self.sender_mail = "inaconsumerinfo@gmail.com"
#         self.password = "ygpczbfnkkyyfvuw"

#     def send(self, emails, subject, content):
#         ssl_context = ssl.create_default_context()
#         service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
#         service.login(self.sender_mail, self.password)
        
#         for email in emails:
#             result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

#         service.quit()


# if __name__ == '__main__':
#     mails = input("Enter emails: ").split()
#     subject = input("Enter subject: ")
#     content = input("Enter content: ")

#     mail = Mail()
#     mail.send(mails, subject, content)


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:


    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "inaconsumerinfo@gmail.com"
        self.password = "ygpczbfnkkyyfvuw"

    def send(self, emails, lga = "Mushin"):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for email in emails:
            mail = MIMEMultipart('alternative')
            mail['Subject'] = 'Jaison\'s Emotion App.'
            mail['From'] = self.sender_mail
            mail['To'] = email
            
            for x in data.keys():

                data[x] = "\n" + data[x].replace("\n\n", "#026").replace("\n", "").replace("#026", "\n\n")

            text = ""
            for text_data in data[lga].split("\n\n"):
                text += f"""
                    <li><b>{text_data}</b>
                """

            html_template = """
            <h1>Urgent Recommendations</h1>

            <p>Hi {0}, </p>

            <p>We are delighted announce that based on your inputs there are some hospitals close by that can help.</p>
            <br>
            <p>Please Visit any of the hospitals below as found in {2}.</p>

            <ol>
                {1}
            </ol>

            Regards,
            Helper Bot.
            """
            html_content = MIMEText(html_template.format(email.split("@")[0], text, lga), 'html')

            mail.attach(html_content)

            service.sendmail(self.sender_mail, email, mail.as_string())

        service.quit()


if __name__ == '__main__':
    mails = input("Enter emails: ").split()

    mail = Mail()
    mail.send(mails)

data = {
"Alimosho":

"""HopeFill Health 11 Bello Close
 Alimosho 102213,
 Lagos.
 08037265446,8am - 12am,

 Crystal Specialist
 Hospital Alimosho
 Lagos
 Lagoon Hospital
 (Apapa), 148/150,
 Akowonjo Rd,
 300001, Lagos.
 0903 798 6329 24 hours 

 Olamma Cares
 Foundation
 14 Shofodiya
 Close, off
 Adegoke street,
  Alh. Masha Rd,
 Surulere 101283,
 Lagos.
 0706 318 3892 10 am - 5 pm

 Westcare
 Specialist
 Hospital
 32 Samuel Street,
 Egbeda 102213,
 Lagos.
 0908 497 5995 24 hours""",  

"Ajeromi-Ifelodun":

""" Ajeromi General
 Hospital, Ajegunle
 6 Cardoso St,
 Ajegunle 102103,
 Lagos.
 0807 177 7802 EVERYDAY
 24 HOURS 

 Saint Milla Hospital 35 Ogbowankwo
 Street, Malu
 102103, Lagos
 N/A MONDAY -
 SUNDAY
  8 am - 5 pm
 Adeb Hospital 64 Alafia St,
 Amukoko 102103,
 Lagos.
 N/A MONDAY -
 SATURDAY
 8 am - 6 pm",

"Kosofe":

"Concept One
 Medical Center
 10, Kehinde
 Odusote Street,
 Kosofe 105102,
 Lagos.
 0909 555 5531 24 hours open. 

 Psychaid Consult 7b Mabinuori
 Dawodu St, Pedro
 100234, Lagos
 0903 499 4798 10 am - 5 pm
 Psychhubb 8 Ajayi St, Mende
  105102, Lagos
 N/A 9 am - 5 pm""", 

"Mushin":

"""Mushin General
 Hospital
 48 Oliyide St,
 Mushin 102215,
 Lagos
 0807 559 3685 EVERYDAY
 24 HOURS

 Hill Star Hospital 98 Palm Avenue,
 Mushin 102215,
 Lagos.
 0708 870 2931 MONDAY - FRIDAY
 9 am - 5 pm 

 Best Hope Hospital 40 Araromi, St,
 Mushin 102215,
 Lagos.
  N/A MONDAY -
 SATURDAY
 9 am - 6 pm""",

"Oshodi-Isolo":

"""Hakron Specialist
 Care Center
 24, Oyetola Street
 off Samuel,
 Mafoluku Oshodi,
 Lagos.
 0803 976 0351 Temporarily Closed

 Total Psyche
 Services and
 Consult
 9 Dr. JP Nzewi
 Close, Oshodi -
 Isolo 100001,
 Lagos.
 0909 652 5192 10 am - 5 pm

 Federal G8XX+9JIM, Nitel N/A EVERYDAY
 NeuroPsychiatric
 Hospital Annex
 Office. 
 Complex, Papa
 Ajao 102215,
 Lagos.
 24 HOURS""",


"Ojo":

"""HallMark Clinic 75 Ojo Igbede
 Road, Ojo 102111,
 Lagos.
 0708 435 6648 7 am - 5 pm 

 Jomark Hospital 2 Ladega St, Alaba
 102103, Lagos.
 N/A EVERYDAY
  24 HOURS

 Rikky Hospital 193 Ojo Road,
 Alaba 102103,
 Lagos.
 N/A EVERYDAY
  9 am - 5 pm""",

"Ikorodu":

"""The retreat health
 center
 Ewu-elepe, Laaga,
 Rd, Ijede Rd,
 Ikorodu, Lagos.
  0818 111 0365 N/A

 Xpress Point -
 ODUFUWAOLUSEUN FED NEURO-PSYCHIATRICTS HOUSING
 EST, Igbo Olomu
 Rd, Lagos.
 0908 043 7495 MONDAY -
 SATURDAY
 8 am - 6 pm

 TJK center Point vent
 281 Omoba bus
 stop, Igbo Olomu
 Rd, Ikorodu, Lagos.
 0813 090 6818 EVERYDAY
 8 am - 6 pm""",

"Surulere":

"""EmpathySpacy
 Therapy Hub
 11 Gbajumo Cres,
 Surulere 101241,
0803 229 5584 9 am - 5 pm
 Lagos.

 Olamma Cares
 Foundation
 14 Shofodiya close
 off Adegoke street,
 ALh. masha road,
 Surulere 101283,
 Lagos.
 0706 318 3892 10 am - 5 pm

 BM Empire
 Multispecialist
  Hospital
  4 Amosu Street,
  Bode Thomas St,
 Lagos.
 0906 869 9032 EVERYDAY
 24 HOURS""",

"Agege":

"""Best Care Hospital 2A Keffi Street, by
 Toyan St, 101233,
 Lagos.
 0901 361 7520 EVERYDAY
 24 HOURS 

 College of Medicine
 University of Lagos.
   8 Alagbigba Street,
 Papa Ashafa
 102212, Lagos.
 01 844 7891 MONDAY -
 SATURDAY
 8 am - 5 pm""",

"Ifako-Ijaiye":

"""General Hospital
 Ifako Ijaiye
 14 College Road,
 Off Iju Rd, Ifako
  Agege, Lagos.

 N/A EVERYDAY
 24 HOURS
 IFAKO General
   Hospital
  Off iju Rd, Ifako
 Agege 101232,
 Lagos.  

 0802 331 1868 EVERYDAY
 24 HOURS
 Saint Thomas
 Hospital
 17 Awoni Murphy
 St, Ifako Ijaiye
 100211, Lagos.
 N/A EVERYDAY
 24 HOURS""",

"Somolu":
"""Amazing Health
 Care Center
 29 Adeshina St,
 Bariga, 102216,
  Lagos.
 0802 311 7849 MONDAY -
 SATURDAY
 9 am - 8 pm 

 Gbagada General
 Hospital
 1 hospital Rd,
 Gbagada, 105102,
 Lagos.
 0905 395 3306 EVERYDAY
 24 HOURS 

 General Hospital
 Somolu
 1 Oguntolu St,
 Somolu 102216,
 Lagos.
 0807 559 4442 EVERYDAY
 24 HOURS""", 

"Amuwo-Odofin":

"""Gracehill Behaviour
 Health Services
 1 Patience
 Olukayode Cresent,
 Lakeview Estate,
 Off Raji Rasaki
  Estate Road,
 Amuwo Odofin
 Estate, Avenue.
 0909 110 7514 24 hours

 Patviv Healthcare
 Limited
 322 Road, A Close
 Round-about
 Festac, Festac
 town, 102312,
 Lagos.
 0803 478 2410 EVERYDAY
 9 am - 8 pm

 HMC Hospital Muwo Tedi Rd,
 Volkswagen
 102113, Lagos.
 N/A MONDAY -
  SATURDAY
 8 am - 5 pm""",

"Ikeja":

"""Grey Insight Limited 5B, JO-Babs dare
 close, off Adeteri
 close, Opebi
 100212, Ikeja.
 0908 758 0004 9 am - 8 pm 

 Sanemind 1 Alayode Close,
 Agbaoku Opebi
 Ikeja, 100212,
 Lagos.
 N/A MONDAY - FRIDAY
 9 am - 5 pm

 MindPlus Practition Rainbow Hut, 27,
 Amore Street, Off
 Toyin St, by Ikeja
 0909 010 0055 N/A""", 

"Eti-Osa":

"""PsychNG Services 10 Hughes Avenue,
 Alagomeji-Yaba
 100001, Lagos
 0808 352 3600 9 am - 5 pm 

 Federal
 Neuro-Psychiatric
  Hospital
 Federal
 Neuro-Psychiatric
 Hospital, 8 Harvey
 Road, Yaba, Lagos.
 0802 310 3066 Temporary Closed

 Citicare
 Psychological
 Services
 26, Akin Leigh
 Cresent, Lekki
 Phase 1, Eti-Osa,
 Lagos.
 0706 369 5438 MONDAY - FRIDAY
 9 am - 8 pm""",

"Apapa":

"""Lagoon Hospital,
 Apapa.
 8 Marine Rd,
 Apapa 102272,
 Lagos.
 0903 413 6452 EVERYDAY
 24 HOURS  

 Majoro Hospital 9 Pelewura Cres,
  Apapa 102272,
  Lagos
  01 454 1652 EVERYDAY
 24 HOURS 

 Chosen Child
 Orphanage and
 Care Center
 106 Gaskiya Rd,
  Ijora 102272,
 Lagos.
 0803 426 6283 EVERYDAY
 24 HOURS""", 

"Epe":

"""General Hospital,
 Epe
 HXPC+F6J, Ikesan
 Street, 106101,
  Epe.
  N/A EVERYDAY
 24 HOURS  

 True care model
 hospital
 19 Adeyemi,
 Adeyemi Apena St,
 Epe.
 0803 439 3545 MONDAY -
 SATURDAY
 8 am - 5 pm
 
 LASU Epe Health
 Center
 HXQW+7CR, Lasu
  Rd, 106101, Epe
  N/A MONDAY -
 SUNDAY
 8 am - 8 pm""",

"Ibeju-Lekki":

"""General Hospital Ibeju Lekki, 105101, Lekki, N/A MONDAY - FRIDAY, 8 am - 4 pm

 MAKOG HOSPITAL Makog house, Opposite Cynergy Hotel, Magbon Alade, Ibeju-Lekki. Along Lekki Free Trade  Zone Rd, Alade, Magbon. 0803 727 0210 EVERYDAY 24 HOURS"""
}

# for x in data.keys():

#     print(data[x].replace("\n\n", " #026")
#                     .replace("\n", " ")
#                     .replace("#026", " \n\n")
#                     , "\n\n\n")
#     data[x] = "\n" + data[x].replace("\n\n", "#026").replace("\n", "").replace("#026", "\n\n")


# print('\n\n\n')
# print(data)

# print(data["Mushin"])