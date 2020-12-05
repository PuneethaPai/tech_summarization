import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from src.generate_data import parse_web_page
from src.utils import read_csv


def parallelize(func, iterable, use_thread=True, *args, **kwargs):
    pool_executor = ThreadPoolExecutor if use_thread else ProcessPoolExecutor
    with pool_executor() as executor:
        data = list(executor.map(func, iterable))
    return data

if __name__ == "__main__":
    data = read_csv("data/summary/common.csv")
    urls = [row["doc_url"] for row in data if row["doc_url"]]
    selected_urls = urls[:100]
    
    start = time.time()
    norm_result = [parse_web_page(url) for url in selected_urls]
    done = time.time()
    print(f"Done, initial {start} -> {done} = {done - start}")
    
    start = done
    thread_result = parallelize(parse_web_page, selected_urls, use_thread=True)
    done = time.time()
    print(f"Done, Threading {start} -> {done} = {done - start}")
    
    # start = time.time()
    # parallelize(parse_web_page, selected_urls, use_thread=False)
    # # parallelize(print, selected_urls, use_thread=False)
    # done = time.time()
    # print(f"Done, Processing {start} -> {done} = {done - start}")
