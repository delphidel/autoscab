import time
import random
import datetime
import pdb
import requests as req
import json
from autoscab.deployments.deployment import Deployment
from autoscab.constants.locators import KingSoopersLocator
from autoscab.constants.common import NOS, NAS
from autoscab.postbot import PostBot
from autoscab.constants.location import load_cities
from pprint import pformat
from autoscab.logger import init_logger


class KingSoopersPostbot(PostBot):

    def __postinit__(self):
        # get some random location info
        cities = load_cities()
        colorado = cities[cities['state_id'] == 'CO']
        row = colorado.sample(1)
        self.identity.city = row.city.values[0]
        self.identity.state = 'Colorado'
        self.identity.zip = random.choice(row.zips.values.tolist()[0].split(' '))
        self.logger.info(f'Applying for job with identity:\n{pformat(self.identity.__dict__)}')

    def apply(self):
        self.choose_position()
        self.make_account()
        self.fill_application()

    def choose_position(self):
        self.positions.click()
        time.sleep(2)
        # stash current window handle
        current_window = self.browser.current_window_handle
        self.apply_button.click()
        time.sleep(5)
        # this opens a new tab.
        for handle in self.browser.window_handles:
            if handle != current_window:
                self.browser.switch_to.window(handle)
                break
        self.logger.success('Position chosen, making account')


    def make_account(self):
        # "make new account"
        self.new_account.click()
        self.random_sleep(3,5)

        # fill in form fields
        self.newacct_email.send_keys(self.identity.email)
        self.random_sleep()
        self.newacct_email_conf.send_keys(self.identity.email)
        self.random_sleep()
        self.newacct_pass.send_keys(self.identity.password)
        self.random_sleep()
        self.newacct_pass_conf.send_keys(self.identity.password)
        self.random_sleep()
        self.newacct_first.send_keys(self.identity.name[0])
        self.random_sleep()
        self.newacct_last.send_keys(self.identity.name[1])
        self.random_sleep()
        self.newacct_us.click()
        self.random_sleep()

        # click privacy waiver dialogue
        self.newacct_privacy.click()
        self.random_sleep()
        self.newacct_privacy_accept.click()
        self.random_sleep()

        # make account
        self.newacct_create.click()
        self.logger.success('Account created, waiting up to 45s for application to load')
        self.random_sleep(5,6)
        # long sleep, their backend is slow.
        self.sleep_until_clickable('app_upload_resume', timeout=45)
        # self.random_sleep(15,20)
        self.logger.success('Application Loaded, filling...')

    def fill_application(self):
        # upload documents
        self.app_upload_resume.click()
        self.random_sleep()
        self._tracebacks = False
        self.app_file_input.send_keys(str(self.identity.resume))
        self.random_sleep(2,3)
        self._tracebacks = True
        self.app_phone.send_keys(self.identity.phone)
        self.random_sleep()
        self.app_state_or.click()
        self.random_sleep()
        self.app_address.send_keys(self.identity.address)
        self.random_sleep()
        self.app_city.send_keys(self.identity.city)
        self.random_sleep()
        self.app_zip.send_keys(self.identity.zip)
        self.random_sleep()

        self.app_ssn.send_keys(self.identity.ssn)

        # fuck it click all the rest of the buttons
        for anattr in [
            "app_heard_other",
            "app_no_education",
            "app_high_school",
            "app_not_related",
            "app_notvet",
            "app_yes18",
            "app_notobacco",
            "app_preference1",
            "app_preference2",
            "app_evenings",
            "app_weekends",
            "app_holidays",
            "app_parttime",
            "app_callanytime",
            "available_sunday",
            "available_monday",
            "available_tues",
            "available_weds",
            "available_thurs",
            "available_fri",
            "available_sat",
            "notfired",
            "nostealing",
            "app_nocrime",
            "app_emergency_other",
            "app_sig_acknowledge",
            "app_am15",
            "app_am16",
            "app_am18",
            "app_am21",
            "app_legaltowork",
            "app_bgcheck"]:
            try:
                button = getattr(self, anattr)
                button.click()
                self.random_sleep(0, 0.5)
            except:
                self.logger.warn("An error occurred pressing button {}".format(anattr))

        # give a random day int he future as a start date
        futuredate = datetime.date.today() + datetime.timedelta(days=random.randint(1,14))
        datestr = futuredate.strftime('%m/%d/%Y')
        self.app_available.send_keys(datestr)
        self.random_sleep()

        self.previous_kroger.send_keys(random.choice(NAS))
        self.random_sleep()
        self.previous_retail.send_keys(random.choice(NOS))
        self.random_sleep()

        self.app_crime_signature.send_keys(' '.join(self.identity.name))

        # fake emergency contact
        self.app_emergency_lname.send_keys(self.identity.faker.first_name())
        self.random_sleep()
        self.app_emergency_fname.send_keys(self.identity.faker.last_name())
        self.random_sleep()
        self.app_emergency_phone.send_keys(self.identity.faker.phone_number())
        self.random_sleep()

        self.app_sig.send_keys(' '.join(self.identity.name))

        self.random_sleep()
        self.submit_application.click()
        self.random_sleep(10,15)
        self.logger.success("Completed Application!")

