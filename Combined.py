import os, pandas
import yfinance as yf
import time,datetime
import shutil
from os import system
import os.path
from pandas_datareader import data as pdr


if not os.path.exists('results'):
        os.makedirs('results')
save_path = 'results/'
filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
completeName = os.path.join(save_path, filename1+".txt")

def createdirectory():
    shutil.rmtree('datasets')
    os.makedirs('datasets')
    

def yfinancedownload(csv_file_name):
        yf.pdr_override()
        with open(csv_file_name) as f:
            lines = f.read().splitlines()
            for symbol in lines:
                # print(1symbol)
                try:
                    
                    data = pdr.get_data_yahoo(symbol, start=pandas.to_datetime('2020-07-15'), end=pandas.to_datetime(datetime.datetime.today() + datetime.timedelta(days=1)), progress=True, treads = True)
                    #To enable test data, adjust the end time
                    # data = pdr.get_data_yahoo(symbol, start=pandas.to_datetime('2020-07-15'), end=pandas.to_datetime('2021-04-06'), progress=True, treads = True)
                    
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
            
            df['8dayEWM']  = df['Close'].ewm(span=8 , adjust=False).mean()
            df['21dayEWM'] = df['Close'].ewm(span=21, adjust=False).mean()
            df['34dayEWM'] = df['Close'].ewm(span=34, adjust=False).mean()
            df['55dayEWM'] = df['Close'].ewm(span=55, adjust=False).mean()
            df['89dayEWM'] = df['Close'].ewm(span=89, adjust=False).mean()
            
            def above_21ema(df):
                return df['Close']> df['21dayEWM']
            
            df['above_21ema_on'] = df.apply(above_21ema, axis=1)
            
            def in_stacked(df):
                return df['Close']> df['8dayEWM'] and df['Close']> df['21dayEWM'] and df['Close']> df['34dayEWM'] and df['Close']> df['55dayEWM'] and df['Close']> df['89dayEWM']
            
            df['stacked_on'] = df.apply(in_stacked, axis=1)
            
            def in_squeeze(df):
                return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

            df['squeeze_on'] = df.apply(in_squeeze, axis=1)

            try:
                    f = open(completeName, "a")
                    if df.iloc[index_1]['squeeze_on'] and not df.iloc[index_2]['squeeze_on']:
                            # print("{} is coming out the squeeze".format(symbol), file=f)
                            print("{0} is coming out of 3day squeeze. \nStacked Postively = {1}, 21EWM = {2}\n".format(symbol,df.iloc[index_2]['stacked_on'],df.iloc[index_2]['above_21ema_on'] ), file=f)
                            print("{0} is coming out of 3day squeeze. \nStacked Postively = {1}, 21EWM = {2}\n".format(symbol,df.iloc[index_2]['stacked_on'],df.iloc[index_2]['above_21ema_on'] ))
                            
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
            
            df['8dayEWM']  = df['Close'].ewm(span=8 , adjust=False).mean()
            df['21dayEWM'] = df['Close'].ewm(span=21, adjust=False).mean()
            df['34dayEWM'] = df['Close'].ewm(span=34, adjust=False).mean()
            df['55dayEWM'] = df['Close'].ewm(span=55, adjust=False).mean()
            df['89dayEWM'] = df['Close'].ewm(span=89, adjust=False).mean()
            
            def above_21ema(df):
                return df['Close']> df['21dayEWM']
            
            df['above_21ema_on'] = df.apply(above_21ema, axis=1)
            
            def in_stacked(df):
                return df['Close']> df['8dayEWM'] and df['Close']> df['21dayEWM'] and df['Close']> df['34dayEWM'] and df['Close']> df['55dayEWM'] and df['Close']> df['89dayEWM']
            
            df['stacked_on'] = df.apply(in_stacked, axis=1)
            
            def in_squeeze(df):
                return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

            df['squeeze_on'] = df.apply(in_squeeze, axis=1)

            try:
                    f = open(completeName, "a")
                    if df.iloc[index_1]['squeeze_on'] and df.iloc[index_1 -1]['squeeze_on'] and df.iloc[index_1-2]['squeeze_on'] and not df.iloc[index_2]['squeeze_on']:
                            print("{0} is coming out of 3day squeeze. \nStacked Postively = {1}, 21dayEWM = {2}\n".format(symbol,df.iloc[index_2]['stacked_on'],df.iloc[index_2]['above_21ema_on'] ), file=f)
                            print("{0} is coming out of 3day squeeze. \nStacked Postively = {1}, 21EWM = {2}\n".format(symbol,df.iloc[index_2]['stacked_on'],df.iloc[index_2]['above_21ema_on'] ))
                            
                    f.close()
            except Exception:
                pass
            
            dataframes[symbol] = df


        


