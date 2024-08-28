# AutoTradingBot

NOTE: Due to the constantly changing nature of a platform like Questrade, the xpaths of the current implementation might be out of date, so this script will not work until they are updated.

This script is set up so that using Selenium with a FireFox web driver, the script can log in to a Questrade account and execute trades based on a set of trade signals that are determined.  In the future, the intention is to have a seperate prediction script set up to predict the movements of currency pairs and have this script execute the trades automatically.  However for now, we are just scrapping the signals from https://ca.investing.com/currencies/streaming-forex-rates-majors.

TradingScript.ipynb is set up so that this script can be run continuously every n hours or days depending on what the user needs.  In this interval the script will pull/derive new signals and update the Questrade portfilio accordingly.

The script will save the results of the signals and the results of the executed actions.  Right now I have the folders in .gitignore so that my results do not take up space, but the script will save the results for the user.

Lastly, note that when scrapping signals from investing.com, we use a specialized FireFox profile.  This profile has uBlock Origin installed, and it is only used to clean out the ads that sometimes get in the way of the functionallity of the scrapper.