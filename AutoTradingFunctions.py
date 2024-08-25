import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def questradeLogIn(questradeDriver, username = "qfx_f3cee", password = "m58jf9"):
    input_username = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.ID, "field_userid")))
    input_password = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.ID, "field_password")))
    login_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='LOG IN ']")))
    input_username.send_keys(username)
    input_password.send_keys(password)
    login_button.click()
    time.sleep(15) # let the page load

def toggleOpenPositionsWindow(questradeDriver, action):
    if action.lower() == "open":
        toggle_open_pos_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[3]/div/section/div[1]/button")))
    if action.lower() == "close":
        toggle_open_pos_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/section/div[1]/button")))
    toggle_open_pos_button.click()
    
def toggleInstrumentsWindow(questradeDriver):
    # toggle_instrument_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/section/div[1]/button")))
    toggle_instrument_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/section/nav/button")))
    toggle_instrument_button.click()

def getAccountValue(questradeDriver):
    while True:
        try:
            account_value_xpath = "/html/body/div[1]/div[2]/footer/div/div/div[4]/span[2]"
            account_value = questradeDriver.find_element(by=By.XPATH, value=account_value_xpath)
            account_value = float(account_value.text.replace(',', ''))
            return account_value
        except:
            time.sleep(5)

def getOpenPositions(questradeDriver):
    symbols = []
    positions = []
    profits = []

    toggleOpenPositionsWindow(questradeDriver, "open")

    open_position_table = questradeDriver.find_elements(by=By.CLASS_NAME, value="focusmanager--no-outline")[2]
    rows = open_position_table.find_elements(by=By.CLASS_NAME, value="draggable")
    for i, row in enumerate(rows):
        if i < len(rows) - 1:
            symbol_xpath = (f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/section/div[2]/div/' + 
                            f'div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/' +
                            f'div[{i+2}]/div/div[2]/div/div/div/div[2]/div/div/div')
            symbols.append(row.find_element(by=By.XPATH, value=symbol_xpath).text[:7])
        else:
            symbols.append("")
        # symbols.append(row.find_element(by=By.CLASS_NAME, value="instrument__name").text)
        positions.append(row.find_element(by=By.CLASS_NAME, value="tst-col-item-ls").get_attribute("title"))
        profits.append(row.find_element(by=By.CLASS_NAME, value="v5RPy_directional-number").text)

    open_positions = pd.DataFrame({
        "Pair": symbols,
        "Position": positions,
        "Profit": profits
    })

    toggleOpenPositionsWindow(questradeDriver, "close")
    return open_positions.drop(open_positions.index[-1])

def scrapeForesignalComSignals():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://foresignal.com/en/")
    pairs = []
    signals = []
    take_profits = []
    stop_losses = []
    try:
        close_warning = driver.find_element(by=By.CLASS_NAME, value="btn-close")
        close_warning.click()
    except:
        pass
    cards = driver.find_elements(by=By.CLASS_NAME, value="card")
    for i in range(len(cards)):
        row = i // 3 + 1
        col = i % 3 + 1
        # Pairs
        pair = driver.find_element(by=By.XPATH, value=f'/html/body/div/div[{row}]/div[{col}]/div[1]/div/div[2]/a')
        pairs.append(pair.text.replace('/', ''))
        # Signals
        signal = driver.find_element(by=By.XPATH, value=f'/html/body/div/div[{row}]/div[{col}]/div[2]/div[4]')
        signals.append(signal.text)
        # Take Profits
        tp = driver.find_element(by=By.XPATH, value=f'/html/body/div/div[{row}]/div[{col}]/div[2]/div[5]/div[2]')
        take_profits.append(float(tp.text))
        # Stop Losses
        sl = driver.find_element(by=By.XPATH, value=f'/html/body/div/div[{row}]/div[{col}]/div[2]/div[6]/div[2]')
        stop_losses.append(float(sl.text))
    signal_table = pd.DataFrame({
        "Pair": pairs,
        "Signal": signals,
        "TakeProfit": take_profits,
        "StopLoss": stop_losses
    })
    driver.quit()
    return signal_table

