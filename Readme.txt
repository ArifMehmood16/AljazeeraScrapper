1. Install Python 3.7 (select option while installation 'add to path')
2. Install Pycharm IDE (select option while installation 'add to path'). The reason to use this ide is that i use IntellijIdea for java dev. They are similar(from same vendor jetbrains)

3. Extract the .zip file.
4. Open the 'AljazeeraScrapper' project directory in pycharm ide.

5. Run in pyrcharm terminal to create virtual env 'scrapperenv':(cd into 'AljazeeraScrapper') python -m venv scrapperenv
6. Run in pyrcharm terminal  to active virtual env: scrapperenv\Scripts\activate.bat

7. configure virtual env for project in pychram ide:
   -got to File->setting->project:[name]->Python Interpreter->Project Interpreter Setting(Button on right)->virtual env->Existing Env-> (select path to activate.bat in virtual env scripts directory)

8. Run following commands in terminal to install required libraries:
	-pip install numpy
	-pip install matplotlib
	-pip install pandas
	-pip install selenium
	-pip install bs4

9. Download 'chromedriver'. the version should be equal to the version of chrome brower installed on system.
	- Chrome Browser Version 83.x.xxx.xx need chromedriver version 83.x.x.x.x 83.0.4103.39
	- Example: Chrome Browser Version 83.0.4103.61 need chromedriver version 83.0.4103.39

10. place the download chromedriver.exe in the project directory 'AljazeeraScrapper'.

11. To start the data collection run the following command: python datacollection.py (Takes 1.5 hours for 500+ articles)
12. To start the data analysis run the following command: python dataanalysis.py

13. data collection is configureable. there are total 5 configurations in datacollection.py. They at the top of the datacollection.py file
	- limit_pages - int - It limits the no of pages to scrap articles urls.
	- limit_articles - int - It limits the no of articles to scrap data.
	- create_menu_list - boolean - It is used to toggle between reading the main site page to scrap all the option in drop down menu to click eg, Africa, Middle East, Sports, etc. 
	- create_url_list - boolean - It is used to toggle between reading the pages to collect url of articles
	- extract_data -boolean - It is used to toggle between reading the articles to collect data
		
	*These configurations are designed to do the task in multiple run or in single run.
	*Setting limit will not extract exact data, but it will extract max data upto the limit configured.
	*Setting limit_page=100 and limit_article=1000 and all the booleans true, will fetch data in single run.
	*This can be done in steps also, by setting single config to true in 3 iteration, and changing the boolean in iterations(limit_page=100, limit_articles=1000)
		Iteration 1: create_menu_list=True	create_url_list=False		create_url_list=False  (Collects menu urls)
		Iteration 2: create_menu_list=False	create_url_list=True		create_url_list=False  (Collects articles urls)
		Iteration 3: create_menu_list=False	create_url_list=False		create_url_list=True	(Extracts data from articles)

14. The results of datacollection.py are in 3 csv files. 'output/menu_url.csv', 'output/articles.csv', 'output/articles_data.csv'

15. data analysis is configureable. there are total 2 configurations in dataanalysis.py. They are at the top of dataanalysis.py file.
	- confidence_level - float - The value of confidence to get the tags in relevance.
	- no_of_tags_to_find_condifence - 5 - the no of tags to get with highest frequency.

16. The results of datacollection.py are in png files. 'output/plots/*'. The file with max_frequency is 'output/plots/max_frequency_tags.png'. The files with confidence plot is saved with the name of parent/main tags.

17. log of both datacollection and dataanalysis are logged in collection_error.log and analysis_error.log respectively.