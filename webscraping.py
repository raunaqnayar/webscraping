# pip install requests --> Needed to grab html files
# pip install beautifulsoup4 --> Needed for scraping web data
'''
This code parses through the the html document of the Hacker News website https://news.ycombinator.com/
Data scraping is used to filter news items.

This code uses print_news() function-
The print_news function takes the following parameters into account-
scan_pages --> number of pages to scan in the Hacker News website
min_upvotes --> minimum number of upvotes a post should recieve to get printed on the terminal
min_comments --> minimum number of comments a post should recieve to get printed on the terminal
desc_comments (default value = False) --> If this is set to True news articles will be printed in decresing order of comments, 
                    if it is False they get printed in decresing order of upvotes. 
print_news(scan_pages,min_upvotes,min_comments,desc_comments=False)

'''
import requests
from bs4 import BeautifulSoup;

def filter_news(scraped_data,min_upvotes,min_comments):
    '''
        Internal function called by print_news() function for fitering operation
        Used to filter a single page in Hacker News website
        Returns a list of filtered posts. Each item of the list contains information of individual post in dictionary format.
        (The returned value is a list of dictionary items embedded in it, which is used by print_news() function for further processing )
        filter_news(scraped_data,min_upvotes,min_comments):
        Arguments Passed-
        scraped_data --> BeautifulSoup instance containing HTML parsed data corresponding to a specific Hacker News Webpage
        min_upvotes --> minimum number of upvotes a post should recieve (filter constraint)
        min_comments --> minimum number of comments a post should recieve (filter constraint)



    '''
    ## BeautifulSoup select methods. 
    # instance.select(.<item>) # selects all class='item' attributes
    # .select(#<item>) # selects all id='item' attributes

    #topic_list=scraped_data.find_all('tr', class_='athing')                        # alternative 2
    story_list=scraped_data.select('.storylink')                                    # alternative 1
    #score_list=scraped_data.find_all('td', class_='subtext')                       # alternative 2
    score_list=scraped_data.select('.subtext')                                        # alternative 1

    hack_news=[]
#<a href="item?id=27265074">77&nbsp;comments</a>
    for i in range(len(story_list)):
        if(score_list[i].select('.score') ) and ('comments' in score_list[i].select('a[href^="item?id="]')[1].contents[0]):
            scores=int(score_list[i].select('.score')[0].contents[0].split(" ")[0])
            comments=int(score_list[i].select('a[href^="item?id="]')[1].contents[0].split("comment")[0]);
            if(scores>=min_upvotes and comments>min_comments):
                hack_news.append({'topic':story_list[i].contents[0],'link':story_list[i]['href'],'votes':scores,'comments':comments})

    
    return(hack_news)

def print_news(pages,min_upvotes,min_comments, desc_comments=False):
    '''
    print_news(scan_pages,min_upvotes,min_comments,desc_comments=False)
    scan_pages --> number of pages to scan in the Hacker News website
    min_upvotes --> minimum number of upvotes a post should recieve to get printed on the terminal
    min_comments --> minimum number of comments a post should recieve to get printed on the terminal
    desc_comments (default value = False) --> 
    If this is set to True news articles will be printed in decresing order of comments, 
    If it is False they get printed in decresing order of upvotes. 

    '''
    news_list =[];
    for i in range(pages):
        if i==0:
            scraped_data=BeautifulSoup(requests.get('https://news.ycombinator.com/').text,'html.parser')
        else:
            scraped_data=BeautifulSoup(requests.get(f'https://news.ycombinator.com/news?p={i+1}').text,'html.parser')

        news_list+=filter_news(scraped_data,min_upvotes,min_comments)

    print(f"List of topics with more than {min_upvotes} points and more than {min_comments} comments:\t")

    if(desc_comments):
        news_list_desc=sorted(news_list, key = lambda k:k['comments'] , reverse=True )
    else:
        news_list_desc=sorted(news_list, key = lambda k:k['votes'] , reverse=True )


    for result in news_list_desc:
        print()
        for k,v in result.items():
            print(f"{k.capitalize()}:\t{v}");

if __name__=='__main__':
    scan_pages=10     
    min_upvotes=600    
    min_comments=300
    desc_comments=False


    print_news(scan_pages,min_upvotes,min_comments,desc_comments)