Hi, I present you my signal bot to buy used tires in Minsk.

The project consists of 2 scrapers (scripers/av_scraper and scripers/bamper_scraper, which correspond to the sites av.by and bamper.by) and stores information in storage/ folder and 1 bot that sends to telegrams new proposals of used tires according to my parameters to telegram.

Main file is bot.py which collects data from storage/av_ and sorage/bamper_ and sends it to me through telegram.

Description of the problem: 
As a rule, really profitable offers are sold within 10-20 minutes after publication. The bot allows you to refuse constant monitoring and evaluation of proposals.
The program searches for new proposals every minute (comparing id) and sends all the necessary characteristics in a convenient form in a message
