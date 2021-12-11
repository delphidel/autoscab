from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import random
import time
import os
import functools
from faker import Faker
from resume_faker import make_resume
from pdf2image import convert_from_path

fake = Faker()
chromedriver_location = "./chromedriver"
print = functools.partial(print, flush=True)

urls = ['https://jobs.kellogg.com/job/Lancaster-Permanent-Production-Associate-Lancaster-PA-17601/817684800/#',
        'https://jobs.kellogg.com/job/Omaha-Permanent-Production-Associate-Omaha-NE-68103/817685900/z',
        'https://jobs.kellogg.com/job/Battle-Creek-Permanent-Production-Associate-Battle-Creek-MI-49014/817685300/',
        'https://jobs.kellogg.com/job/Memphis-Permanent-Production-Associate-Memphis-TN-38114/817685700/'
        ]


data2 = {
    'resume': '//*[@id="49:_file"]',
    'addy': '//*[@id="69:_txtFld"]',
    'city': '//*[@id="73:_txtFld"]',
    'zip': '//*[@id="81:_txtFld"]',
    'job': '//*[@id="101:_txtFld"]',
    'salary': '//*[@id="172:_txtFld"]',
    'country': '//*[@id="195:_select"]'
}
data = {
    'email': '//*[@id="fbclc_userName"]',
    'email-retype': '//*[@id="fbclc_emailConf"]',
    'pass': '//*[@id="fbclc_pwd"]',
    'pass-retype': '//*[@id="fbclc_pwdConf"]',
    'first_name': '//*[@id="fbclc_fName"]',
    'last_name': '//*[@id="fbclc_lName"]',
    'pn': '//*[@id="fbclc_phoneNumber"]',

}


cities = {'Lancaster':  'Pennsylvania',
          'Omaha':  'Nebraska',
          'Battle Creek':   'Michigan',
          'Memphis':    'Tennessee',
          }

zip_codes = {
    'Lancaster':    ['17573', '17601', '17602', '17605', '17606', '17699'],
    'Omaha':    ['68104', '68105', '68106', '68124', '68127', '68134'],
    'Battle Creek': ['49014', '49015', '49016', '49017', '49018', '49037'],
    'Memphis':  ['38116', '38118', '38122', '38127', '38134', '38103'],
}

