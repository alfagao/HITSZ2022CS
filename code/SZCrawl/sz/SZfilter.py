
# 返回当前页面仅含 文章列表href 的soup对象
def soup_filter_page(soup):
    return soup.find(class_="zx_ml_list")

# 寻找下一页的url, 找不到则为None
def soup_filter_next(soup):
    next_soup = soup.find(class_="next")
    if next_soup is not None:
        return next_soup['href']
    return None

# 从soup中提取data并返回
# 包括: publicDate(str), passageTitle(str), passageContent(list of str)
def get_title(soup):
    return soup.find(class_="tit").find("h1").text

def get_date(soup):
    return soup.find("h6").find_all("span")[1].text[7:17]

def get_content(soup):
    text_soup_all = soup.find(class_="news_cont_d_wrap").find_all('p')
    return [val.text.strip() for val in text_soup_all]

def page_content_fill(soup):
    title = get_title(soup)
    date = get_date(soup)
    content = get_content(soup)
    return {
        "publicDate": date,
        "passageTitle": title,
        "passageContent": content
    }
