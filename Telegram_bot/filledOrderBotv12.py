import time, telegram_send
from binance.client import Client
from datetime import datetime
import personal_function as pf

#api_key='abcdef'   #write your Binance API Key inside brackets 
#api_secret= 'adafasfsaf' #write your Binance API secret inside brackets 
#config_telegram = "Giang.conf"

lenOldOrderId = 20
listOldOrderId = [0] * lenOldOrderId
listNewOrderId = [0] * lenOldOrderId

    
def checkFilledOrderSpot(client,orderOld):
##check spot filled orders
    global listOldOrderId, listNewOrderId
    lenOrderOld=len(orderOld)    
    orderNew=client.get_open_orders()  
   
    if (orderNew != orderOld):
        for i in range(lenOrderOld):
            tempOrder=orderOld[i]
            symbol=tempOrder['symbol']
            orderId=tempOrder['orderId']
            
            
            if orderId not in listOldOrderId:
                orderChecking=client.get_order(symbol=symbol,orderId=orderId)
                if (orderChecking['status']=='FILLED'): 
                    symbolFilled=orderChecking['symbol']
                    sideFilled=orderChecking['side']
                    # typeFilled=orderChecking['type']                    
                    # executedQtyFilled=orderChecking['executedQty']
                    
                    cummulativeQuoteQtyFilled=orderChecking['cummulativeQuoteQty']  
                    priceFilled=orderChecking['price']                    
                    
                    # msgSpot='SPOT Order '+ typeFilled + ' ' + sideFilled +" of " + symbolFilled + ' has been filled.\n' \
                    #     + 'PRICE: ' +  priceFilled  + '\n' \
                    #         +'Time: '+ tmFilled + ' SGT\n' \
                    #             + 'Amount: ' + executedQtyFilled +'\n' \
                    #                 + 'Total Quote: '+cummulativeQuoteQtyFilled 
                    if (float(cummulativeQuoteQtyFilled) >= 200.0) and (sideFilled.lower()=='buy'):
                        msgSpot= '💹 BUY ' + symbolFilled + ' at price: ' +  priceFilled
                        telegram_send.send(messages=[msgSpot])
                    elif (float(cummulativeQuoteQtyFilled) >= 0.0) and (sideFilled.lower()=='sell'):
                        msgSpot='🆘 SELL ' + symbolFilled + ' at price: ' +  priceFilled
                        telegram_send.send(messages=[msgSpot])
                    
                    listNewOrderId[0:lenOldOrderId-1]=listOldOrderId[1:lenOldOrderId]
                    listNewOrderId[lenOldOrderId-1]=orderId
                    listOldOrderId=listNewOrderId.copy()    
    return orderNew

def checkFilledOrderFuture(client,oldPosition):
##check future filled orders
    # global listOldFutureOrderId, listNewFutureOrderId
    # lenOldPosition=len(oldPosition)    
    
    newPosition=client.futures_position_information()
    newPosition = [{k: v for k, v in d.items() if k == 'symbol' or k == 'positionAmt'} for d in newPosition]    
    # newPosition = [{k: v for k, v in d.items() if k != 'updateTime'} for d in newPosition]
    
    list_difference = []
    
    if (newPosition != oldPosition):        
        minlen = min(len(oldPosition),len(newPosition)) 
        for i in range(minlen):
            item1 = newPosition[i]
            item2 = oldPosition[i]
            if item1 != item2:
                list_difference.append(item1)
        
        if list_difference != []:
            for item in list_difference:
                # tempOrder=futureOrderOld[i]
                symbol=item['symbol']
                symbolOrders = client.futures_get_all_orders(symbol=symbol)
                
                tempList = []
                for d in symbolOrders:
                    if d['status'] == 'FILLED':
                        tempList.append(d['updateTime'])
                if tempList != []:
                    max_value = max(tempList)
                    for orderChecking in symbolOrders:
                        if orderChecking['updateTime'] == max_value and orderChecking['status'] == 'FILLED':
                            symbolFilled=orderChecking['symbol']
                            sideFilled=orderChecking['side']
                            typeFilled=orderChecking['type']                    
                            executedQtyFilled=orderChecking['executedQty']
                            tif = orderChecking['timeInForce']
                            posSide = orderChecking['positionSide']                        
                            cummulativeQuoteQtyFilled=orderChecking['cumQuote']  
                            priceFilled=orderChecking['avgPrice']                    
                            
                            if tif == 'IOC':
                                msgFuture='Future Order '+ 'LIQUIDATION ' + sideFilled +" of " + symbolFilled + ' ' + posSide + ' has been filled.\n' \
                                    + 'PRICE: ' +  priceFilled  + '\n' \
                                        + 'Amount: ' + executedQtyFilled +'\n' \
                                            + 'Total Quote: '+cummulativeQuoteQtyFilled 
        
                            else:
                                msgFuture='Future Order '+ typeFilled + ' ' + sideFilled +" of " + symbolFilled + ' ' + posSide + ' has been filled.\n' \
                                    + 'PRICE: ' +  priceFilled  + '\n' \
                                        + 'Amount: ' + executedQtyFilled +'\n' \
                                            + 'Total Quote: '+cummulativeQuoteQtyFilled 
                            telegram_send.send(messages=[msgFuture])                    
                            telegram_send.send(messages=[msgFuture])
                        
    return newPosition


#%%
# First time to run
client = pf.client()   
orderOld=client.get_open_orders() #spot
oldPosition = client.futures_position_information() #future
oldPosition = [{k: v for k, v in d.items() if k == 'symbol' or k == 'positionAmt'} for d in oldPosition]    
# oldPosition = [{k: v for k, v in d.items() if k != 'updateTime'} for d in oldPosition]
sleeptime=30

telegram_send.send(messages=['Hello, This is the binance filled order bot.'])
#telegram_send.send(messages=["Wow that was easy!"])
while True:
    print('Is checking at',datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))   
    
    try:        
        orderOldTemp=checkFilledOrderSpot(client,orderOld)
        orderOld = orderOldTemp
        print('Finish checking SPOT orders')
        time.sleep(sleeptime)
    except:
        print('Error in checkFilledOrderSpot, retrying...')
        time.sleep(sleeptime)
        continue   

    try:
        oldPositionTemp=checkFilledOrderFuture(client,oldPosition)        
        oldPosition = oldPositionTemp
        print('Finish checking FUTURE orders')
        time.sleep(sleeptime)
        
    except:
        print('Error in checkFilledOrderFuture, retrying...')        
        time.sleep(sleeptime)
        continue
    
    
    

