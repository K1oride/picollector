# picollector
The picollector projects aims to build a smart web spider that could crawl pictures from user-specified site and related sites(generated by Google search the keywords).

# Dependencies
-Python version 2.7
-requests
-beautifulsoup4
-pymysql

# Future developments
1. replace beautifulsoup by lxml(xpath) to better suit pages of various structures;
2. replace MySQL by MongoDB to better suit sites with different sturctures;
3. keep crawling rules in MySQL database. Connect with SQLalchemy ORM instead of Core;
4. complete the finding relative sites with Google search part;
5. a module that analysises the structure of sites;
6. rewrite the exsisting parts with scrapy, boosting crawling efficiency by using multithread and error handling features of the framework;
7. provide some features against anti-spider rules used in some sites.

# Looking for cooperation...
