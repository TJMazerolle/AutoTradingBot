from datetime import datetime
from AutoTradingFunctions import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def mainScript(signal_timeframe, username, password, output_actions = True, update_positions = True):

    # print("Current time:", datetime.now())

    relevant_pairs = ["AUDCAD","AUDCHF","AUDJPY","AUDNZD","AUDUSD","CADCHF","CADJPY",
                      "CHFJPY","EURAUD","EURCAD","EURCHF","EURGBP","EURJPY","EURNZD",
                      "EURUSD","GBPAUD","GBPCAD","GBPCHF","GBPJPY","GBPNZD","GBPUSD",
                      "NZDCAD","NZDCHF","NZDJPY","NZDUSD","USDCAD","USDCHF","USDJPY"]

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.questradefxglobal.com/sim/d/trading/open-positions")

    # Log into Questrade
    questradeLogIn(driver, username=username, password=password)

    # Get account value
    try:
        account_value = getAccountValue(driver)
        print(f"Account Value: ${account_value}")
    except:
        print("Script Failed at getAccountValue()")

    # Get bid/ask prices
    try:
        bid_ask_prices = getBidAsk(driver)
        print("Got Bid/Ask Prices")
    except:
        print("Script Failed at getBidAsk()")

    # Get Open Positions
    try:
        open_positions = getOpenPositions(driver)
        print("Got Open Positions")
    except:
        print("Script Failed at getOpenPositions()")

    # Get Signals from investing.com
    try:
        signals = scrapeInvestingComSignals() # note that the function also saves the scrapped data
        print("Scrapped Signals From investing.com")
    except:
        print("Script Failed at scrapeInvestingComSignals()")

    # Get Actions to take on Open Positions
    try:
        actions = getActions(relevant_pairs, open_positions, signals, timeframe=signal_timeframe)
        print("Got Actions to Execute")
    except:
        print("Script Failed at getActions()")
    close_positions = actions[actions["Action"] == "Close"].reset_index(drop=True)
    open_long_positions = actions[actions["Action"] == "Open Long"].reset_index(drop=True)
    open_short_positions = actions[actions["Action"] == "Open Short"].reset_index(drop=True)
    reverse_to_long_positions = actions[actions["Action"] == "Reverse to Long"].reset_index(drop=True)
    reverse_to_short_positions = actions[actions["Action"] == "Reverse to Short"].reset_index(drop=True)

    # Display Actions about to be Taken
    if output_actions:
        print("Close Positions:")
        display(close_positions)
        print("\nOpen Long Positions:")
        display(open_long_positions)
        print("\nOpen Short Positions:")
        display(open_short_positions)
        print("\nReverse to Long Positions:")
        display(reverse_to_long_positions)
        print("\nReverse to Short Positions:")
        display(reverse_to_short_positions)

    if update_positions:
        updatePositions(driver, close_positions, open_long_positions, open_short_positions, 
                        reverse_to_long_positions, reverse_to_short_positions, bid_ask_prices, account_value / 2)

    driver.quit()
    
def DailyUpdate():
    while True:
        try:
            mainScript("Daily", "qfx_454ff", "c63js87", output_actions=False, update_positions = True)
            output_text = f"Completed Daily Run at {datetime.now()}"
            print(output_text)
            print("=" * len(output_text))
            break
        except NoSuchElementException:
            print(f"NoSuchElementException at {datetime.now}. Restarting Script.")
        except TimeoutException:
            print(f"TimeoutException at {datetime.now}. Restarting Script.")

def WeeklyUpdate():
    current_time = datetime.now().strftime("%H:%M")
    while True:
        try:
            mainScript("Weekly", "qfx_efe05", "c57fj49", output_actions = False, update_positions = True)
            output_text = f"Completed Weekly Run at {datetime.now()}"
            print(output_text)
            print("=" * len(output_text))
            break
        except NoSuchElementException:
            print(f"NoSuchElementException at {datetime.now}. Restarting Script.")
        except TimeoutException:
            print(f"TimeoutException at {datetime.now}. Restarting Script.")

def MiscTests():
    mainScript("Daily", "qfx_f4b8e", "n52ym6", output_actions = True)