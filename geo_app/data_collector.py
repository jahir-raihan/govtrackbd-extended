from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
from .models import Project
requests.packages.urllib3.disable_warnings()


class LgedCrawler:

    def __init__(self):
        self.__all_tables = None
        self.__dic = {}

    def execute_data_aggregation(self, data):

        """Main data aggregator method"""

        __html_data = BeautifulSoup(data.text, 'html.parser')
        self.__all_tables = __html_data.find_all('table')

        # Method call to aggregate data from the tables
        self.get_broader_table_data()
        self.get_short_info_data()
        self.get_image_url()

        # Method Call to store data in database
        self.store_data()

    def get_broader_table_data(self):

        """Collects data from Table 1, called as Broader Information Table"""

        broader_table = self.__all_tables[2]
        bt_rows = broader_table.find_all('tr')[1:]

        # Storing all data in a dictionary
        for row in bt_rows:
            columns = row.find_all('td')
            self.__dic[columns[0].get_text().strip()] = columns[2].get_text().strip()

    def get_short_info_data(self):

        """Collects data from Table 2, called as At a Glance or Short Info Table, but the
            Data inside is valid."""

        short_inf_table = self.__all_tables[3]
        st_rows = short_inf_table.find_all('tr')

        # Storing all data in a dictionary
        for row in st_rows:
            columns = row.find_all('td')
            self.__dic[columns[0].get_text().strip()[:-1]] = columns[1].get_text().strip()

    def get_image_url(self):

        """To get project image url, if image is given for the project"""

        image_table = self.__all_tables[0]
        url = 'https://oldweb.lged.gov.bd/' + image_table.tr.td.img['src']
        self.__dic['image'] = url

    def store_data(self):

        """Stores data in the database"""

        data = self.__dic

        for k, v in data.items():
            print(k, ' : ', v)

        if data['Project Code'] == '':
            return

        try:
            proj = Project.objects.get(project_code=data['Project Code'], category='LGED')
        except:
            proj = Project(project_code=data['Project Code'], category='LGED')

        proj.project_name = data['Project Name']
        proj.pd_name = data['Name of PD']
        proj.start_date = datetime.strptime(data['Start Date'], '%b-%Y')
        proj.completion_date = datetime.strptime(data['Completion Date'], '%b-%Y')
        proj.funded_by = data['Funded By']
        proj.budget = data['Budget']
        proj.sector = data['Sector']
        proj.status = data['Status']
        proj.approval_ref = data['Approval Ref']
        proj.executing_agency = data['Executing Agency']
        proj.ministry = data['Ministry']
        proj.short_title = data['Short Title']
        proj.note = data['Comments']
        proj.physical_progress = data['Physical Progress (%)']
        proj.cumulative_expenditure = data['Cumulative Expenditure']
        proj.date_of_approval = data['Date of Approval']
        proj.image = data['image']
        proj.implementing_agency = data['Implementing Agency']
        proj.save()

    def get_data(self):

        """Returns current data."""
        return self.__dic


def crawl_lged():

    """Main driver function to crawl and collect project data from LGED website."""

    for i in range(2, 1040):  # I know it's current projects count.
        try:
            response_data = requests.get(f'https://oldweb.lged.gov.bd/ProjectHome.aspx?projectID={i}')

            store_data = LgedCrawler()
            store_data.execute_data_aggregation(response_data)

            i += 1


        except:
            pass


# NDRE Crawler


