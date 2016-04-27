import requests,re,html
import codecs

from lxml import etree

listing_url='http://m.58.com/sh/yewu/'
listing_url='http://m.58.com/sh/yewu/'
famouscompanyid='http://qy.58.com/mq/'
# unfamouscompanyid=
headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1','From': 'http://m.58.com/sh' }


tag=re.compile(r'.*<div\s*class\s*=\s*"myf"\s*>(.*)</div>.*')
tagsplit=re.compile(r'<.*?>')
spacere=re.compile(r'\s*')
urlre=re.compile(r'.*58supin\.com.*')
adidre=re.compile(r'.*/(.*)\.shtml.*')
companyidre=re.compile(r'.*detail/(.*)/')
companyphonere=re.compile(r'.*>(\d+\-*\d+\-*\d+)<.*')
companymailre=re.compile(r'.*>([0-9a-zA-Z\_]*@[0-9a-zA-Z\_]*\.[0-9a-zA-Z\_]*)<.*')
companywebaddre=re.compile(r'.*>(http.*?)<')
famouscompanyre=re.compile(r'.*名企.*')

liboxxpath="//ul[@class='list-info job']/li"
liboxxpath="//div[@id='infolist']/dl"
liboxxpath="//ul[@class='infoList']/li"
nextxpath="//a[@class='pagenext']/@href"
titlexpath="//span[@id='d_title']/text()"
payxpath="//div[@class='price']/span[@class='pay']/text()"
timexpath=["//div[@class='status_bar']/span[@class='date']/text()","//div[@class='pub_date']/span[2]/text()"]
viewcountxpath="//span[@id='totalcount']/text()"
jobpositionxpath="//section[@class='job_con']/ul/li[1]/span[@class='attrValue']/a/text()"
jobneedxpath="//section[@class='job_con']/ul/li[@class='req']/span[@class='attrValue']/text()"
joblocationxpath="//span[@class='attrValue dizhiValue']/a[1]/text()"
jobfulixpath="//div[@class='fulivalue attrValue']/span/text()"
companynamexpath="//div[@class='com']//h2[contains(@class,'c_tit')]/a/text()"
companyaxpath="//div[@class='com']//h2[contains(@class,'c_tit')]/a/@href"
phonexpath="//a[@id='contact_phone']/@phoneno"
contactxpath="//div[@class='com']//div[@class='contact']/span[2]/text()"
jobdisxpath="//div[@class='position_dis']/div[@class='dis_con']/p/text()"

companytitlexpath="//div[@class='titArea']/h2/text()"
companyisrenxpath="//div[@class='compAdd']/span[@class='busLic']"
companytypexpath="//div[@class='detArea']/dl[@class='compMsg']/dd[1]/text()"
companymodxpath="//div[@class='detArea']/dl[@class='compMsg']/dd[2]/text()"
companyhangxpath="//div[@class='detArea']/dl[@class='compMsg']/dd[3]/a/text()"
companyaddxpath="//div[@class='detArea']/dl[@class='compMsg']/dd[4]/text()"
companyintroxpath="//div[@class='compSum']/div[@class='txtArea']/p/span/text()"
companycontactxpath="//div[@class='addB compTouch']/dl"


def buildxpath(htmltext,givenxpath,ismutil):
    page = etree.HTML(htmltext)
    if isinstance(givenxpath,list):
        for x in givenxpath:
            content=page.xpath(x)
            if len(content) != 0:
                if ismutil:
                    return "，".join(content)
                else:
                    return content[0]
    else:
        content=page.xpath(givenxpath)
        if len(content) != 0:
            if ismutil:
                return "，".join(content)
            else:
                return content[0]
    return None

def parsercompanyweb(companytext,company,adf,companyf):
    try:
        companycontact=(str(etree.tostring(buildxpath(companytext,companycontactxpath,0)))or '').replace('\\n','').replace('\\t','')
    except TypeError:
        companycontact=''
    company['phone']=''
    company['mail']=''
    company['webadd']=''
    if companyphonere.match(companycontact):
        company['phone']=companyphonere.match(companycontact).group(1)
    if companymailre.match(companycontact):
        company['mail']=companymailre.match(companycontact).group(1)
    if companywebaddre.match(companycontact):
        company['webadd']=companywebaddre.match(companycontact).group(1)
    company['title']=buildxpath(companytext,companytitlexpath,0)
    if buildxpath(companytext,companyisrenxpath,0) !=None:
        company['isrenzheng']=1
    else:
        company['isrenzheng']=0
    company['type']=buildxpath(companytext,companytypexpath,0).strip()
    company['mod']=buildxpath(companytext,companymodxpath,0)
    company['hang']=buildxpath(companytext,companyhangxpath,0)
    company['add']=buildxpath(companytext,companyaddxpath,0)
    company['intro']=(buildxpath(companytext,companyintroxpath,1) or '').replace(',...,','').replace(',','，').strip().replace('\r','')
    companyf.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format( company['id'],company['url'],company['title'],
    company['isfamous'],company['isrenzheng'],company['type'],company['mod'],company['hang'],
    company['add'],company['intro'],company['phone'],company['mail'],company['webadd']))
    # print(company['isfamous'])
    # print(company['url'])


