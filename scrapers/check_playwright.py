from time import sleep

from playwright.sync_api import Playwright, sync_playwright
from playwright._impl._errors import TimeoutError


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://cmainfo.cma.gov.il/publicreports")
    page.get_by_role('button').nth(0).click()
    page.get_by_placeholder('תחום').nth(0).click()
    page.get_by_role('option', name='פנסיה').click()
    page.get_by_role('button').nth(1).click()
    page.get_by_role('combobox').nth(1).click()
    page.get_by_role('option').nth(3).click()
    page.get_by_role('combobox').nth(1).click()
    page.get_by_role('option').nth(4).click()
    page.get_by_role('combobox').nth(1).click()
    page.get_by_role('option').nth(5).click()
    page.get_by_role('combobox').nth(1).click()
    page.get_by_role('option').nth(6).click()
    page.get_by_role('combobox').nth(1).click()
    page.get_by_role('option').nth(7).click()
    page.get_by_role("button", name="Select").nth(1).click()
    page.get_by_role("option", name="2020").click()
    page.get_by_role('button', name='Select').nth(2).click()
    page.get_by_role("option", name="רבעון ראשון").click()
    page.get_by_role("button", name="Select").nth(3).click()
    page.get_by_role("option", name="2021").click()
    page.get_by_role("button", name="Select").nth(4).click()
    page.get_by_role("option", name="רבעון ראשון").click()
    sleep(15)
    page.get_by_role("button", name="חיפוש").click()
    sleep(5)
    page.locator('table tbody tr').all()
    row_count = page.locator('table tbody tr').count()
    position_errors = []
    for i in range(row_count):
        try:
            with page.expect_download() as download_info:
                page.locator("table tbody tr").nth(i).locator('td').nth(8).locator('img').click()
                report_type = page.locator("table tbody tr").nth(i).locator('td').nth(0).inner_text().strip()
                company_name = f'{page.locator("table tbody tr").nth(i).locator("td").nth(2).inner_text().strip()}'
                text = '-'.join([str(i), report_type, company_name])
                track_name = page.locator("table tbody tr").nth(i).locator('td').nth(4).inner_text().strip()
                if track_name:
                    text += f'-{track_name}'
                print(text)
            download = download_info.value
            download.save_as(f'../data/{i}.xlsx')
        except TimeoutError:
            position_errors.append(i)
            print(position_errors)
    for i in position_errors:
        try:
            with page.expect_download() as download_info:
                page.locator("table tbody tr").nth(i).locator('td').nth(8).locator('img').click()
                report_type = page.locator("table tbody tr").nth(i).locator('td').nth(0).inner_text().strip()
                company_name = f'{page.locator("table tbody tr").nth(i).locator("td").nth(2).inner_text().strip()}'
                text = '-'.join([str(i), report_type, company_name])
                track_name = page.locator("table tbody tr").nth(i).locator('td').nth(4).inner_text().strip()
                if track_name:
                    text += f'-{track_name}'
                print(text)
            download = download_info.value
            download.save_as(f'../data/{i}.xlsx')
        except TimeoutError as e:
            report_type = page.locator("table tbody tr").nth(i).locator('td').nth(0).inner_text().strip()
            company_name = f'{page.locator("table tbody tr").nth(i).locator("td").nth(2).inner_text().strip()}'
            track_name = page.locator("table tbody tr").nth(i).locator('td').nth(4).inner_text().strip()
            if track_name:
                text = '-'.join([str(i), report_type, company_name, track_name])
            else:
                text = '-'.join([str(i), report_type, company_name])
            print('Error with:')
            print(text)
        sleep(1)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
