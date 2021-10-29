import json
import re
import datetime

#input generated from knime
_input = r"input/purchase_record0.json"

def read_date(date_string):
    date = re.search('^\S+', date_string)[0]
    hour = re.search('\S+$', date_string)[0]

    return datetime.datetime.fromisoformat(date).replace(hour=int(hour))

class order:
    def __init__(self, o_id, date, uid, tag, fee, prod=set()):
        if not isinstance(prod, set):
            raise TypeError("product list must be in set")
        self.id = o_id
        self.date = read_date(date)
        self.uid = uid
        self.name = tag
        self.cost = fee
        self.prod = prod
        
    def order2dict(self):
        thisDict = {}
        thisDict.update({'oid': self.id,
                         'date': self.date,
                         'uid': self.uid,
                         'u_name': self.name,
                         'cost': self.cost,
                         'prod': self.prod
                         })
        return thisDict
        
    def __str__(self):
        return str(self.order2dict())
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(str(self.id))
    def __eq__(self, other): return other is self
    def __ne__(self, other): return other is not self
        
    #adds new item to order
    def add_prod(self, new_prod):
        if not isinstance(new_prod, SKU):
            raise TypeError(str(new_prod) + " is not a SKU object")

        if new_prod in self.prod:
            for existing_prod in self.prod:
                if existing_prod.id == new_prod.id:
                    existing_prod.qty += new_prod.qty
        else:
            self.prod.add(new_prod)
 
class SKU:
    def __init__(self, p_id, name, qty):
        self.id = p_id
        self.name = name
        self.qty = qty
        
    def __eq__(self, other):
        return self.id == other.id
        
    def __hash__(self):
        return hash(self.id)
    
    def SKU2dict(self):
        thisDict = {}
        thisDict.update({'pid': self.id,
                         'p_name': self.name,
                         'qty': self.qty
                         })
        return thisDict
        
    def __str__(self):
        return str(self.SKU2dict())
    
    def __repr__(self):
        return self.__str__()

def debug(r):
    for x in r:
        print()
        print('oid: ', r[x].id)
        print(r[x].prod)
        print()
        
def filter_high(rec, low_limit = 0, high_limit = 2147483647):
    filtered_rec = {}
    for x in rec:
        if rec[x]['price'] <= high_limit and rec[x]['price'] >= low_limit:
            filtered_rec.update({x:rec[x]})
    return filtered_rec

def print_date(date):
    s = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + ' ' + str(date.hour) 
    return s

def main():
    input_stream = json.loads(open(_input, 'r').read())
    
    purchase_record = {}

    for line in input_stream:
        oid = line['order_id'] 
        if not oid in purchase_record:
            purchase_record.update({oid: {'date': line['order_date'], 
                                          'uid': line['customer_id'], 
                                          'u_name': line['customer_tag'], 
                                          'price': line['org_product_fee_no_tax'],
                                          'prod': set()
                                          }})
        
        purchase_record[oid]['prod'].add(SKU(line['product_id'], line['product'], line['qty']))
    
    
    pr_n = filter_high(purchase_record, 0, 400)
    
    for x in pr_n:
        print (x, '"'+pr_n[x]['date']+'"', pr_n[x]['uid'], '"'+pr_n[x]['u_name']+'"', pr_n[x]['price'], '"'+str(pr_n[x]['prod'])+'"', sep=', ')

        
        

if __name__ == "__main__":
    main()
