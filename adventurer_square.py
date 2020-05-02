from enum import Enum
from bs4 import BeautifulSoup
import requests
import re
import time


class PageList(Enum):
    TOP = 'https://hiroba.dqx.jp/sc/'
    TOKOYAMI_STRENGTH = 'https://hiroba.dqx.jp/sc/tokoyami/'
    TENGOKU = 'https://hiroba.dqx.jp/sc/game/tengoku'


bazaar_url_template = 'https://hiroba.dqx.jp/sc/search/bazaar/{item_id}/0/page/{page}'
market_price_pattern = re.compile(r'\D*(?P<price>(\d|,)+)\s*G')


class AdventurerSquareError(Exception):
    pass


class AdventurerSquare:
    def __init__(self):
        self.username = None
        self.password = None
        self.session = requests.Session()

    def login(self, username: str, password: str):
        login_page = self.session.get('https://hiroba.dqx.jp/sc/login')
        login_page_content = BeautifulSoup(login_page.content, 'lxml')
        stored_hidden = login_page_content.find('input', attrs={'name': '_STORED_', 'type': 'hidden'})['value']
        form_action = login_page_content.find('form', attrs={'name': 'login'})['action']
        post_target_url = 'https://secure.square-enix.com/oauth/oa/' + form_action

        main_form_page = self.session.post(post_target_url,
                                           params={
                                               'sqexid': username,
                                               'password': password,
                                               '_STORED_': stored_hidden,
                                           })
        main_form_page_content = BeautifulSoup(main_form_page.content, 'lxml')
        post_target_url = main_form_page_content.find('form', attrs={'name': 'mainForm'})['action']
        cis_sessid_hidden = main_form_page_content.find('input', attrs={'name': 'cis_sessid', 'type': 'hidden'})['value']
        provision_hidden = main_form_page_content.find('input', attrs={'name': 'provision', 'type': 'hidden'})['value']
        c_hidden = main_form_page_content.find('input', attrs={'name': '_c', 'type': 'hidden'})['value']

        self.session.post(post_target_url,
                          params={
                              'cis_sessid': cis_sessid_hidden,
                              'provision': provision_hidden,
                              '_c': c_hidden
                          })
        character_choice_page = self.session.get('https://hiroba.dqx.jp/sc/login/characterselect/')
        character_choice_page_content = BeautifulSoup(character_choice_page.content, 'lxml')
        cid_hidden = character_choice_page_content.find('a', attrs={'class': 'button submitBtn charselect centering'})['rel']

        self.session.post('https://hiroba.dqx.jp/sc/login/characterexec',
                          params={
                              'cid': cid_hidden
                          })
        self.username = username
        self.password = password
        return self

    def close(self):
        self.session.close()

    def get_tokoyami_strength(self):
        page = self.session.get(PageList.TOKOYAMI_STRENGTH.value)
        tokoyami_table = BeautifulSoup(page.content, 'lxml').find('table', 'tokoyami')
        tokoyami_records = tokoyami_table.find_all('tr')[1:]
        tokoyami_strength = list(
            map(lambda record: record.find_all('td')[1].find('img').get('src')[61:62], tokoyami_records))
        return {
            'regiro': tokoyami_strength[0],
            'scorpide': tokoyami_strength[1],
            'gerzark': tokoyami_strength[2],
            'gardodon': tokoyami_strength[3]
        }

    def get_tengoku_status(self):
        page = self.session.get(PageList.TENGOKU.value)
        soup = BeautifulSoup(page.content, 'html.parser')
        is_closed = soup.find('div', 'tengoku is-close') is not None

        if is_closed:
            return {
                'opened': False
            }

        try:
            status_div = soup.find('div', 'tengoku is-open')
            period_div = status_div.find('div', 'tengoku__period')
            periods = list(map(lambda period: period.get_text(), period_div.find_all('span')[1::2]))

            conditions_table = soup.find('table', 'tengoku-x-table')
            condition_trs = conditions_table.find_all('tr')
            battle_condition_trs = condition_trs[3:8]
            item_condition_tr = condition_trs[-1]

            battle_condition_contents = list(
                map(lambda condition: condition.find('td').get_text().strip(), battle_condition_trs))

            item_condition_contents = list(map(lambda condition: '・ ' + condition.get_text(),
                                               item_condition_tr.find('div', 'tengoku-x-table_items-list').find_all('div')))
        except AttributeError as error:
            raise AdventurerSquareError('failed to get tengoku status.') from error

        return {
            'opened': True,
            'period': {
                'start_date': periods[0],
                'end_date': periods[1]
            },
            'battle_conditions': battle_condition_contents,
            'item_conditions': item_condition_contents
        }

    def get_item_name_by_id(self, item_id: str) -> str:
        item_url = 'https://hiroba.dqx.jp/sc/game/item/{item_id}/'.format(
            item_id=item_id
        )
        item_page = self.session.get(item_url)
        item_page_content = BeautifulSoup(item_page.content, 'lxml')
        item_page_data_table_tr = item_page_content.select_one('.dataTable .dataTableTd td div table tr')
        if item_page_data_table_tr is None:
            return None

        item_name = item_page_data_table_tr.find_all('td')[2].get_text()
        return item_name

    def get_market_price(self, item_id: str) -> int:
        if self.username is None or self.password is None:
            raise AssertionError('adventurer square login failed. username or password is empty')

        item_page = self.session.get(bazaar_url_template.format(item_id=item_id, page=0))
        item_page_content = BeautifulSoup(item_page.content, 'lxml')
        item_list_tr = item_page_content.find('table', attrs={'class': 'bazaarTable bazaarlist'}).find_all('tr')[1]
        if item_list_tr is None:
            return None

        item_price_td = item_list_tr.find_all('td')[1]
        item_price_p = item_price_td.find_all('p')[1]

        item_unit_price_span = item_price_p.find('span')
        if item_unit_price_span is None:
            target_price_tag = item_price_p
        else:
            target_price_tag = item_unit_price_span

        market_price_value = market_price_pattern.match(target_price_tag.get_text())
        time.sleep(2)
        return int(market_price_value.group('price'))