def random_phone(format = None):
    area_codes = [
        '201',
        '202',
        '203',
        '204',
        '205',
        '206',
        '207',
        '208',
        '209',
        '210',
        '212',
        '213',
        '214',
        '215',
        '216',
        '217',
        '218',
        '219',
        '220',
        '223',
        '224',
        '225',
        '226',
        '228',
        '229',
        '231',
        '234',
        '236',
        '239',
        '240',
        '242',
        '246',
        '248',
        '249',
        '250',
        '251',
        '252',
        '253',
        '254',
        '256',
        '260',
        '262',
        '264',
        '267',
        '268',
        '269',
        '270',
        '272',
        '276',
        '279',
        '281',
        '284',
        '289',
        '301',
        '302',
        '303',
        '304',
        '305',
        '306',
        '307',
        '308',
        '309',
        '310',
        '312',
        '313',
        '314',
        '315',
        '316',
        '317',
        '318',
        '319',
        '320',
        '321',
        '323',
        '325',
        '326',
        '330',
        '331',
        '332',
        '334',
        '336',
        '337',
        '339',
        '340',
        '341',
        '343',
        '345',
        '346',
        '347',
        '351',
        '352',
        '360',
        '361',
        '364',
        '365',
        '367',
        '368',
        '380',
        '385',
        '386',
        '401',
        '402',
        '403',
        '404',
        '405',
        '406',
        '407',
        '408',
        '409',
        '410',
        '412',
        '413',
        '414',
        '415',
        '416',
        '417',
        '418',
        '419',
        '423',
        '424',
        '425',
        '430',
        '431',
        '432',
        '434',
        '435',
        '437',
        '438',
        '440',
        '441',
        '442',
        '443',
        '445',
        '447',
        '448',
        '450',
        '456',
        '458',
        '463',
        '469',
        '470',
        '473',
        '474',
        '475',
        '478',
        '479',
        '480',
        '484',
        '500',
        '501',
        '502',
        '503',
        '504',
        '505',
        '506',
        '507',
        '508',
        '509',
        '510',
        '512',
        '513',
        '514',
        '515',
        '516',
        '517',
        '518',
        '519',
        '520',
        '530',
        '531',
        '533',
        '534',
        '539',
        '540',
        '541',
        '544',
        '548',
        '551',
        '559',
        '561',
        '562',
        '563',
        '564',
        '566',
        '567',
        '570',
        '571',
        '572',
        '573',
        '574',
        '575',
        '577',
        '579',
        '580',
        '581',
        '582',
        '585',
        '586',
        '587',
        '600',
        '601',
        '602',
        '603',
        '604',
        '605',
        '606',
        '607',
        '608',
        '609',
        '610',
        '612',
        '613',
        '614',
        '615',
        '616',
        '617',
        '618',
        '619',
        '620',
        '623',
        '626',
        '628',
        '629',
        '630',
        '631',
        '636',
        '639',
        '640',
        '641',
        '646',
        '647',
        '649',
        '650',
        '651',
        '657',
        '658',
        '659',
        '660',
        '661',
        '662',
        '664',
        '667',
        '669',
        '670',
        '671',
        '672',
        '678',
        '680',
        '681',
        '682',
        '684',
        '689',
        '700',
        '701',
        '702',
        '703',
        '704',
        '705',
        '706',
        '707',
        '708',
        '709',
        '710',
        '712',
        '713',
        '714',
        '715',
        '716',
        '717',
        '718',
        '719',
        '720',
        '721',
        '724',
        '725',
        '726',
        '727',
        '731',
        '732',
        '734',
        '737',
        '742',
        '740',
        '743',
        '747',
        '754',
        '757',
        '758',
        '760',
        '762',
        '763',
        '765',
        '767',
        '769',
        '770',
        '771',
        '772',
        '773',
        '774',
        '775',
        '778',
        '779',
        '780',
        '781',
        '782',
        '784',
        '785',
        '786',
        '787',
        '800',
        '801',
        '802',
        '803',
        '804',
        '805',
        '806',
        '807',
        '808',
        '809',
        '810',
        '812',
        '813',
        '814',
        '815',
        '816',
        '817',
        '818',
        '819',
        '820',
        '825',
        '828',
        '829',
        '830',
        '831',
        '832',
        '833',
        '838',
        '839',
        '840',
        '843',
        '844',
        '845',
        '847',
        '848',
        '849',
        '850',
        '854',
        '855',
        '856',
        '857',
        '858',
        '859',
        '860',
        '862',
        '863',
        '864',
        '865',
        '866',
        '867',
        '868',
        '869',
        '870',
        '872',
        '873',
        '876',
        '877',
        '878',
        '888',
        '900',
        '901',
        '902',
        '903',
        '904',
        '905',
        '906',
        '907',
        '908',
        '909',
        '910',
        '911',
        '912',
        '913',
        '914',
        '915',
        '916',
        '917',
        '918',
        '919',
        '920',
        '925',
        '928',
        '929',
        '930',
        '931',
        '934',
        '936',
        '937',
        '938',
        '939',
        '940',
        '941',
        '945',
        '947',
        '949',
        '951',
        '952',
        '954',
        '956',
        '959',
        '970',
        '971',
        '972',
        '973',
        '978',
        '979',
        '980',
        '984',
        '985',
        '986',
        '989',
    ]
    area_code = str(random.choice(area_codes))
    middle_three = str(random.randint(100,999))
    last_four = str(random.randint(1000,9999))

    if format is None:
        format = random.randint(0,4)

    if format==0:
        return area_code+middle_three+last_four
    elif format==1:
        return area_code+' '+middle_three+' '+last_four
    elif format==2:
        return area_code+'.'+middle_three+'.'+last_four
    elif format==3:
        return area_code+'-'+middle_three+'-'+last_four
    elif format==4:
        return '('+area_code+') '+middle_three+'-'+last_four
    

