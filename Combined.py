import os, pandas
import yfinance as yf
import time,datetime
import shutil
from os import system
import os.path
from pandas_datareader import data as pdr


if not os.path.exists('results'):
        os.makedirs('results')
        
if not os.path.exists('exit_results'):
        os.makedirs('exit_results')

if not os.path.exists('datasets'):
        os.makedirs('datasets')
        
save_path = 'results/'
filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
completeName = os.path.join(save_path, filename1+".txt")

save_exit_path = 'exit_results/'
filename_exit = datetime.datetime.now().strftime("%Y%m%d")
completeName_exit = os.path.join(save_exit_path, filename_exit+".txt")

def createdirectory():
    shutil.rmtree('datasets')
    os.makedirs('datasets')
    
 
    

def yfinancedownload(csv_file_name, interval_time):
        yf.pdr_override()
        with open(csv_file_name) as f:
            lines = f.read().splitlines()
            for symbol in lines:
                # print(1symbol)
                try:
                    if(csv_file_name == 'Test.csv'):
                        data = pdr.get_data_yahoo(symbol, start=pandas.to_datetime('2020-07-15'), end=pandas.to_datetime('2021-04-06'),interval = interval_time, progress=True, treads = True)
                    else:
                        data = pdr.get_data_yahoo(symbol, start=pandas.to_datetime('2020-07-15'), end=pandas.to_datetime(datetime.datetime.today() + datetime.timedelta(days=1)), interval = interval_time, progress=True, treads = True)
                     
                    
                    data.to_csv("datasets/{}.csv".format(symbol))
                except Exception:
                    pass
            

def squeezedetection(index_1,index_2,days):  
        
        dataframes = {}
        for filename in os.listdir('datasets'):
            
            symbol = filename.split(".")[0]

           
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
            df['13dayEWM'] = df['Close'].ewm(span=13, adjust=False).mean()
            df['21dayEWM'] = df['Close'].ewm(span=21, adjust=False).mean()
            df['34dayEWM'] = df['Close'].ewm(span=34, adjust=False).mean()
            df['55dayEWM'] = df['Close'].ewm(span=55, adjust=False).mean()
            df['89dayEWM'] = df['Close'].ewm(span=89, adjust=False).mean()
            
            def above_21ema(df):
                return df['Close']> df['21dayEWM']
            
            df['above_21ema_on'] = df.apply(above_21ema, axis=1)
            
            def in_stacked(df):
                # return df['Close']> df['8dayEWM'] and df['Close']> df['21dayEWM'] and df['Close']> df['34dayEWM'] and df['Close']> df['55dayEWM'] and df['Close']> df['89dayEWM']
                return df['Close']> df['8dayEWM'] > df['13dayEWM'] and df['13dayEWM'] > df['21dayEWM'] and df['21dayEWM'] > df['34dayEWM'] and df['34dayEWM'] > df['55dayEWM'] and df['55dayEWM'] > df['89dayEWM']
            
            df['stacked_on'] = df.apply(in_stacked, axis=1)
            
            def in_squeeze(df):
                return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

            df['squeeze_on'] = df.apply(in_squeeze, axis=1)

            #Calculating True Streaks
            df['start_of_squeeze'] = df['squeeze_on'].ne(df['squeeze_on'].shift())
            df['squeeze_id']=df['start_of_squeeze'].cumsum()
            df['squeeze_counter']=df.groupby('squeeze_id').cumcount()+1
            
            
           
                
            if(days == 1):    
                try:
                    f = open(completeName, "a")
                    # if df.iloc[index_1]['squeeze_on'] and df.iloc[index_1]['stacked_on'] and df.iloc[index_1]['above_21ema_on'] and not df.iloc[index_2]['squeeze_on'] :
                    if df.iloc[index_1]['squeeze_on'] and not df.iloc[index_2]['squeeze_on'] :
                            print("{0} is coming out of squeeze. \nStacked Postively = {1}, 21dayEWM = {2} , Sq. days = {3}, Volume = {4}\n".format(symbol,df.iloc[index_2]['stacked_on'],df.iloc[index_2]['above_21ema_on'],df.iloc[index_1]['squeeze_counter'],df.iloc[index_2]['Volume'] ), file=f)
                            print("{0} is coming out of squeeze. \nStacked Postively = {1}, 21EWM = {2}, Sq. days = {3}, Volume = {4}\n".format(symbol,df.iloc[index_2]['stacked_on'],df.iloc[index_2]['above_21ema_on'],df.iloc[index_1]['squeeze_counter'],df.iloc[index_2]['Volume'] ))
                            
                    f.close()
                except Exception:
                    pass    
            
            

            else:
                print ('Skipping!!!')
           
            dataframes[symbol] = df
        

