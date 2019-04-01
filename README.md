# securityMonitor

### 环境

基于Python3.6+，由于其中Seebug爬虫调用Pyppeteer库对Python环境有要求，故要求Python3.6+

### 结构

利用 Flask 写的简单Web展示，前端使用了部分layui的样式等。考虑到Flask在用装饰器定义路径时比较方便，如果使用Django或者Tornado显得更有条理一些。

Web 展示和爬虫部分是分开的。Spider模块里是一些爬虫的脚本，将爬虫得到的数据存储到Mongo，然后Web展示则是从Mongo里面读取数据。

### 界面

简单的界面如下：

![](https://ws3.sinaimg.cn/large/006tKfTcly1g1nfxvawrij31mi0u07av.jpg)

爬虫目前抓取了这几个数据源，后期可根据需要进行维护，添加自定义抓取的数据源。

![](https://ws1.sinaimg.cn/large/006tKfTcly1g1ng04b7mjj31mj0u0dpp.jpg)

数据展示分了两个 Tab，按照时间顺序分今日和历史存储的数据进行展示，另外配合搜索框进行检索。

### 爬虫

其实爬虫的数据是沿用了之前的一些，这里做了一些修改进行数据存储然后Web展示而已。

Seebug 涉及到一些反爬，在搜索一些前人经验时，发现利用execjs执行整个js代码块时随着反爬升级总是会出现一些问题。于是想起去年先知白帽大会猪猪侠讲的Web 2.0启发式爬虫，其实有用到Pyppeteer这个库。其实这是node.js的Puppeteer库对Python的支持，使用这种方法暂时不会被反爬拦截，但是这个库要求Python3.6+。

另外WeChat的爬虫是调用了搜狗微信的接口，但是也会遇到一些反爬的拦截，在前面的文章中补充了绕过反爬的方法，调用打码平台解封Ip，生产Cookie。还有暗网的爬虫会涉敏，就不公布了。

更多可参考博客poochi.cn