def random_email(name=None):
    if name == None:
        name = fake.name()
    
    emailData = [
        ['0', 'gmail.com', '17.74'],
        ['2', 'yahoo.com', '17.34'],
        ['3', 'hotmail.com', '15.53'],
        ['4', 'aol.com', '3.2'],
        ['5', 'hotmail.co.uk', '1.27'],
        ['6', 'hotmail.fr', '1.24'],
        ['7', 'msn.com', '1.09'],
        ['8', 'yahoo.fr', '0.98'],
        ['9', 'wanadoo.fr', '0.9'],
        ['10', 'orange.fr', '0.83'],
        ['11', 'comcast.net', '0.76'],
        ['12', 'yahoo.co.uk', '0.73'],
        ['13', 'yahoo.com.br', '0.69'],
        ['14', 'yahoo.co.in', '0.6'],
        ['15', 'live.com', '0.56'],
        ['16', 'rediffmail.com', '0.51'],
        ['17', 'free.fr', '0.51'],
        ['18', 'gmx.de', '0.44'],
        ['19', 'web.de', '0.43'],
        ['20', 'yandex.ru', '0.42'],
        ['21', 'ymail.com', '0.41'],
        ['22', 'libero.it', '0.38'],
        ['23', 'outlook.com', '0.38'],
        ['24', 'uol.com.br', '0.34'],
        ['25', 'bol.com.br', '0.33'],
        ['26', 'mail.ru', '0.32'],
        ['27', 'cox.net', '0.25'],
        ['28', 'hotmail.it', '0.25'],
        ['29', 'sbcglobal.net', '0.24'],
        ['30', 'sfr.fr', '0.23'],
        ['31', 'live.fr', '0.23'],
        ['32', 'verizon.net', '0.22'],
        ['33', 'live.co.uk', '0.21'],
        ['34', 'googlemail.com', '0.2'],
        ['35', 'yahoo.es', '0.2'],
        ['36', 'ig.com.br', '0.19'],
        ['37', 'live.nl', '0.19'],
        ['38', 'bigpond.com', '0.18'],
        ['39', 'terra.com.br', '0.17'],
        ['40', 'yahoo.it', '0.17'],
        ['41', 'neuf.fr', '0.17'],
        ['42', 'yahoo.de', '0.16'],
        ['43', 'alice.it', '0.16'],
        ['44', 'rocketmail.com', '0.15'],
        ['45', 'att.net', '0.15'],
        ['46', 'laposte.net', '0.15'],
        ['47', 'facebook.com', '0.15'],
        ['48', 'bellsouth.net', '0.15'],
        ['49', 'yahoo.in', '0.14'],
        ['50', 'hotmail.es', '0.13'],
        ['51', 'charter.net', '0.12'],
        ['52', 'yahoo.ca', '0.12'],
        ['53', 'yahoo.com.au', '0.12'],
        ['54', 'rambler.ru', '0.12'],
        ['55', 'hotmail.de', '0.11'],
        ['56', 'tiscali.it', '0.1'],
        ['57', 'shaw.ca', '0.1'],
        ['58', 'yahoo.co.jp', '0.1'],
        ['59', 'sky.com', '0.1'],
        ['60', 'earthlink.net', '0.09'],
        ['61', 'optonline.net', '0.09'],
        ['62', 'freenet.de', '0.09'],
        ['63', 't-online.de', '0.09'],
        ['64', 'aliceadsl.fr', '0.08'],
        ['65', 'virgilio.it', '0.08'],
        ['66', 'home.nl', '0.07'],
        ['67', 'qq.com', '0.07'],
        ['68', 'telenet.be', '0.07'],
        ['69', 'me.com', '0.07'],
        ['70', 'yahoo.com.ar', '0.07'],
        ['71', 'tiscali.co.uk', '0.07'],
        ['72', 'yahoo.com.mx', '0.07'],
        ['73', 'voila.fr', '0.06'],
        ['74', 'gmx.net', '0.06'],
        ['75', 'mail.com', '0.06'],
        ['76', 'planet.nl', '0.06'],
        ['77', 'tin.it', '0.06'],
        ['78', 'live.it', '0.06'],
        ['79', 'ntlworld.com', '0.06'],
        ['80', 'arcor.de', '0.06'],
        ['81', 'yahoo.co.id', '0.06'],
        ['82', 'frontiernet.net', '0.06'],
        ['83', 'hetnet.nl', '0.05'],
        ['84', 'live.com.au', '0.05'],
        ['85', 'yahoo.com.sg', '0.05'],
        ['86', 'zonnet.nl', '0.05'],
        ['87', 'club-internet.fr', '0.05'],
        ['88', 'juno.com', '0.05'],
        ['89', 'optusnet.com.au', '0.05'],
        ['90', 'blueyonder.co.uk', '0.05'],
        ['91', 'bluewin.ch', '0.05'],
        ['92', 'skynet.be', '0.05'],
        ['93', 'sympatico.ca', '0.05'],
        ['94', 'windstream.net', '0.05'],
        ['95', 'mac.com', '0.05'],
        ['96', 'centurytel.net', '0.05'],
        ['97', 'chello.nl', '0.04'],
        ['98', 'live.ca', '0.04'],
        ['99', 'aim.com', '0.04'],
        ['100', 'bigpond.net.au', '0.04']
    ]

    mailGens = [lambda fn, ln, *names: fn + ln,
                lambda fn, ln, *names: fn + "." + ln,
                lambda fn, ln, *names: fn + "_" + ln,
                lambda fn, ln, *names: fn[0] + "." + ln,
                lambda fn, ln, *names: fn[0] + "_" + ln,
                lambda fn, ln, *names: fn + ln + str(int(1/random.random()**3)),
                lambda fn, ln, *names: fn + "." + ln + str(int(1/random.random()**3)),
                lambda fn, ln, *names: fn + "_" + ln + str(int(1/random.random()**3)),
                lambda fn, ln, *names: fn[0] + "." + ln + str(int(1/random.random()**3)),
                lambda fn, ln, *names: fn[0] + "_" + ln + str(int(1/random.random()**3)),]

    mailGenWeights = [1, 0.9, 0.95, 0.8, 0.7, 0.75, 0.7, 0.7, 0.6, 0.5]

    emailChoices = [float(line[2]) for line in emailData]

    return random.choices(mailGens, mailGenWeights)[0](*name.split(" ")).lower() + "@" + random.choices(emailData, emailChoices)[0][1]



