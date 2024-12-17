from concurrent.futures import ThreadPoolExecutor
from time import time

from tqdm.asyncio import tqdm_asyncio

import utils.constants as constants
from driver.setup import setup_driver
from driver.utils import search_submit
from requests_custom.utils import get_soup_requests, close_session
from updates.proxy import get_proxy, get_proxy_next
from utils.channel import (
    format_channel_name,
    get_results_from_soup,
    get_results_from_soup_requests,
)
from utils.config import config
from utils.retry import (
    retry_func,
    find_clickable_element_with_retry,
)
from utils.tools import (
    get_pbar_remaining,
    get_soup,
    format_url_with_cache,
    add_url_info,
    get_urls_from_file
)

if config.open_driver:
    try:
        from selenium.webdriver.common.by import By
    except:
        pass


async def get_channels_by_online_search(names, callback=None):
    """
    Get the channels by online search
    """
    channels = {}
    pageUrl = constants.foodie_url
    if not pageUrl:
        return channels
    proxy = None
    open_proxy = config.open_proxy
    open_driver = config.open_driver
    page_num = config.online_search_page_num
    if open_proxy:
        proxy = await get_proxy(pageUrl, best=True, with_test=True)
    start_time = time()
    online_search_name = constants.origin_map["online_search"]
    whitelist = get_urls_from_file(constants.whitelist_path)
    blacklist = get_urls_from_file(constants.blacklist_path)

    def process_channel_by_online_search(name):
        nonlocal proxy
        info_list = []
        driver = None
        try:
            if open_driver:
                driver = setup_driver(proxy)
                try:
                    retry_func(
                        lambda: driver.get(pageUrl), name=f"online search:{name}"
                    )
                except Exception as e:
                    if open_proxy:
                        proxy = get_proxy_next()
                    driver.close()
                    driver.quit()
                    driver = setup_driver(proxy)
                    driver.get(pageUrl)
                search_submit(driver, name)
            else:
                page_soup = None
                request_url = f"{pageUrl}?s={name}"
                try:
                    page_soup = retry_func(
                        lambda: get_soup_requests(request_url, proxy=proxy),
                        name=f"online search:{name}",
                    )
                except Exception as e:
                    if open_proxy:
                        proxy = get_proxy_next()
                    page_soup = get_soup_requests(request_url, proxy=proxy)
                if not page_soup:
                    print(f"{name}:Request fail.")
                    return
            retry_limit = 3
            for page in range(1, page_num + 1):
                retries = 0
                if not open_driver and page == 1:
                    retries = 2
                while retries < retry_limit:
                    try:
                        if page > 1:
                            if open_driver:
                                page_link = find_clickable_element_with_retry(
                                    driver,
                                    (
                                        By.XPATH,
                                        f'//a[contains(@href, "={page}") and contains(@href, "{name}")]',
                                    ),
                                )
                                if not page_link:
                                    break
                                driver.execute_script(
                                    "arguments[0].click();", page_link
                                )
                            else:
                                request_url = f"{pageUrl}?s={name}&page={page}"
                                page_soup = retry_func(
                                    lambda: get_soup_requests(request_url, proxy=proxy),
                                    name=f"online search:{name}, page:{page}",
                                )
                        soup = (
                            get_soup(driver.page_source) if open_driver else page_soup
                        )
                        if soup:
                            if "About 0 results" in soup.text:
                                retries += 1
                                continue
                            results = (
                                get_results_from_soup(soup, name)
                                if open_driver
                                else get_results_from_soup_requests(soup, name)
                            )
                            print(name, "page:", page, "results num:", len(results))
                            if len(results) == 0:
                                print(
                                    f"{name}:No results found, refreshing page and retrying..."
                                )
                                if open_driver:
                                    driver.refresh()
                                retries += 1
                                continue
                            elif len(results) <= 3:
                                if open_driver:
                                    next_page_link = find_clickable_element_with_retry(
                                        driver,
                                        (
                                            By.XPATH,
                                            f'//a[contains(@href, "={page + 1}") and contains(@href, "{name}")]',
                                        ),
                                        retries=1,
                                    )
                                    if next_page_link:
                                        if open_proxy:
                                            proxy = get_proxy_next()
                                        driver.close()
                                        driver.quit()
                                        driver = setup_driver(proxy)
                                        search_submit(driver, name)
                                retries += 1
                                continue
                            for result in results:
                                url, date, resolution = result
                                if url:
                                    url = add_url_info(url, online_search_name)
                                    url = format_url_with_cache(url)
                                    info_list.append((url, date, resolution))
                            break
                        else:
                            print(
                                f"{name}:No page soup found, refreshing page and retrying..."
                            )
                            if open_driver:
                                driver.refresh()
                            retries += 1
                            continue
                    except Exception as e:
                        print(f"{name}:Error on page {page}: {e}")
                        break
                if retries == retry_limit:
                    print(f"{name}:Reached retry limit, moving to next page")
        except Exception as e:
            print(f"{name}:Error on search: {e}")
            pass
        finally:
            if driver:
                driver.close()
                driver.quit()
            pbar.update()
            if callback:
                callback(
                    f"正在进行线上查询, 剩余{names_len - pbar.n}个频道待查询, 预计剩余时间: {get_pbar_remaining(n=pbar.n, total=pbar.total, start_time=start_time)}",
                    int((pbar.n / names_len) * 100),
                )
            return {"name": format_channel_name(name), "data": info_list}

    names_len = len(names)
    pbar = tqdm_asyncio(total=names_len, desc="Online search")
    if callback:
        callback(f"正在进行线上查询, 共{names_len}个频道", 0)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(process_channel_by_online_search, name) for name in names
        ]
        for future in futures:
            result = future.result()
            name = result.get("name")
            data = result.get("data", [])
            if name:
                channels[name] = data
    if not open_driver:
        close_session()
    pbar.close()
    return channels
