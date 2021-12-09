Hi, I present my signal bot to buy used tires in Minsk.

The project consists of 2 scrapers (scrapers/av_scraper.py and scrapers/bamper_scraper.py, which correspond to the sites av.by and bamper.by) and stores information in storage/ folder and 1 bot that sends to telegrams new proposals of used tires according to my parameters to telegram.

Main file is bot.py which collects data from storages/av_storage.json and sorage/bamper_storage.json and sends it to me through telegram.

Description of the problem: 
As a rule, really profitable offers are sold within 10-20 minutes after publication. Thфt bot allows me to refuse constant monitoring and evaluation of proposals.
The program searches for new proposals every minute (comparing id) and sends all the necessary characteristics in a convenient form in a message

