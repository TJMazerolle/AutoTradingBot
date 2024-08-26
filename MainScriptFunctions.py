from datetime import datetime
from AutoTradingFunctions import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def mainScript(signal_timeframe, username, password, method, output_actions = True, update_positions = True):

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
    account_value = getAccountValue(driver)

    # Get bid/ask prices
    bid_ask_prices = getBidAsk(driver)

    # Get Open Positions
    open_positions = getOpenPositions(driver)
    print(open_positions)

    if method == "investing.com":
        # Get Signals from investing.com
        signals = scrapeInvestingComSignals() # note that the function also saves the scrapped data

        # Get Actions to take on Open Positions
        actions = getActions(relevant_pairs, open_positions, signals, timeframe=signal_timeframe)
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
    
    if method == "foresignal.com":
        signals = scrapeForesignalComSignals()
        # signals.loc[2, "Signal"] = "Sell"
        # signals.loc[6, "Signal"] = "Buy"
        print(signals)
        print(open_positions)
        for i, pair in enumerate(signals["Pair"]):
            if signals["Signal"][i] == "Filled":
                continue
            if pair in open_positions["Pair"]:
                continue
            openPosition(driver, pair, signals["Signal"][i], 10000, bid_ask_prices,
                        take_profit = signals["TakeProfit"][i], stop_loss = signals["StopLoss"][i])

    driver.quit()
    
def DailyUpdate():
    while True:
        try:
            mainScript("Daily", "qfx_1933b", "i58re42", "investing.com", output_actions=False, update_positions = True)
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
            mainScript("Weekly", "qfx_efe05", "c57fj49", "investing.com", output_actions = False, update_positions = True)
            output_text = f"Completed Weekly Run at {datetime.now()}"
            print(output_text)
            print("=" * len(output_text))
            break
        except NoSuchElementException:
            print(f"NoSuchElementException at {datetime.now}. Restarting Script.")
        except TimeoutException:
            print(f"TimeoutException at {datetime.now}. Restarting Script.")

def MiscTests():
    mainScript("Daily", "qfx_f4b8e", "n52ym6", "investing.com", output_actions = True)