# stock_news_warning_messenger_python

This is a small script that takes a ".csv" file of the stocks you wish to follow and if the stock prices changes more than +-5% on the day, it sends a SMS warning message to your phone using the Twillio SMS messenging API. Furthermore, the script uses the Newsapi API to include the top 3 most popular news articles briefs associated with the stock of interest in addition to the stock percentage movement warning. The attached article brief includes the title, description and url. 

The script can be scheduled to run once per day on cloud based python servers to provided constant stock updates. 

For more on Newsapi:
https://newsapi.org

For more on Twillio:
https://www.twilio.com


![IMG_0446](https://user-images.githubusercontent.com/76194492/180065589-dd215ef6-888d-4391-aa07-5e0e4e39d10b.PNG)
Figure 1 : Sample text message