def get_deployment_urls():

    logger = init_logger('kingsoopers-postbot')

    # get ten random position ID from the search for 'king soopers temporary'; wrap in a query URL
    ids = []

    queryFmt = 'https://kroger.eightfold.ai/api/apply/v2/jobs?domain=kroger.com&domain=kroger.com&start={}&num=10&location=colorado&query=temporary'

    logger.info("Polling for ids...")

    # first query gets count
    start = 0
    r = req.get(queryFmt.format(start))
    count = json.loads(r.text)['count']
    logger.info("Getting 10 ids from {} total matches".format(count))

    # second query gets a random set of ten
    r = req.get(queryFmt.format(random.randint(0,count-10)))
    logger.info("Made the last API call, extracting...".format(count))    
    positions = json.loads(r.text)['positions']
    for pos in positions:
        ids.append(pos['id'])

    logger.info("Got {} ids! Making urls...".format(len(ids)))

    urls = []
    urlFmt = 'https://kroger.eightfold.ai/careers?pid={}'
    for this_id in ids:
        urls.append(urlFmt.format(this_id))
    return urls

KingSoopersDeployment = Deployment(
    name="kingsoopers",
#    urls=get_deployment_urls(),
    urls=['https://kroger.eightfold.ai/careers?pid=10496566',
          'https://kroger.eightfold.ai/careers?pid=10496587',
          'https://kroger.eightfold.ai/careers?pid=10496342',
          'https://kroger.eightfold.ai/careers?pid=10496575',
          'https://kroger.eightfold.ai/careers?pid=10496588',
          'https://kroger.eightfold.ai/careers?pid=10302982',
          'https://kroger.eightfold.ai/careers?pid=10302912',
          'https://kroger.eightfold.ai/careers?pid=10302903',
          'https://kroger.eightfold.ai/careers?pid=10302985',
          'https://kroger.eightfold.ai/careers?pid=10302904',
          'https://kroger.eightfold.ai/careers?pid=10302821',
          'https://kroger.eightfold.ai/careers?pid=10302782',
          'https://kroger.eightfold.ai/careers?pid=10302897',
          'https://kroger.eightfold.ai/careers?pid=10302905',
          'https://kroger.eightfold.ai/careers?pid=10302902',
          'https://kroger.eightfold.ai/careers?pid=10302884',
          'https://kroger.eightfold.ai/careers?pid=10302930',
          'https://kroger.eightfold.ai/careers?pid=10302900',
          'https://kroger.eightfold.ai/careers?pid=10302779',
          'https://kroger.eightfold.ai/careers?pid=10302696',
          'https://kroger.eightfold.ai/careers?pid=10302835',
          'https://kroger.eightfold.ai/careers?pid=10302929',
          'https://kroger.eightfold.ai/careers?pid=10302920',
          'https://kroger.eightfold.ai/careers?pid=10303010',
          'https://kroger.eightfold.ai/careers?pid=10303002',
          'https://kroger.eightfold.ai/careers?pid=10302911',
          'https://kroger.eightfold.ai/careers?pid=10303004',
          'https://kroger.eightfold.ai/careers?pid=10302883',
          'https://kroger.eightfold.ai/careers?pid=10302915',
          'https://kroger.eightfold.ai/careers?pid=10302778',
          'https://kroger.eightfold.ai/careers?pid=10302908',
          'https://kroger.eightfold.ai/careers?pid=10302792',
          'https://kroger.eightfold.ai/careers?pid=10302916',
          'https://kroger.eightfold.ai/careers?pid=10302931',
          'https://kroger.eightfold.ai/careers?pid=10302956',
          'https://kroger.eightfold.ai/careers?pid=10302955',
          'https://kroger.eightfold.ai/careers?pid=10302935',
          'https://kroger.eightfold.ai/careers?pid=10302909',
          'https://kroger.eightfold.ai/careers?pid=10302798',
          'https://kroger.eightfold.ai/careers?pid=10302766',
          'https://kroger.eightfold.ai/careers?pid=10302940',
          'https://kroger.eightfold.ai/careers?pid=10302941',
          'https://kroger.eightfold.ai/careers?pid=10302968',
          'https://kroger.eightfold.ai/careers?pid=10302810',
          'https://kroger.eightfold.ai/careers?pid=10302917',
          'https://kroger.eightfold.ai/careers?pid=10302901',
          'https://kroger.eightfold.ai/careers?pid=10302819',
          'https://kroger.eightfold.ai/careers?pid=10302777',
          'https://kroger.eightfold.ai/careers?pid=10303016',
          'https://kroger.eightfold.ai/careers?pid=10302925',
          'https://kroger.eightfold.ai/careers?pid=10302786',
          'https://kroger.eightfold.ai/careers?pid=10302695',
          'https://kroger.eightfold.ai/careers?pid=10302789',
          'https://kroger.eightfold.ai/careers?pid=10302898',
          'https://kroger.eightfold.ai/careers?pid=10302932',
          'https://kroger.eightfold.ai/careers?pid=10302923',
          'https://kroger.eightfold.ai/careers?pid=10302914',
          'https://kroger.eightfold.ai/careers?pid=10302796',
          'https://kroger.eightfold.ai/careers?pid=10302811',
          'https://kroger.eightfold.ai/careers?pid=10302827',
          'https://kroger.eightfold.ai/careers?pid=10302834',
          'https://kroger.eightfold.ai/careers?pid=10302701',
          'https://kroger.eightfold.ai/careers?pid=10302764',
          'https://kroger.eightfold.ai/careers?pid=10302899',
          'https://kroger.eightfold.ai/careers?pid=10302825',
          'https://kroger.eightfold.ai/careers?pid=10302886',
          'https://kroger.eightfold.ai/careers?pid=10302781',
          'https://kroger.eightfold.ai/careers?pid=10302759',
          'https://kroger.eightfold.ai/careers?pid=10302761',
          'https://kroger.eightfold.ai/careers?pid=10302924',
          'https://kroger.eightfold.ai/careers?pid=10302767',
          'https://kroger.eightfold.ai/careers?pid=10302907',
          'https://kroger.eightfold.ai/careers?pid=10302769',
          'https://kroger.eightfold.ai/careers?pid=10302910',
          'https://kroger.eightfold.ai/careers?pid=10302954',
          'https://kroger.eightfold.ai/careers?pid=10302896',
          'https://kroger.eightfold.ai/careers?pid=10302979',
          'https://kroger.eightfold.ai/careers?pid=10302969',
          'https://kroger.eightfold.ai/careers?pid=10303014',
          'https://kroger.eightfold.ai/careers?pid=10302885',
          'https://kroger.eightfold.ai/careers?pid=10302765',
          'https://kroger.eightfold.ai/careers?pid=10302788',
          'https://kroger.eightfold.ai/careers?pid=10302774',
          'https://kroger.eightfold.ai/careers?pid=10302760',
          'https://kroger.eightfold.ai/careers?pid=10302822',
          'https://kroger.eightfold.ai/careers?pid=10302728',
          'https://kroger.eightfold.ai/careers?pid=10302824',
          'https://kroger.eightfold.ai/careers?pid=10302762',
          'https://kroger.eightfold.ai/careers?pid=10302773',
          'https://kroger.eightfold.ai/careers?pid=10302744',
          'https://kroger.eightfold.ai/careers?pid=10302743'],
#    urls=['https://kroger.eightfold.ai/careers?pid=10302982&location=colorado&query=king%20soopers%20temporary&domain=kroger.com&triggerGoButton=false'],
#    urls = ['https://kroger.eightfold.ai/careers?query=king+soopers&domain=kroger.com&location_distance_km=100&messenger=email'],
    locators=dict(KingSoopersLocator.__dict__),
    postbot=KingSoopersPostbot
)