def main():
    cls = lambda: system('cls')
    cls()
    createdirectory()
    
    
    f = open(completeName, "a")
    print ("*******************************************************************" , file=f)
    print ("\nStart : %s" % time.ctime(), file=f)
    
    f.close()
    
    csv_selection = input ("Enter 1 for OLstocks,\nEnter 2 for 2000-Top-Companies,\nEnter 3 for NASDAQ\nEnter 4 for SP500\nEnter 5 for 2,3,4 Data \nEnter 6 for Test\n Or any key to skip downloading\n: ")
    if(csv_selection == '1'):
       f = open(completeName, "a")
       print ("Data : OL \n" , file=f)
       f.close()
       yfinancedownload('OSL.csv')
       
    elif(csv_selection == '2'):
       f = open(completeName, "a")
       print ("Data :2000-Top-Companies\n " , file=f)
       f.close() 
       yfinancedownload('2000.csv')
       
    elif(csv_selection == '3'):
       f = open(completeName, "a")
       print ("Data :NASDAQ\n " , file=f)
       f.close() 
       yfinancedownload('NASDAQ.csv')
       
    elif(csv_selection == '4'):
       f = open(completeName, "a")
       print ("Data :SP500\n " , file=f)
       f.close() 
       yfinancedownload('SP500.csv')
       
    elif(csv_selection == '5'):
       f = open(completeName, "a")
       print ("Data : S&P500 + 2000 Top Companies + NASDAQ\n " , file=f)
       f.close()  
       yfinancedownload('SP500.csv')
       yfinancedownload('2000.csv')
       yfinancedownload('NASDAQ.csv')
    elif(csv_selection == '6'):
       f = open(completeName, "a")
       print ("Data :Test\n " , file=f)
       f.close() 
       yfinancedownload('Test.csv')
    
    else:
       print ('Skipping Downloading')
    
    print ("Writing to output file started at %s" % time.ctime())   
    f = open(completeName, "a")
    
    print ("===================================================================" , file=f)
    print ("Stocks which are in Squeeze Two Days before and coming out yesterday " , file=f)
    print ("===================================================================" , file=f)
    print ("===================================================================" )
    print ("Stocks which are in Squeeze Two Days before and coming out yesterday " )
    print ("===================================================================" )
    f.close()
    squeezedetection(-3,-1)
    
    f = open(completeName, "a")
    print ("===================================================================" , file=f)
    print ("Stocks which are in Squeeze Day before and coming out yesterday " , file=f)
    print ("===================================================================" , file=f)
    print ("===================================================================" )
    print ("Stocks which are in Squeeze Day before and coming out yesterday " )
    print ("===================================================================" )
    f.close()
    
    squeezedetection(-2,-1)
    f = open(completeName, "a")
    print ("==========================================================================================" , file=f) 
    print ("Stocks which are in Squeeze for last 3 days CONT. until Two Days before and coming out yesterday " , file=f)
    print ("==========================================================================================" , file=f)
    print ("==========================================================================================") 
    print ("Stocks which are in Squeeze for last 3 days CONT. until Two Days before and coming out yesterday ")
    print ("==========================================================================================" )
    f.close()
    
    squeezed_3_days_detection(-3,-1)
    f = open(completeName, "a")
    print ("==========================================================================================" , file=f)
    print ("Stocks which are in Squeeze for last 3 days CONT.  until day before and coming out yesterday " , file=f)
    print ("==========================================================================================" , file=f) 
    print ("==========================================================================================" )
    print ("Stocks which are in Squeeze for last 3 days CONT.  until day before and coming out yesterday ")
    print ("==========================================================================================" ) 
    f.close()
    
    
    squeezed_3_days_detection(-2,-1) 
    f = open(completeName, "a")
    print ("==========================================================================================" , file=f) 
    f.close()
    
    f = open(completeName, "a")
    print ("End : %s" % time.ctime(), file=f)
    print ("Completed at %s \n" % time.ctime())
    print ("*******************************************************************" , file=f)
    f.close()
if __name__ == "__main__":
    main()