def start_driver(rand_num):
    driver = webdriver.Chrome(chromedriver_location)
    driver.get(urls[rand_num])
    # driver.manage().timeouts().pageLoadTimeout(5, SECONDS)
    # time.sleep(10)
    driver.implicitly_wait(10)
    time.sleep(2)
    driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[2]/div/div[1]/div[1]/div/div/button').click()
    driver.find_element_by_xpath(
        '//*[@id="applyOption-top-manual"]').click()
    driver.find_element_by_xpath(
        '//*[@id="page_content"]/div[2]/div/div/div[2]/div/div/div[2]/a').click()
    return driver

def generate_account(driver, rand_num, fake_identity):
    # make fake account info and fill
    password = fake.password()
    for key in data.keys():
        match key:
            case 'email' | 'email-retype':
                info = fake_identity['email']
            case 'pass' | 'pass-retype':
                info = password
            case 'first_name':
                info = fake_identity['first_name']
            case 'last_name':
                info = fake_identity['last_name']
            case 'pn':
                info = random_phone()

        driver.find_element_by_xpath(data.get(key)).send_keys(info)
        
    time.sleep(random.randint(0, 2))
    select = Select(driver.find_element_by_id('fbclc_ituCode'))
    select.select_by_value('US')
    select = Select(driver.find_element_by_id('fbclc_country'))
    select.select_by_value('US')

    driver.find_element_by_xpath('//*[@id="dataPrivacyId"]').click()
    time.sleep(1.5)
    driver.find_element_by_xpath('//*[@id="dlgButton_20:"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="fbclc_createAccountButton"]').click()

    time.sleep(1.5)

    print(f"successfully made account for fake email {fake_identity['email']}")