def parservad(vadtext,ad,adf,companyf):
    ad['title']=buildxpath(vadtext,titlexpath,0)
    ad['pay']=buildxpath(vadtext,payxpath,0)
    ad['time']=buildxpath(vadtext,timexpath,0)
    ad['viewcount']=buildxpath(vadtext,viewcountxpath,0)
    ad['jobposition']=buildxpath(vadtext,jobpositionxpath,0)
    ad['jobneed']=buildxpath(vadtext,jobneedxpath,0)
    ad['joblocation']=buildxpath(vadtext,joblocationxpath,0)
    ad['jobfuli']=buildxpath(vadtext,jobfulixpath,1)
    ad['jobcompany']=buildxpath(vadtext,companynamexpath,0)
    ad['phone']=buildxpath(vadtext,phonexpath,0)
    ad['contact']=buildxpath(vadtext,contactxpath,0)
    ad['jobdis']=buildxpath(vadtext,jobdisxpath,0).replace(',','，').strip().replace('\r','')
    # print(ad['url'])
    adf.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(ad['id'],ad['url'],ad['city'],ad['category'],ad['title'],
    ad['tag'], ad['pay'], ad['time'],ad['viewcount'],ad['jobposition'],
    ad['jobneed'],ad['joblocation'],ad['jobfuli'],ad['jobcompany'],
    ad['jobdis'],ad['phone'], ad['contact']))
    company=dict()
    if famouscompanyre.match(ad['tag']):
        company['isfamous']=1
    else:
        company['isfamous']=0
    companyr=requests.get(buildxpath(vadtext,companyaxpath,0))
    company['url']=companyr.url
    company['id']=companyidre.match(company['url']).group(1) or ''
    parsercompanyweb(companyr.text,company,adf,companyf)

def parserlisting(htmlstr,adf,companyf,count):
    page = etree.HTML(htmlstr)
    liboxs = page.xpath(liboxxpath)
    for libox in liboxs:
        # ad=dict()
        litree=etree.tostring(libox)
        # tags=re.split(tagsplit,tag.match(str(litree)).group(1))
        # for x in tags:
        #     if spacere.match(x):
        #       tags.remove(x)
        # ad['tag']=html.unescape('，'.join(tags).replace(' ',''))
        # ad['city']='sh'
        # ad['category']='yewu'
        vadbox=etree.HTML(litree)
        print(litree)
        # vadurl=etree.tostring(vadbox.xpath("//div[@class='title']/a/@href")[0])
        ad_url= vadbox.xpath("//div[@class='item-right']/a/@href")[0]
        ad_title= vadbox.xpath("//div[@class='item-right']//dt/strong/text()")[0]
        #company_url = vadbox.xpath("//dd/a[contains(@class,'fl')]/@href")[0]
        company_name = vadbox.xpath("//div[@class='item-right']//dd[@class='info-desc']/em[2]/text()")
        if len(company_name) == 0:
            company_name = ['unknown']
        company_name=company_name[0]
        type = vadbox.xpath("//div[@class='item-last']/span")
        if len(type) == 0:
            type = ['unknown']
        elif len(type) == 1:
            type = ['unknown']
            service = vadbox.xpath("//div[@class='item-last']/span/text()")
        else:
            type = vadbox.xpath("//div[@class='item-last']/span[1]/text()")
            service = vadbox.xpath("//div[@class='item-last']/span[2]/text()")
        type = type[0]
        #area = vadbox.xpath("//dd[@class='w96']/text()")
        #service = vadbox.xpath("//div[@class='item-last']/span[2]/text()")
        if len(service) == 0:
            #service = vadbox.xpath("//dd[@class='w68']/text()")
            service = ['unknown']
        service =service[0].strip()
        s = '{},{},{},{}\n'.format( ad_title,company_name, type, service)#ad_url, ad_title, company_url, company_name,{},{},{},{},
        print(s)
        adf.write(s)
        continue
        vadr=requests.get(vadurl)
        vadtext=vadr.text
        ad['url']=vadr.url
        if not urlre.match(vadr.url):
            ad['id']=adidre.match(vadr.url).group(1)
            try:
                parservad(vadtext,ad,adf,companyf)
            except Exception:
                continue
    while count<100:
        count=count+1
        try:
            nexturl=page.xpath(nextxpath)[0].split('?')[0]
        except Exception:
            print('ohh')
            exit()
        #htmltext=requests.get('http://m.58.com'+nexturl).text
        htmltext=requests.get('http://sh.58.com'+nexturl,headers=headers).text
        print('http://m.58.com'+nexturl)
        parserlisting(htmltext,adf,companyf,count)



count=1
htmltext=requests.get(listing_url, headers=headers).text
with codecs.open('adc.txt','w',"utf-8")as adf:
    with open('company.txt','w',errors='ignore')as companyf:
        #adf.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('id','url','城市','类目',
        #                                                                  '标题','标签','薪酬','发布时间','查看次数','职位','要求',
        #                                                                  '地点','福利','公司名','工作描述','电话','联系人'))
        #companyf.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('id','url','标题','是否名企','是否认证',
        #                                                                 '类型','规模','行业','地址','介绍','电话',
        #                                                                  '邮件','网址'))
        parserlisting(htmltext,adf,companyf,count)
