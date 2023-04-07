from datetime import date, time, timedelta, datetime
import argparse
import json
import os

class PillControl():
    
    def __init__(self, startDate, pillTime="22:30:00", pills_per_day=2, initial_stock=30):
        if (not initial_stock):
            initial_stock=30
            print("Trigger")
        
        self.pillTime = time.fromisoformat(pillTime)
        self.startDate = date.fromisoformat(startDate)
        self.pills_per_day = pills_per_day
        self.initial_stock = initial_stock
   
    def get_deadline(self):
        if self.pills_per_day > 1:
            deadline = self.startDate + timedelta(days=(self.initial_stock/2)-1)
            return deadline


        deadline = self.startDate + timedelta(days=self.initial_stock-1)

        return deadline

    def getStock(self):
        today = date.today()
            
        stock = self.get_deadline() - today 

        if datetime.now().time() < self.pillTime:
            stock = stock + timedelta(days=1)

        if self.pills_per_day > 1:
            return(stock.days*2)

        return stock.days
            

    def printResults(self):
        try:
            print('\t\t YYYY MM DD')
            print(f"Fecha de inicio  {self.startDate} con {self.initial_stock} pildoras")
            print(f"Fecha limite     {self.get_deadline()} a las {self.pillTime} horas")
            print(f'Stock actual     {self.getStock()} pildoras')
            print(f"Consumiendo      {self.pills_per_day} pildoras diarias ")
            return True
        except:
            return False


      
    def toDict(self):
        return {
            'startDate': self.startDate.isoformat(),
            'time':self.pillTime.isoformat(),
            'initialStock':self.initial_stock,
            'pillsPerDay':self.pills_per_day,
            }

        
def file_is_empty(path):
    return os.stat(path).st_size==0

def saveToDisk(data:dict):
    with open('sample2.json', 'w') as outfile: 

        json.dump(data, outfile)



def ReadUserInput():
    if (not file_is_empty('sample2.json')):
        with open('sample2.json','r') as read_content:
            json_obj = json.load(read_content)


            return PillControl(
                startDate= json_obj['startDate'],
                pillTime = json_obj['time'],
                initial_stock= int(json_obj['initialStock']),
                pills_per_day=int(json_obj['pillsPerDay']),
            )

def InputArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--date', type= date.fromisoformat)
    parser.add_argument('-s', '--stock', type=int, help="Initial stock")
    parser.add_argument('-r','--reset',action='store_true', help='stock to 30 and initial date to today')
    parser.add_argument('-w', '--write',action='store_true', help='save input to disk' )

    args = parser.parse_args()
    if (args.date and args.stock):
        startDate = args.date.isoformat()
        newInput = PillControl(startDate=startDate, initial_stock=args.stock)
        if (args.save):
            saveToDisk(newInput.toDict())
        return newInput.printResults()

    if(args.reset):
        today = date.today().isoformat()
        mydict = PillControl(startDate=today, initial_stock=30).toDict()
        if (args.save):
            saveToDisk(mydict)

        


def main():
    InputArgs()

    saved = ReadUserInput()
    if (saved):
        saved.printResults()
        return
    else:
        print('No hay registros')


if (__name__ == '__main__'):
    main()
        