def exittrade():
    dataframes = {}
    f = open(completeName_exit, "a")
    print ("*******************************************************************" , file=f)
    print ("\nStart : %s" % time.ctime(), file=f)
    f.close()
    for filename in os.listdir('datasets'):
            
            symbol = filename.split(".")[0]

           
            df = pandas.read_csv('datasets/{}'.format(filename))
            if df.empty: 
                continue
            
            df['8dayEWM']  = df['Close'].ewm(span=8 , adjust=False).mean()
            df['13dayEWM'] = df['Close'].ewm(span=13, adjust=False).mean()
            df['21dayEWM'] = df['Close'].ewm(span=21, adjust=False).mean()
            df['34dayEWM'] = df['Close'].ewm(span=34, adjust=False).mean()
            df['55dayEWM'] = df['Close'].ewm(span=55, adjust=False).mean()
            df['89dayEWM'] = df['Close'].ewm(span=89, adjust=False).mean()
            
            df['Close2'] = df['Close'].shift()
            df['Close3'] = df['Close2'].shift()
            df['Close4'] = df['Close3'].shift()
            
            def momentum_opposite(df):
              return not (df['Close']< df['Close2'] and df['Close2'] < df['Close3'])
            
            df['momentum_opposite_on'] = df.apply(momentum_opposite, axis=1)
            
            def cont_3_momentum_positive(df):
              return df['Close']> df['Close2'] and df['Close2'] > df['Close3'] and df['Close3'] > df['Close4']
            
            df['cont_3_momentum_positive'] = df.apply(cont_3_momentum_positive, axis=1)
            
            
            def above_21ema(df):
                return df['Close']> df['21dayEWM']
            
            df['above_21ema_on'] = df.apply(above_21ema, axis=1)
            
            def above_34ema(df):
                return df['Close']> df['34dayEWM']
            
            df['above_34ema_on'] = df.apply(above_34ema, axis=1)
            
            def in_stacked(df):
                # return df['Close']> df['8dayEWM'] and df['Close']> df['21dayEWM'] and df['Close']> df['34dayEWM'] and df['Close']> df['55dayEWM'] and df['Close']> df['89dayEWM']
                return df['Close']> df['8dayEWM'] > df['13dayEWM'] and df['13dayEWM'] > df['21dayEWM'] and df['21dayEWM'] > df['34dayEWM'] and df['34dayEWM'] > df['55dayEWM'] and df['55dayEWM'] > df['89dayEWM']
            
            df['stacked_on'] = df.apply(in_stacked, axis=1)
            
            try:
                    f = open(completeName_exit, "a")
                    print ("===================================================================" , file=f)
                    print ("===================================================================" )
                    print("{0} -> Last three sessions stock moved up = {1} \n" .format(symbol,df.iloc[-1]['cont_3_momentum_positive'] ), file=f)
                    print("{0} -> Last three sessions stock moved up = {1} \n" .format(symbol,df.iloc[-1]['cont_3_momentum_positive'] ))
                    
                    # if df.iloc[-1]['stacked_on'] == False or df.iloc[-1]['above_21ema_on']== False or df.iloc[-1]['above_34ema_on']== False or df.iloc[-1]['momentum_opposite_on']: 
                    print("{0} -> Stacked Postively = {1}, 21S-EWM = {2}, 34S-EWM = {3}, Momentum = {4} \n".format(symbol,df.iloc[-1]['stacked_on'],df.iloc[-1]['above_21ema_on'],df.iloc[-1]['above_34ema_on'],df.iloc[-1]['momentum_opposite_on'] ), file=f)
                    print("{0} -> Stacked Postively = {1}, 21S-EWM = {2}, 34dayEWM = {3}, Momentum = {4} \n".format(symbol,df.iloc[-1]['stacked_on'],df.iloc[-1]['above_21ema_on'],df.iloc[-1]['above_34ema_on'],df.iloc[-1]['momentum_opposite_on'] ))        
                    # else:
                        # continue
                    print ("===================================================================" , file=f)
                    print ("===================================================================" )
                    time.sleep(10)
                    f.close()
            except Exception:
                    pass    
    