def scrapeInvestingComSignals():
    while True:
        try:
            # url_path = "https://ca.investing.com/currencies/streaming-forex-rates-majors"
            # driverInvestingCom = webdriver.Firefox()
            # driverInvestingCom.maximize_window()
            # driverInvestingCom.get(url_path)
            extension = "C:/Users/tjmaz/AppData/Roaming/Mozilla/Firefox/Profiles/uo4io7dr.SeleniumProfile"
            firefox_profile = webdriver.FirefoxProfile(extension)
            options = webdriver.FirefoxOptions()
            options.profile = firefox_profile
            driverInvestingCom = webdriver.Firefox(options=options)
            driverInvestingCom.maximize_window()
            driverInvestingCom.get("https://ca.investing.com/currencies/streaming-forex-rates-majors")
            time.sleep(5)
            button = WebDriverWait(driverInvestingCom, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Technical']")))
            button.click()
            pair = []
            hourly = []
            daily = []
            weekly = []
            monthly = []
            rows = driverInvestingCom.find_elements(by=By.CLASS_NAME, value="datatable-v2_row__hkEus")
            skipped_first_row = False
            for row in rows:
                if skipped_first_row:
                    contents = row.find_elements(by=By.CSS_SELECTOR, value="td")
                    hourly.append(contents[2].text)
                    daily.append(contents[3].text)
                    weekly.append(contents[4].text)
                    monthly.append(contents[5].text)
                    currency = contents[1].find_element(by=By.CSS_SELECTOR, value="a")
                    pair.append(currency.get_attribute("title").replace("/", ""))
                else:
                    skipped_first_row = True
            driverInvestingCom.quit()
            signals = pd.DataFrame({
                "Pair": pair,
                "Hourly": hourly,
                "Daily": daily,
                "Weekly": weekly,
                "Monthly": monthly
            })
            signals.to_csv("G:/My Drive/University of Waterloo Files/Applied Machine Learning and Artificial Intelligence/Projects/AutoTradingBot/.gitignore/FXStreetSignals/Signals " 
                        + str(datetime.now())[:19].replace(":", "-") + ".csv", index = False)
            return signals
        except:
            driverInvestingCom.quit()
            print("5 Minute Timer Reached: Rerunning scrapeInvestingComSignals()")

def loadInvestingComSignals():
    file_path = "G:/My Drive/University of Waterloo Files/Applied Machine Learning and Artificial Intelligence/Projects/AutoTradingBot/.gitignore/FXStreetSignals"
    latest_signals = os.listdir(file_path)[-1]
    return pd.read_csv(file_path + "/" + latest_signals)

def getActions(relevant_pairs, open_positions, signals, timeframe = "Daily"):
    actual_open_positions = open_positions.copy()
    actual_open_positions = actual_open_positions[actual_open_positions["Position"] != "Square"] 
    strong_positions = ["Strong Buy", "Strong Sell"]
    relevant_signals = signals[["Pair", timeframe]]
    relevant_signals = relevant_signals[relevant_signals[timeframe].isin(strong_positions)]
    relevant_signals = relevant_signals[relevant_signals["Pair"].isin(relevant_pairs)].reset_index(drop=True)
    position_signals = pd.merge(actual_open_positions[["Pair", "Position"]], relevant_signals, how = "outer")
    action = []
    for i in range(position_signals.shape[0]):
        if str(position_signals[timeframe][i]) == "nan":
            action.append("Close")
        elif str(position_signals["Position"][i]) == "nan": #or position_signals["Position"][i] == "Square":
            if position_signals[timeframe][i] == "Strong Buy":
                action.append("Open Long")
            else:
                action.append("Open Short")
        elif position_signals["Position"][i] == "Long" and position_signals[timeframe][i] == "Strong Sell":
            action.append("Reverse to Short")
        elif position_signals["Position"][i] == "Short" and position_signals[timeframe][i] == "Strong Buy":
            action.append("Reverse to Long")
        else:
            action.append("Hold")
    position_signals["Action"] = action
    position_signals.to_csv("G:/My Drive/University of Waterloo Files/Applied Machine Learning and Artificial Intelligence/Projects/AutoTradingBot/.gitignore/ExecutedTrades/" 
                            + timeframe + "Actions At" + str(datetime.now())[:19].replace(":", "-") + ".csv", index = False)
    return position_signals

def calculateQuantity(pair, desired_exposure, bid_ask_table):
    numerator = pair[:3]
    if numerator == "CAD":
        return max(1000.0, float(desired_exposure))
    if numerator == "AUD":
        index = bid_ask_table[bid_ask_table['Pair'] == "AUDCAD"].index.item()
        price = bid_ask_table["Ask"][index]
        return max(1000.0,desired_exposure / float(price))
    if numerator == "CHF":
        index = bid_ask_table[bid_ask_table['Pair'] == "CADCHF"].index.item()
        price = bid_ask_table["Ask"][index]
        return max(1000.0,desired_exposure * float(price))
    if numerator == "EUR":
        index = bid_ask_table[bid_ask_table['Pair'] == "EURCAD"].index.item()
        price = bid_ask_table["Ask"][index]
        return max(1000.0,desired_exposure / float(price))
    if numerator == "GBP":
        index = bid_ask_table[bid_ask_table['Pair'] == "GBPCAD"].index.item()
        price = bid_ask_table["Ask"][index]
        return max(1000.0,desired_exposure / float(price))
    if numerator == "NZD":
        index = bid_ask_table[bid_ask_table['Pair'] == "NZDCAD"].index.item()
        price = bid_ask_table["Ask"][index]
        return max(1000.0,desired_exposure / float(price))
    if numerator == "USD":
        index = bid_ask_table[bid_ask_table['Pair'] == "USDCAD"].index.item()
        price = bid_ask_table["Ask"][index]
        return max(1000.0,desired_exposure / float(price))

def closePosition(questradeDriver, symbol_to_close, pos_of_symbol_to_close):
    toggleOpenPositionsWindow(questradeDriver, "open")
    open_position_table = questradeDriver.find_elements(by=By.CLASS_NAME, value="focusmanager--no-outline")[2]
    rows = open_position_table.find_elements(by=By.CLASS_NAME, value="draggable")
    for i, row in enumerate(rows):
        symbol_xpath = (f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/section/div[2]/' + 
                        f'div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div/' + 
                        f'div/div/div[{i+2}]/div/div[2]/div/div/div/div[2]/div/div/div')
        row_symbol = row.find_element(by=By.XPATH, value=symbol_xpath).text
        if row_symbol == symbol_to_close:
            button_xpath = (f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/section/div[2]' + 
                            f'/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div' + 
                            f'/div/div/div[{i+2}]/div/div[18]/div/div/button')
            close_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            close_button.click()
            if pos_of_symbol_to_close == "Long":
                close_pos_button_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[1]/" +
                                          "div/div[4]/div/div[4]/div/div[1]/div[1]/div[1]/div[1]/div/div")
                close_pos_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, close_pos_button_xpath)))
                close_pos_button.click()
                time.sleep(1)
                close_pos_button.click()
            else:
                close_pos_button_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[1]/" +
                                          "div/div[4]/div/div[4]/div/div[1]/div[1]/div[1]/div[3]/div/div")
                close_pos_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, close_pos_button_xpath)))
                close_pos_button.click()
                time.sleep(1)
                close_pos_button.click()
            confirm_button_xpath = "/html/body/div[4]/div/div/div/div[2]/div[2]/div/button"
            confirm_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
            confirm_button.click()
            break
    toggleOpenPositionsWindow(questradeDriver, "close")

