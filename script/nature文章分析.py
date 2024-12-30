import requests
from lxml import etree
import time
import csv

def get_affiliation(url, headers):
    """获取作者单位"""
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        
        affiliations = html.xpath('//*[@class="c-article-author-affiliation__address"]/text()')
        affiliations = [aff.strip() for aff in affiliations if aff.strip()]
        return '; '.join(affiliations)
    except Exception as e:
        print(f"获取作者单位时发生错误: {e}")
        return ""

def get_article_titles(base_url, page_num, csv_writer):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": base_url
        }
        
        response = requests.get(base_url, headers=headers)
        response.encoding = 'utf-8'
        
        html = etree.HTML(response.text)
        elements = html.xpath('//*[@class="app-article-list-row"]/li//a')
        elements2 = html.xpath('//*[@class="app-article-list-row"]/li//time/@datetime')
        elements3 = html.xpath('//*[@data-test="journal-title-and-link"]/text()') 
        
        print(f"\n--- 第 {page_num} 页 ---")
        for index, title in enumerate(elements, 1):
            full_text = ''.join(title.xpath('string()')).strip()
            href = 'https://www.nature.com' + title.xpath('@href')[0]
            article_date = elements2[index-1]
            journal = elements3[index-1]

            # 获取作者单位
            # print(f"正在获取第 {(page_num-1)*50 + index} 篇文章的作者单位...")
            # affiliation = get_affiliation(href, headers)
            
            # 写入CSV文件
            csv_writer.writerow([
                (page_num-1)*50 + index,
                full_text,
                href,
                article_date,
                journal
            ])
            
            print(f"{(page_num-1)*50 + index}. {full_text}")
            print(f"   链接: {href}")
            print(f"   日期: {article_date}")
            print(f"   期刊: {journal}\n")

            
        return len(elements)
        
    except Exception as e:
        print(f"获取第 {page_num} 页时发生错误: {e}")
        return 0

def main():
    # 打开CSV文件
    with open('nature_articles_2021.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['序号', '标题', '链接', '发布日期', '期刊'])

        for year in range(2021, 2022):
            print(f"\n正在获取第 {year} 年...")

            page = 1
            total_articles = 0
            
            while True:
                print(f"\n正在获取第 {page} 页...")
                
                # url = f'https://www.nature.com/search?order=date_desc&subject=hydrology&journal={journal}&article_type=research%2C+reviews&date_range=2024-2024&page={page}'
                url = f'https://www.nature.com/search?article_type=research%2C+reviews&subject=hydrology&order=date_desc&date_range={str(year)}-{str(year)}&page={page}'
                
                articles_count = get_article_titles(url, page, writer)
                total_articles += articles_count
                
                if articles_count < 50:
                    break
                    
                time.sleep(3)
                page += 1
        
        print(f"\n爬取完成！共获取 {total_articles} 篇文章")
        print(f"结果已保存到 nature_articles.csv")

if __name__ == "__main__":
    main()