def squeeze_print():
    
    print ("Writing to output file started at %s" % time.ctime())   
    f = open(completeName, "a")
    
    print ("===================================================================" , file=f)
    print ("Stocks which are in Squeeze Two Days before and coming out yesterday " , file=f)
    print ("===================================================================" , file=f)
    print ("===================================================================" )
    print ("Stocks which are in Squeeze Two Days before and coming out yesterday " )
    print ("===================================================================" )
    f.close()
    squeezedetection(-3,-1,1)
    
    f = open(completeName, "a")
    print ("===================================================================" , file=f)
    print ("Stocks which are in Squeeze Day before and coming out yesterday " , file=f)
    print ("===================================================================" , file=f)
    print ("===================================================================" )
    print ("Stocks which are in Squeeze Day before and coming out yesterday " )
    print ("===================================================================" )
    f.close()
    squeezedetection(-2,-1,1)
    
      
    f = open(completeName, "a")
    print ("==========================================================================================" , file=f) 
    f.close()
    
    f = open(completeName, "a")
    print ("End : %s" % time.ctime(), file=f)
    print ("Completed at %s \n" % time.ctime())
    print ("*******************************************************************" , file=f)
    f.close()
  
    


def main():
    # cls = lambda: system('cls')
    # cls()
    createdirectory()
    
    
    f = open(completeName, "a")
    print ("*******************************************************************" , file=f)
    print ("\nStart : %s" % time.ctime(), file=f)
    
    f.close()
    
    csv_selection = input ("Enter 1 for OLstocks,\nEnter 2 for 2000-Top-Companies,\nEnter 3 for NASDAQ\nEnter 4 for SP500\nEnter 5  OL + S&P500 + Losing Trade? \nEnter 6 for Test \nEnter 7 for Trade Status\n Or any key to skip downloading\n: ")
    if(csv_selection == '1'):
       f = open(completeName, "a")
       print ("Data : OL \n" , file=f)
       f.close()
       yfinancedownload('OSL.csv','1d')
       squeeze_print()
       
    elif(csv_selection == '2'):
       f = open(completeName, "a")
       print ("Data :2000-Top-Companies\n " , file=f)
       f.close() 
       yfinancedownload('2000.csv','1d')
       squeeze_print()
       
    elif(csv_selection == '3'):
       f = open(completeName, "a")
       print ("Data :NASDAQ\n " , file=f)
       f.close() 
       yfinancedownload('NASDAQ.csv','1h')
       squeeze_print()
       
    elif(csv_selection == '4'):
       f = open(completeName, "a")
       print ("Data :SP500\n " , file=f)
       f.close() 
       yfinancedownload('SP500.csv','1d')
       squeeze_print()
       
    elif(csv_selection == '5'):
       f = open(completeName, "a")
       print (" OL + S&P500 + Losing Trade?\n " , file=f)
       print ("OSL: \n", file=f)
       f.close()  
       yfinancedownload('OSL.csv','1d')
       squeeze_print()
       shutil.rmtree('datasets')
       os.makedirs('datasets')
       f = open(completeName, "a")
       print ("S&P500: \n", file=f)
       f.close() 
       yfinancedownload('SP500.csv','1d')
       squeeze_print()
       shutil.rmtree('datasets')
       os.makedirs('datasets')
       f = open(completeName, "a")
       print ("Data :Trade\n " , file=f)
       f.close() 
       yfinancedownload('Trade2.csv','1d')
    #    squeeze_print()
       exittrade()
       
    elif(csv_selection == '6'):
       f = open(completeName, "a")
       print ("Data :Trade\n " , file=f)
       f.close() 
       yfinancedownload('nasdaq100.csv','1h')
       squeeze_print()
    #    exittrade()
       
    elif(csv_selection == '7'):
        while(True):
            f = open(completeName, "a")
            print ("Data :Losing Trade?\n " , file=f)
            f.close() 
            yfinancedownload('nasdaq100.csv','1h')
    #    squeeze_print()
            exittrade()
            time.sleep(3000)

    else:
       print ('Skipping Downloading')
       squeeze_print()
    
    
    
if __name__ == "__main__":
    main()