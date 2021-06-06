import os, pandas
import yfinance as yf
import time
import shutil
from os import system

def createdirectory():
    if not os.path.exists('datasets'):
        os.makedirs('datasets')

def yfinancedownload(csv_file_name):
        # yf.pdr_override()
        with open(csv_file_name) as f:
            lines = f.read().splitlines()
            for symbol in lines:
                # print(symbol)
                try:
                    data = yf.download(symbol,period = "ytd", interval = "1d", treads = True)
                    # data = yf.download(symbol, start=today.strftime("%m/%d/%y")-30, end=today.strftime("%m/%d/%y"), progress=True, treads = True)
                    # data = pdr.get_data_yahoo(symbol, period = "ytd", interval = "1d",progress=True, treads = True)
                    data.to_csv("datasets/{}.csv".format(symbol))
                except Exception:
                    pass
            

def squeezedetection(index_1,index_2):  
        
        dataframes = {}
        for filename in os.listdir('datasets'):
            #print(filename)
            symbol = filename.split(".")[0]

            #print(symbol)
            df = pandas.read_csv('datasets/{}'.format(filename))
            if df.empty: 
                continue
            
            df['20sma'] = df['Close'].rolling(window=20).mean()
            df['stddev'] = df['Close'].rolling(window=20).std()
            df['lower_band'] = df['20sma'] - (2 * df['stddev'])
            df['upper_band'] = df['20sma'] + (2 * df['stddev'])

            df['TR'] = abs(df['High'] - df['Low'])
            df['ATR'] = df['TR'].rolling(window=20).mean()

            df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
            df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

            def in_squeeze(df):
                return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

            df['squeeze_on'] = df.apply(in_squeeze, axis=1)

            try:
                    f = open("output.txt", "a")
                    if df.iloc[index_1]['squeeze_on'] and not df.iloc[index_2]['squeeze_on']:
                            print("{} is coming out the squeeze".format(symbol), file=f)
                            
                    f.close()
            except Exception:
                pass
           

        

def squeezed_3_days_detection(index_1,index_2):  
        
        dataframes = {}
        for filename in os.listdir('datasets'):
            #print(filename)
            symbol = filename.split(".")[0]

            #print(symbol)
            df = pandas.read_csv('datasets/{}'.format(filename))
            if df.empty: 
                continue
            
            df['20sma'] = df['Close'].rolling(window=20).mean()
            df['stddev'] = df['Close'].rolling(window=20).std()
            df['lower_band'] = df['20sma'] - (2 * df['stddev'])
            df['upper_band'] = df['20sma'] + (2 * df['stddev'])

            df['TR'] = abs(df['High'] - df['Low'])
            df['ATR'] = df['TR'].rolling(window=20).mean()

            df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
            df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

            def in_squeeze(df):
                return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

            df['squeeze_on'] = df.apply(in_squeeze, axis=1)

            try:
                    f = open("output.txt", "a")
                    if df.iloc[index_1]['squeeze_on'] and df.iloc[index_1 -1]['squeeze_on'] and df.iloc[index_1-2]['squeeze_on'] and not df.iloc[index_2]['squeeze_on']:
                            print("{} is coming out of 3day squeeze ".format(symbol), file=f)
                            
                    f.close()
            except Exception:
                pass
            
            dataframes[symbol] = df


        


def main():
    cls = lambda: system('cls')
    cls()
    createdirectory()
    
    f = open("output.txt", "a")
    print ("\nStart : %s" % time.ctime(), file=f)
    
    f.close()
    
    csv_selection = input ("Enter 1 for OL+S&P500 stocks,\n Enter 2 for 2000-Top-Companies,\n Enter 3 for NASDAQ\n Enter 4 for 1,2,3\n Or any key to skip downloading\n: ")
    if(csv_selection == '1'):
       f = open("output.txt", "a")
       print ("\nOL + S&P500\n " , file=f)
       f.close()
       yfinancedownload('OSL_plus_SP500.csv')
       
    elif(csv_selection == '2'):
       f = open("output.txt", "a")
       print ("\n2000-Top-Companies\n " , file=f)
       f.close() 
       yfinancedownload('2000.csv')
       
    elif(csv_selection == '3'):
       f = open("output.txt", "a")
       print ("\nNASDAQ\n " , file=f)
       f.close() 
       yfinancedownload('NASDAQ.csv')
       
    elif(csv_selection == '4'):
       f = open("output.txt", "a")
       print ("\nOL + S&P500 + 2000 Top Companies + NASDAQ\n " , file=f)
       f.close()  
       yfinancedownload('OSL_plus_SP500.csv')
       yfinancedownload('2000.csv')
       yfinancedownload('NASDAQ.csv')
    else:
       print ('Skipping Downloading')
    
    print ("Writing to output file started at %s" % time.ctime())   
    f = open("output.txt", "a")
    print ("===================================================================" , file=f)
    print ("Stocks which are in Squeeze Two Days before and coming out yesterday " , file=f)
    print ("===================================================================" , file=f)
    f.close()
    squeezedetection(-3,-1)
    
    f = open("output.txt", "a")
    print ("===================================================================" , file=f)
    print ("Stocks which are in Squeeze Day before and coming out yesterday " , file=f)
    print ("===================================================================" , file=f)
    f.close()
    
    squeezedetection(-2,-1)
    f = open("output.txt", "a")
    print ("==========================================================================================" , file=f) 
    print ("Stocks which are in Squeeze for last 3 days CONT. until Two Days before and coming out yesterday " , file=f)
    print ("==========================================================================================" , file=f)
    f.close()
    
    squeezed_3_days_detection(-3,-1)
    f = open("output.txt", "a")
    print ("==========================================================================================" , file=f)
    print ("Stocks which are in Squeeze for last 3 days CONT.  until day before and coming out yesterday " , file=f)
    print ("==========================================================================================" , file=f) 
    f.close()
    
    
    squeezed_3_days_detection(-2,-1) 
    f = open("output.txt", "a")
    print ("==========================================================================================" , file=f) 
    f.close()
    
    f = open("output.txt", "a")
    print ("End : %s" % time.ctime(), file=f)
    print ("Completed at %s \n" % time.ctime())
    f.close()
if __name__ == "__main__":
    main()