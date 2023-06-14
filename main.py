import requests,csv,re,time
from tqdm import tqdm


# 发送HTTP GET请求获取网页内容
URL = "https://gaokao.chsi.com.cn"
YggkUrl= "https://gaokao.chsi.com.cn/zsgs/zhangcheng/listVerifedZszc--method-index,ssdm-,yxls-,xlcc-,zgsx-,yxjbz-,start-{}.dhtml"
headers = {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
csvFile = '阳光高考网高校招生简章.csv'

def PageGet(url,number):
    response = requests.get(headers=headers,url=url)
    # 检查响应状态码
    if response.status_code == 200:
        #匹配高校名称和主页链接
        schoolPattern = r' <a class="text-decoration-none name" target="_blank" href="(.*?)">\r\n(.*?)\r'
        schoolResult = re.findall(schoolPattern,response.text)
        #匹配高校招生简章链接
        zszcPattern = r'  <a class="zszc-link text-decoration-none" href="(.*?)" target="_blank"'
        zszcResult = re.findall(zszcPattern,response.text)
        #数据清洗整理
        cleanData = []
        for i in range(len(schoolResult)):
            data = [1 + i + number*100,                     #序号
                    re.sub(r"\s+","",schoolResult[i][1]),   #名称
                    URL+schoolResult[i][0],                 #介绍
                    URL+zszcResult[i]]                      #招生政策
            cleanData.append(data)
        print(cleanData[1])
        writeZszcUrl(cleanData)

    else:#报错显示码
        print("page get unsuccessfully,the status code is ", response.status_code)

def createZSZC():
    with open(csvFile, mode='w', newline='') as file:
        title = ["序号","名称","介绍","招生简章"]
        writer = csv.writer(file)
        writer.writerow(title)

def writeZszcUrl(data):
    with open(csvFile, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
def dealZszcUrl():
    with open(csvFile, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            zxzcUrl = row[3]
            schoolName = row[1]
            print(zxzcUrl,"    ",schoolName)
            # response = requests.get(headers=headers,url=zxzcUrl)
            # if response.status_code == 200:


if __name__ == "__main__":
    # pagesNumber = 2
    # progress_bar = tqdm(total=pagesNumber)
    # createZSZC()
    # for i in range(pagesNumber):
    #     pageUrl = YggkUrl.format(0+i*100)
    #     PageGet(pageUrl,i)
    #     time.sleep(1)
    #     progress_bar.update(1)
    # progress_bar.close()
    # print("获取高校链接任务已完成！")
    dealZszcUrl()