class NdReCrawler:

    def __init__(self):
        self.notifier = False
        self.sids_list = []

    def execute_operation(self):

        """Main driver method for execution"""

        # Collect sids
        self.collect_sids()

        # Scrap datas using sids
        self.scrap_data()

    def collect_sids(self):

        """Collects sids by crawling over NDRE website and crawls until it reaches the end"""

        # Loop terminator
        is_end = True

        # Paginator
        page = 1

        # Main loop
        while is_end:

            # Get data
            data = self.request_data('https://ndre.sreda.gov.bd/index.php?id=1&i=0&pg=', page)

            # Get the required table
            table = data.find_all('table')[0]

            # Collect all table rows
            all_rows = table.find_all('tr')
            rows = all_rows[3:]
            sids = []

            # Loop over rows
            for r in rows:

                # Only collect sids from the row
                column = r.find_all('td')[2]
                sids.append(column.text.strip())

            # If there's no sids terminate the loop in next iteration
            if len(sids) == 0:
                is_end = False

            # Else append sids to the main sids_list for scrapping and increase the paginator by one
            else:
                self.sids_list.extend(sids)
                page += 1

    def scrap_data(self):

        """Scraps data from webpage by using sids collected previously, and stores them in a dictionary.
            We can use the dictionary to use these collected data anywhere we want.

            NOTE :
                When we scrap over the page, the page has only one root table, which is than divided into sub tables,
                like a nested list. So it was bit tricky to figure out how to get the exact table data.
                That's why there's a nasty table calls and row calls over the table only for collecting valid and
                accurate data.
            """

        # Looping over sids list
        for sids in self.sids_list:

            # Get data
            data = self.request_data('https://ndre.sreda.gov.bd/index.php?id=06&kid=', sids)

            dic = {}
            # Getting all tables
            table = data.find_all('table')

            # Getting first table rows, which is sub first table of root table
            rows = table[0].find_all('tr')[0].find_all('table')[0]

            # Finding all rows
            row = rows.find_all('tr')

            # Try and except block for error handling
            try:

                # Looping over all rows
                for r in row[1:]:

                    # Getting columns
                    col = r.find_all('td')

                    # Adding columns to the tmp dictionary
                    dic[col[0].text.strip()] = col[2].text.strip()

                # Getting second table rows, which is sub second table of the root table
                rows1 = table[0].find_all('tr')[0].find_all('table')[1]

                # Finding all rows init
                row1 = rows1.find_all('tr')

                # Looping over all rows
                for r in row1[1:]:

                    # Getting all columns
                    col = r.find_all('td')

                    # Adding columns to the tmp dictionary
                    dic[col[0].text.strip()] = col[2].text.strip()
            except:
                continue

            # Add to the database, or update on database
            try:
                proj = Project.objects.get(project_code=sids, category='NDRE')

            except:
                proj = Project(project_code=sids, category='NDRE')

            self.save_to_db(proj, dic)

    def save_to_db(self, proj, dic):
        lat_lng = dic['Latitude, Longitude'].split(',')
        proj.project_name = dic['System Name']
        proj.technology_type = dic['Technology Type']
        proj.capacity = dic['Capacity']
        proj.completion_date = datetime.strptime(dic['Completion Date'], '%Y-%m-%d')
        proj.present_status = dic['Present Status']
        proj.funded_by = dic['Financing Org.']
        proj.implementing_agency = dic['Implementing Agency']
        proj.pd_name = dic['PD Name']
        proj.division = dic['Division']
        proj.district = dic['District']
        proj.upazilla = dic['Upazilla']
        proj.grid_status = dic['Grid Status']
        proj.location = dic['Location']
        proj.latitude, proj.longitude = lat_lng[0], lat_lng[1]
        proj.note = dic['Note']
        proj.expected_life_time = dic['Expected Energy Generation and CO2 Emission reduction during System Life']
        proj.expected_till_now = dic['Expected Energy Generation and CO2 Emission reduction till today']
        proj.save()
        self.notifier = True

    def request_data(self, url, arg):

        """Sends requests to given url with argument and gets html data in text format, then returns
            it as BS4 datatype for further operation"""

        self.notifier = True  # Only for ignoring annoying style guide

        # Getting html response, converting that to text and converting to BS4 data type and returning it.
        html_data = requests.get(f'{url}{arg}', verify=False).text

        return BeautifulSoup(html_data, 'html.parser')


def crawl_ndre():

    obj = NdReCrawler()
    obj.execute_operation()


