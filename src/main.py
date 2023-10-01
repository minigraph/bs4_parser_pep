import csv
import datetime as dt
import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DATETIME_FORMAT, EXPECTED_STATUS,
                       MAIN_DOC_URL, PEP_URL, HTMLTag, HTMLAttr, HTMLValue)
from outputs import control_output
from utils import find_tag, get_response

# Паттерн поиска версии и статуса ссылки
PATTERN_VS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
# Паттерн поиска ссылки на архив документации
PATTERN_HREF = r'.+pdf-a4\.zip$'
FEATURE_LXML = 'lxml'


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if not response:
        return

    soup = BeautifulSoup(response.text, features=FEATURE_LXML)
    main_div = find_tag(
        soup,
        HTMLTag.SECTION,
        attrs={HTMLAttr.ID: HTMLValue.WHATNEW}
    )
    div_with_ul = find_tag(
        main_div,
        HTMLTag.DIV,
        attrs={HTMLAttr.CLASS: HTMLValue.TREE_WR}
    )
    sections_by_python = div_with_ul.find_all(
        HTMLTag.LI,
        attrs={HTMLAttr.CLASS: HTMLValue.TREE_L1}
    )

    result = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, HTMLTag.A)
        version_link = urljoin(whats_new_url, version_a_tag[HTMLAttr.HREF])

        response = get_response(session, version_link)
        if not response:
            continue

        soup = BeautifulSoup(response.text, features=FEATURE_LXML)
        h1, dl = find_tag(soup, HTMLTag.H1), find_tag(soup, HTMLTag.DL)
        dl_text = dl.text.replace('\n', ' ')
        result.append((version_link, h1.text, dl_text))

    return result


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if not response:
        return

    soup = BeautifulSoup(response.text, features=FEATURE_LXML)
    sidebar = find_tag(
        soup,
        HTMLTag.DIV,
        attrs={HTMLAttr.CLASS: HTMLValue.SPHINX}
    )
    ul_tags = sidebar.find_all(HTMLTag.UL)
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all(HTMLTag.A)
            break
    else:
        raise Exception('Ничего не нашлось')

    result = [('Ссылка на документацию', 'Версия', 'Статус')]
    for a in a_tags:
        link = a[HTMLAttr.HREF]
        text_match = re.search(PATTERN_VS, a.text)
        version, status = a.text, ''
        if text_match is not None:
            version, status = text_match.groups()

        result.append((link, version, status))

    return result


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if not response:
        return

    soup = BeautifulSoup(response.text, features=FEATURE_LXML)
    table_tag = find_tag(
        soup,
        HTMLTag.TABLE,
        {HTMLAttr.CLASS: HTMLValue.DOCUTILS}
    )
    pdf_a4_tag = find_tag(
        table_tag,
        HTMLTag.A,
        {HTMLAttr.HREF: re.compile(PATTERN_HREF)}
    )

    archive_url = urljoin(downloads_url, pdf_a4_tag[HTMLAttr.HREF])
    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)

    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    if not response:
        return

    dict_status, list_error_status = dict(), []
    soup = BeautifulSoup(response.text, features=FEATURE_LXML)
    section = find_tag(
        soup,
        HTMLTag.SECTION,
        {HTMLAttr.ID: HTMLValue.PEP_CONTENT}
    )
    tag_tables = section.find_all(
        HTMLTag.TABLE,
        {HTMLAttr.CLASS: HTMLValue.PEP_ZERO}
    )
    for table in tag_tables:
        tbody = find_tag(table, HTMLTag.TBODY)
        tr_rows = tbody.find_all(HTMLTag.TR)
        for row in tr_rows:
            pep_a_tag = find_tag(
                row,
                HTMLTag.A,
                {HTMLAttr.CLASS: HTMLValue.PEP_REF}
            )
            pep_link = urljoin(PEP_URL, pep_a_tag[HTMLAttr.HREF])
            response = get_response(session, pep_link)
            if not response:
                continue

            abbr_tag = row.find_all(HTMLTag.ABBR)
            table_status = ('Active', 'Draft')
            if len(abbr_tag) == 1 and len(abbr_tag[0].text) == 2:
                table_status = EXPECTED_STATUS[abbr_tag[0].text[1]]

            soup = BeautifulSoup(response.text, features=FEATURE_LXML)
            dl = find_tag(soup, HTMLTag.DL, {HTMLAttr.CLASS: HTMLValue.RFC})
            page_status = find_tag(dl, HTMLTag.ABBR).text
            if page_status in table_status:
                if page_status in dict_status.keys():
                    dict_status[page_status] += 1
                else:
                    dict_status[page_status] = 1
            else:
                list_error_status.append((pep_link, page_status, table_status))

    log_error_status = ('{0}\n'
                        'Статус в карточке: {1}\n'
                        'Ожидаемые статусы: {2}\n')
    for error in list_error_status:
        logging.info(log_error_status.format(*error))

    results, total = [('Статус', 'Количество')], 0
    for pair in dict_status.items():
        results.append(pair)
        total += pair[1]
    results.append(('Total', total))

    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'pep_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)

    logging.info(f'Файл с результатами был сохранён: {file_path}')


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
