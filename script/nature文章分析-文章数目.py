import requests
from lxml import etree
import time
import csv
from datetime import datetime

def get_search_results(url, journal, year, headers):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        html = etree.HTML(response.text)
        
        # 获取结果数量
        results = html.xpath('//*[@data-test="results-data"]/span[2]/text()')
        result_count = results[0] if results else "0"
        
        return result_count
            
    except Exception as e:
        print(f"获取搜索结果时发生错误: {e}")
        return "0"

def main():
    # 期刊列表
    journals = [
        'natsustain',  # Nature Sustainability
        'natrevearthenviron', # Nature Reviews Earth & Environment
        'nclimate',    # Nature Climate Change
        'ngeo',        # Nature Geoscience
        'commsenv',     # Communications Earth & Environment
        'natwater',    # Nature Water
        'ncomms',      # Nature Communications
        'srep',        # Scientific Reports
        'sdata',        # Scientific Data
        'npjcleanwater', # npj Clean Water
        'nature',       # Nature
        'npjclimatsci' # npj Climate and Atmospheric Science
    ]
    
    # 年份范围
    years = range(2010, 2025)  # 2010到2024
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    
    # 创建CSV文件
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'nature_journals_statistics_{current_time}.csv'
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['期刊', '年份', '文章数量'])
        
        # 遍历每个期刊和年份
        for journal in journals:
            print(f"\n处理期刊: {journal}")
            
            for year in years:
                print(f"处理年份: {year}")
                
                # 构建URL
                url = f'https://www.nature.com/search?order=date_desc&journal={journal}&article_type=research%2C+reviews&date_range={year}-{year}&page=1'
                
                # 获取结果数量
                result_count = get_search_results(url, journal, year, headers)

                if result_count == '0':
                    break
                
                # 写入CSV
                writer.writerow([journal, year, result_count.replace(' results', '')])
                
                print(f"文章数量: {result_count}")
                
                # 添加延时，避免请求过快
                time.sleep(2)
    
    print(f"\n统计完成！结果已保存到 {filename}")

if __name__ == "__main__":
    main()