def openPosition(questradeDriver, symbol_to_open, action, amount, bid_ask_prices,
                 take_profit = None, stop_loss = None):
    toggleInstrumentsWindow(questradeDriver)
    if take_profit is None and stop_loss is None:
        instrument_table = questradeDriver.find_elements(by=By.CLASS_NAME, value="focusmanager--no-outline")[0]
        rows = instrument_table.find_elements(by=By.CLASS_NAME, value="draggable")
        for i, row in enumerate(rows):
            symbol_xpath = (f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/section/div[2]' +
                            f'/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/' +
                            f'div[{i+1}]/div/div[1]/div/div/div/div[2]/div/div/div')
            row_symbol = row.find_element(by=By.XPATH, value=symbol_xpath).text
            quantity = calculateQuantity(row_symbol, amount, bid_ask_prices)
            if row_symbol == symbol_to_open:
                open_pos_button_xpath = (f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]' +
                                         f'/section/div[2]/div/div/div[3]/div/div/div/div[2]/div/div[2]' +
                                         f'/div/div/div/div/div/div/div/div[{i+1}]/div/div[3]/button')
                open_pos_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, open_pos_button_xpath)))
                open_pos_button.click()
                try:
                    close_muw_button_xpath = (f'/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div' +
                                              f'/div[2]/div/div/div/div[1]/div/div/div[4]/button')
                    close_muw_button = WebDriverWait(questradeDriver, 3).until(EC.element_to_be_clickable((By.XPATH, close_muw_button_xpath)))
                    close_muw_button.click()
                except:
                    pass
                imput_amount_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[2]/div" +
                                      "/div/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div/div[2]/input")
                input_amount = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.XPATH, imput_amount_xpath)))
                time.sleep(1)
                input_amount.send_keys(str(quantity))
                time.sleep(2)
                if action == "Open Long" or action == "Buy":
                    open_long_button_xpath = ('/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div' +
                                              '/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div[1]' +
                                              '/div[1]/div[1]/div[3]/div/div')
                    open_long_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, open_long_button_xpath)))
                    open_long_button.click()
                    time.sleep(1)
                    open_long_button.click()
                if action == "Open Short" or action == "Sell":
                    open_short_button_xpath = ('/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div' +
                                               '/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div/div[1]' +
                                               '/div[1]/div[1]/div[1]/div/div')
                    open_short_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, open_short_button_xpath)))
                    open_short_button.click()
                    time.sleep(1)
                    open_short_button.click()
                    # time.sleep(9999)
                close_trade_window_xpath = "/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[1]/header/button"
                confirm_button_xpath = "/html/body/div[5]/div/div/div/div[2]/div[2]/div/button"
                close_trade_window = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, close_trade_window_xpath)))
                confirm_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
                confirm_button.click()
                time.sleep(1)
                close_trade_window.click()
                time.sleep(1)
                break
    else:
        instrument_table = questradeDriver.find_elements(by=By.CLASS_NAME, value="focusmanager--no-outline")[0]
        rows = instrument_table.find_elements(by=By.CLASS_NAME, value="draggable")
        for i, row in enumerate(rows):
            symbol_xpath = (f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/section/div[2]' +
                            f'/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/' +
                            f'div[{i+1}]/div/div[1]/div/div/div/div[2]/div/div/div')
            row_symbol = row.find_element(by=By.XPATH, value=symbol_xpath).text
            quantity = calculateQuantity(row_symbol, amount, bid_ask_prices)
            if row_symbol == symbol_to_open:
                open_pos_button_xpath = (f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]' +
                                         f'/section/div[2]/div/div/div[3]/div/div/div/div[2]/div/div[2]' +
                                         f'/div/div/div/div/div/div/div/div[{i+1}]/div/div[3]/button')
                open_pos_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, open_pos_button_xpath)))
                open_pos_button.click()
                time.sleep(1)
                next_trade_option_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[2]/div/div/div" +
                                           "/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div/div[3]/div")
                next_trade_option = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.XPATH, next_trade_option_xpath)))
                next_trade_option.click()
                time.sleep(1)
                input_amount_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[2]/div/div" +
                                      "/div/div[2]/div[2]/div/div[4]/div/div[1]/div[2]/div/div[2]/input")
                input_amount = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.XPATH, input_amount_xpath)))
                time.sleep(1)
                input_amount.send_keys(str(quantity))
                time.sleep(1)
                tp_sl_window_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[2]/div/div" + 
                                      "/div/div[2]/div[2]/div/div[6]/div/div/div/div/div/div[2]/div/span")
                tp_sl_window = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.XPATH, tp_sl_window_xpath)))
                tp_sl_window.click()
                input_tp_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[2]/div/div/div/div[2]" + 
                                  "/div[2]/div/div[6]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[2]/input")
                input_tp = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.XPATH, input_tp_xpath)))
                time.sleep(1)
                input_tp.send_keys(str(take_profit))
                time.sleep(1)
                input_sl_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[2]/div/div/div/div[2]" +
                                  "/div[2]/div/div[6]/div/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[2]/input")
                input_sl = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.XPATH, input_sl_xpath)))
                time.sleep(1)
                input_sl.send_keys(str(stop_loss))
                time.sleep(1)
                if action == "Sell":
                    switch_to_sell_xpath = ("/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[2]/div/div" +
                                            "/div/div[2]/div[2]/div/div[3]/div/div[1]/div[2]/div/div[3]/div")
                    switch_to_sell = WebDriverWait(questradeDriver, 60).until(EC.presence_of_element_located((By.XPATH, switch_to_sell_xpath)))
                    switch_to_sell.click()
                close_trade_window_xpath = "/html/body/div[4]/div[2]/div[1]/span/div/div/div[2]/div/div[1]/header/button"
                confirm_button_xpath = "/html/body/div[5]/div/div/div/div[2]/div[2]/div/button"
                close_trade_window = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, close_trade_window_xpath)))
                confirm_button = WebDriverWait(questradeDriver, 60).until(EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
                confirm_button.click()
                time.sleep(1)
                close_trade_window.click()
                time.sleep(1)
    toggleInstrumentsWindow(questradeDriver)

def updatePositions(questradeDriver, close_positions, open_long_positions, open_short_positions, 
                    reverse_to_long_positions, reverse_to_short_positions, bid_ask_prices, amount,
                    take_profit = None, stop_loss = None):
    # Close Positions
    for i in range(close_positions.shape[0]):
        # if close_positions["Position"][i] == "Square":
        #     continue
        closePosition(questradeDriver, close_positions["Pair"][i], close_positions["Position"][i])
        time.sleep(1)
    # Open Long Positions
    for i in range(open_long_positions.shape[0]):
        openPosition(questradeDriver, open_long_positions["Pair"][i], open_long_positions["Action"][i], 
                     amount, bid_ask_prices, take_profit, stop_loss)
        time.sleep(1)
    # Open Short Positions
    for i in range(open_short_positions.shape[0]):
        openPosition(questradeDriver, open_short_positions["Pair"][i], open_short_positions["Action"][i], 
                     amount, bid_ask_prices, take_profit, stop_loss)
        time.sleep(1)
    # Reverse to Long Positions
    for i in range(reverse_to_long_positions.shape[0]):
        closePosition(questradeDriver, reverse_to_long_positions["Pair"][i], reverse_to_long_positions["Position"][i])
        openPosition(questradeDriver, reverse_to_long_positions["Pair"][i], "Open Long", 
                     amount, bid_ask_prices, take_profit, stop_loss)
        time.sleep(1)
    # Reverse to Short Positions
    for i in range(reverse_to_short_positions.shape[0]):
        closePosition(questradeDriver, reverse_to_short_positions["Pair"][i], reverse_to_short_positions["Position"][i])
        openPosition(questradeDriver, reverse_to_short_positions["Pair"][i], "Open Short", 
                     amount, bid_ask_prices, take_profit, stop_loss)
        time.sleep(1)
    
def getBidAsk(questradeDriver):
    toggleInstrumentsWindow(questradeDriver)
    time.sleep(5)
    pair = []
    bid = []
    ask = []
    instrument_table = questradeDriver.find_elements(by=By.CLASS_NAME, value="focusmanager--no-outline")[0]
    rows = instrument_table.find_elements(by=By.CLASS_NAME, value="draggable")
    for i, row in enumerate(rows):
        symbol_xpath = (f'/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/section/div/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div[{i+1}]/div/div[1]/div/div/div/div[2]/div/div/div')
        bid_xpath = (f'/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/section/div/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div[{i+1}]/div/div[2]/button/div/div[2]/p/span')
        ask_xpath = (f'/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/section/div/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div[{i+1}]/div/div[3]/button/div/div[2]/p/span')
        pair.append(row.find_element(by=By.XPATH, value=symbol_xpath).text)
        bid.append(row.find_element(by=By.XPATH, value=bid_xpath).text)
        ask.append(row.find_element(by=By.XPATH, value=ask_xpath).text)
    bid_ask_prices = pd.DataFrame({
        "Pair": pair,
        "Bid": bid,
        "Ask": ask
        })
    toggleInstrumentsWindow(questradeDriver)
    return bid_ask_prices