def fill_out_application_and_submit(driver, rand_num, fake_identity):

    driver.implicitly_wait(10)
    city = list(cities.keys())[rand_num]

    # make resume
    resume_filename = fake_identity['last_name']+'-Resume'
    make_resume(fake_identity['first_name']+' '+fake_identity['last_name'], fake_identity['email'], resume_filename+'.pdf')
    images = convert_from_path(resume_filename+'.pdf')
    images[0].save(resume_filename+'.png', 'PNG')
    
    # fill out form parts of app
    driver.find_element_by_xpath('//*[@id="109:topBar"]').click()
    driver.find_element_by_xpath('//*[@id="260:topBar"]').click()

    zip_num = random.randint(0, 4)

    for key in data2.keys():

        match key:
            case 'resume':
                driver.find_element_by_xpath('//*[@id="48:_attach"]/div[6]').click()
                info = os.getcwd()+'/'+resume_filename+'.png'
            case 'addy':
                info = fake.street_address()
            case 'city':
                info = city
            case 'zip':
                zipp = zip_codes[city]
                info = zipp[zip_num]
            case 'job':
                info = fake.job()
            case 'salary':
                info = random.randint(15, 35)

        driver.find_element_by_xpath(data2.get(key)).send_keys(info)

    print(f"successfully filled out app forms for {city}")

    # fill out dropdowns
    select = Select(driver.find_element_by_id('154:_select'))
    select.select_by_visible_text('Yes')
    select = Select(driver.find_element_by_id('195:_select'))
    select.select_by_visible_text('United States')

    select = Select(driver.find_element_by_id('211:_select'))
    select.select_by_visible_text('Yes')
    select = Select(driver.find_element_by_id('215:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('219:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('223:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('227:_select'))
    select.select_by_visible_text('No')
    select = Select(driver.find_element_by_id('231:_select'))
    select.select_by_visible_text('Yes')
    select = Select(driver.find_element_by_id('223:_select'))
    select.select_by_visible_text('No')

    time.sleep(1)

    select = Select(driver.find_element_by_id('235:_select'))
    gender = random.choice(['Male', 'Female', 'Other'])
    select.select_by_visible_text(gender)

    driver.find_element_by_xpath('//label[text()="350 LBS"]').click()
    driver.find_element_by_xpath('//label[text()="800 LBS"]').click()
    els = driver.find_elements_by_xpath('//label[text()="Yes"]')
    for el in els:
        el.click()

    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="261:_submitBtn"]').click()
    print(f"successfully submitted application")

    # take out the trash
    os.remove(resume_filename+'.pdf')
    os.remove(resume_filename+'.png')

def main():
    for _ in range(10000):
        rand_num = random.randint(0, 3)
        try:
            driver = start_driver(rand_num)
        except Exception as e:
            print(f"failed to start driver: {str(e)}")
            driver.close()
            continue

        time.sleep(2)

        fake_first_name = fake.first_name()
        fake_last_name = fake.last_name()
        fake_email = random_email(fake_first_name+' '+fake_last_name)

        fake_identity = {
            'first_name': fake_first_name,
            'last_name': fake_last_name,
            'email': fake_email
        }

        try:
            generate_account(driver, rand_num, fake_identity)
        except Exception as e:
            print(f"failed to create account: {str(e)}")
            driver.close()
            continue

        try:
            fill_out_application_and_submit(driver, rand_num, fake_identity)
        except Exception as e:
            print(f"failed to fill out app and submit: {str(e)}")
            driver.close()
            continue

        driver.close()
        time.sleep(5)

if __name__ == '__main__':
    main()
    sys.exit()
