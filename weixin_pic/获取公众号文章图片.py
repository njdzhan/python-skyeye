from re import findall
from urllib.request import urlopen
import os
 
url = 'https://mp.weixin.qq.com/s/VFSVPFpp0agTdaM_nbm07Q'
image_path = '/root/test/Wechatimg'
os.chdir(image_path)
 
# bytes->str：decode 解码
with urlopen(url) as fp:
    content = fp.read().decode()   # 需要进行解码成字符串
    print(content)              # 得到的是默认的utf-8格式字符串
 
pattern = 'data-w="570" data-src="(.+?)"'
result = findall(pattern, content)
#print(result)                      # 得到的是一个列表
 
for index, item in enumerate(result,1):
    data = urlopen(str(item)).read()
    print('开始下载第' + str(index) +'张图片：'+ str(item))
    f = open(str(index) + '.jpg', "wb")
    f.write(data)
