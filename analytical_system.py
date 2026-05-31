import mysql.connector
import matplotlib.pyplot as plt
from datetime import date 
conn=mysql.connector.connect(
    host="localhost",
    user='root',
    password='PassMysql@1',
    database='vcube',
)
cursor=conn.cursor()
cursor = conn.cursor(buffered=True)
items_list=[]
price_list=[]
weight_list=[]
profits=[]
#INTERFACE PAGE
print('''1.customer\n2.Owner''')
try:
 login_mode=int(input('choose correct option:'))
except  ValueError:
    print('option should be numeric')
if login_mode==1:
    while True:
        print('''1.Login\n2.Register\n3.Exit''')
        login=int(input('choose correct option:'))
        #CUSTOMER PAGE
        if login==1:
            user_id = int(input('Enter your login id: '))
            user_pass = input('Enter your password: ')
            query = """
            SELECT id
            FROM customer c
            JOIN passwords p ON c.p_id = p.p_id
            WHERE id = %s AND p.pass = %s"""

            cursor.execute(query, (user_id, user_pass))
            login_ver = cursor.fetchone()
            if login_ver == None:
                 print("Invalid Credentials")
                 break
            else:                 
              print("Login successful")
              query1 = """SELECT i.item_name,c.cost,w.weight from inventory i inner join costs c
               on i.c_id=c.c_id inner join weights w on i.w_id=w.w_id"""
              cursor.execute(query1)
              inventory = cursor.fetchall()
              print("Inventory Items:")
              print('*'*10,'ITEMS LIST','*'*10)
              print(f"{'Item':<10}{'Cost':<10}{'Weight':<10}")
              if len(inventory)==0:
                  print('no items here')
              else:
                  for item, cost, weight in inventory:
                      print(f"{item:<20}{cost:<20}{weight:<20}")
                  print()
                  #CART OPERATIONS
                  while True:
                      print("1.Add Item to cart\n2.Remove Item\n3.Update Item\n4.View\n5.Bill\n6.Pay\n7.Exit")
                      log_val=int(input('Enter your choice:'))
                      if log_val==1:
                          while True:
                              item=input("Enter Item Name to be add:")
                              query="select item_name from inventory"
                              cursor.execute(query)
                              list_vals=cursor.fetchall()
                              if (f'{item}',) in list_vals:
                                  items_list.append(item)
                                  while True:
                                      try:
                                         item_weight=int(input("Enter weight of item:"))
                                      except  ValueError as e:
                                          print(e)
                                      query="select w_id from inventory where item_name=%s"
                                      cursor.execute(query,(item,))
                                      w_id=cursor.fetchone()
                                      query="select weight from weights where w_id=%s "
                                      cursor.execute(query,(w_id[0],))
                                      weights_vals=cursor.fetchone()
                                      if item_weight < weights_vals[0]:
                                                    weight_list.append(item_weight)
                                                    new_val=weights_vals[0]-item_weight
                                                    query="""update weights set weight=%s where
                                                    w_id=%s"""
                                                    cursor.execute(query,(new_val,w_id[0]))
                                                    break
                                      else:
                                          print(f'The item weights is only {weights_vals}kgs')
                                          break
                                  query="select c_id from inventory where item_name=%s"
                                  cursor.execute(query,(item,))
                                  c_id=cursor.fetchone()
                                  query="select cost,actual_value from costs where c_id=%s "
                                  cursor.execute(query,(c_id[0],))
                                  cost=cursor.fetchone()    
                                  if cost[0]>0:
                                        price_list.append(cost[0]*item_weight)
                                        profit_val=cost[0]*item_weight-cost[1]*item_weight
                                        cur_date=date.today()
                                        query='insert into profit values(%s,%s)'
                                        cursor.execute(query,(cur_date,profit_val))
                                        print('nice')
                                  else:
                                       print('somthing wrong')
                              else:
                                  print('sorry this item not availble')
                              print("item added to cart successfully")
                              note=input('Do you want another item (yes/no):')
                              if note=='yes':
                                  pass
                              else:
                                  break
                      #DELETE ITEM FROM CART
                      elif log_val==2:
                          item=input('which item you want delete:')
                          if item in items_list:
                              items_list.remove(item)
                              print('Item seccessfully deleted')
                      #UPDATE ITEM IN  CART
                      elif log_val==3:
                          item=input('which item you want update:')
                          if item in items_list:
                              idx=items_list.index(item)
                              new_weight=int(input('Enter new weight of item:'))
                              weight_list[idx]=new_weight
                              query="select w_id,c_id from inventory where item_name=%s"
                              cursor.execute(query,(item,))
                              w_id=cursor.fetchone()
                              query='select cost from costs where c_id=%s'
                              cursor.execute(query,(w_id[1],))
                              original_cost=cursor.fetchone()
                              price_list[idx]=new_weight*original_cost[0]
                              query="select weight from weights where w_id=%s"
                              cursor.execute(query,(w_id[0],))
                              original_weight=cursor.fetchone()
                              update_val=original_weight[0]-new_weight
                              query='update weights set weight=%s where w_id=%s'
                              cursor.execute(query,(update_val,w_id[0]))
                              print('Item succesfully updated')
                              print()
                      #CART VIEW
                      elif log_val==4:
                          print('*'*10,'CART','*'*10)
                          print('-'*20)
                          print(f"{'Item':<10}{'Cost':<10}{'Weight':<10}")
                          print('-'*20)
                          for i,j,k in zip(items_list,price_list,weight_list):
                              print(f'{i:<10} {j:<10} {k:<10}')
                          print('-'*20)
                          print()
                          print()
                      #BILL CALCULATION
                      elif log_val==5:
                          print('*'*10,'CART','*'*10)
                          print('-'*20)
                          print(f"{'Item':<10}{'Cost':<10}{'Weight':<10}")
                          print('-'*20)
                          for i,j,k in zip(items_list,price_list,weight_list):
                              print(f'{i:<10} {j:<10} {k:<10}')
                          print('-'*20)
                          print()
                          print()
                          Total=sum(price_list)
                          print('-'*20)
                          print("BILL: ",Total)
                          print('-'*20)
                          print('*'*10,'Pay now','*'*10)
                          print()
                      #PAYMENT PROCESS  
                      elif log_val==6:
                          Total=sum(price_list)
                          amount=int(input('Enter amount to pay:'))
                          if amount==Total:
                              print('*'*10,"THANK YOU",'*'*10)
                              conn.commit()
                              break
                          else:
                              print('amount not match to bill')
                              break
                      else:
                          print("THANK YOU")
                          break
                          
                    
        #REGISTER PAGE   
        elif login==2:
                user_name = input('Enter your name: ')
                user_pass = input('Enter your password: ')
                user_address = input('Enter your address: ')
                user_mobile = input('Enter your mobile number: ')
                def pas_val(p):
                    query = "INSERT INTO passwords(pass) VALUES(%s)"
                    cursor.execute(query, (p,))
                    conn.commit()

                    cursor.execute("SELECT p_id FROM passwords WHERE pass=%s", (p,))
                    val = cursor.fetchone()

                    return val[0] if val else "no val"
                def add_val(a):
                    query = "INSERT INTO customer_address(address) VALUES(%s)"
                    cursor.execute(query,(a,))
                    conn.commit()

                    cursor.execute("SELECT c_a_id FROM customer_address WHERE address=%s", (a,))
                    val = cursor.fetchone()

                    return val[0] if val else None
                def mobile_val(m):
                    query = "INSERT INTO customer_mobiles(mobile) VALUES(%s)"
                    cursor.execute(query, (m,))
                    conn.commit()

                    cursor.execute("SELECT c_id FROM customer_mobiles WHERE mobile=%s", (m,))
                    val = cursor.fetchone()

                    return val[0] if val else None
                p_id = pas_val(user_pass)
                c_a_id = add_val(user_address)
                c_id = mobile_val(user_mobile)
               
                if p_id and c_a_id and c_id:
                    query = """
                    INSERT INTO customer (name, c_id, c_a_id, p_id)
                    VALUES (%s, %s, %s, %s)
                    """

                    values = (user_name, c_id, c_a_id, p_id)

                    cursor.execute(query, values)
                    conn.commit()

                    print("Registration successfully completed")
                    print("Your customer ID is:", cursor.lastrowid)

                else:
                    print("Error: Could not create foreign key references")
        else:
            print("*"*10,"Thank You","*"*10)
            break
#OWNER PAGE LOGIN
elif login_mode==2:
    name=input('Enter your name:')
    pw=input('Enter your password:')
    if name=="venkatesh" and pw=="venkatesh":
        #OWNER OPERATIONS
        while True:
            print('1.Update inventory\n2.customer details\n3.Profit\n4.Exit')
            option=int(input('Enter your option:'))
            if option==1:
                print('1.Update item\n2.Delete item\n3.insert item\n4.Display inventory')
                p1=int(input('Enter your option:'))
                if p1==1:
                    item=input('Enter item name to update:')
                    query="select item_id,w_id,c_id from inventory where item_name=%s"
                    cursor.execute(query,(item,))
                    val=cursor.fetchone()
                    if val:
                        item_id = val[0]
                        w_id = val[1]
                        c_id = val[2]
                        print('1.cost\n2.weight')
                        up_val=int(input('Select a option to update:'))
                        if up_val==1:
                                up_val1=int(input('Enter new cost of item:'))
                                query="update  costs set cost=%s where c_id=%s"
                                cursor.execute(query,(up_val1,c_id))
                                conn.commit()
                                print('successfully updated')
                                
                        elif up_val==2:
                                up_val1=int(input('Enter new weight of item:'))
                                query="update weights SET weight=%s where w_id=%s"
                                cursor.execute(query,(up_val1,w_id))
                                conn.commit()
                                print('successfully updated')
                        else:
                            print('invalid option')
                        conn.commit()
                    
                if p1==2:
                    item=input('Enter item to delete:')
                    query="select item_id from inventory where item_name=%s"
                    cursor.execute(query,(item,))
                    val=cursor.fetchone()
                    if val is not None:
                        cursor.execute("select w_id,c_id from customer where id=%s",(val[0],))
                        values=cursor.fetchone()
                        cursor.execute("delete from weights where w_id=%s",(values[0],))
                        cursor.execute("delete from weights where w_id=%s",(values[1],))
                        query="delete from inventory where item_name=%s"
                        cursor.execute(query,(item,))
                        print('Item deleted succesfully')
                    else:
                        print('Item not existed')
                    conn.commit()
                #INSERT ITEMS INTO INVENTORY
                if p1==3:
                    item = input('Enter item name: ')
                    cursor.execute("insert into inventory(item_name)values(%s)",(item,))
                    cursor.execute(
                        "SELECT item_id FROM inventory WHERE item_name=%s",
                        (item,)
                    )
                    val = cursor.fetchone()
                    if val:
                        cost = int(input('Enter cost: '))
                        cost_price=int(input('Enter cost_price:'))

                        cursor.execute(
                            "INSERT INTO costs(cost,actual_value) VALUES(%s,%s)",
                            (cost,cost_price)
                        )

                        cost_id = cursor.lastrowid
                        weight = int(input('Enter weight: '))

                        cursor.execute(
                            "INSERT INTO weights(weight) VALUES(%s)",
                            (weight,)
                        )

                        weight_id = cursor.lastrowid

                        cursor.execute(
                            "update inventory set c_id=%s,w_id=%s where item_id=%s",
                            (cost_id, weight_id,val[0])
                        )

                        conn.commit()

                        print('Successfully added')

                    else:
                        print('Item already exists')
                #INVENTORY VIEW
                if p1==4:
                    cursor.execute("select item_name from inventory")
                    a1=cursor.fetchall()
                    cursor.execute("select weight from weights")
                    a2=cursor.fetchall()
                    cursor.execute("select cost from costs")
                    a3=cursor.fetchall()
                    print('*'*10,'ITEM LIST','*'*10)
                    print(f"{'Item':<15} {'Weight':<15} {'Cost':<15}")
                    for a,b,c in zip(a1,a2,a3):
                      print(f'{a[0]:<15} {b[0]:<15} {c[0]:<15}')
                    print('*'*19)
            elif option==2:           
                cursor.execute("select name from customer")
                a1=cursor.fetchall()
                cursor.execute("select address from customer_address")
                a2=cursor.fetchall()
                cursor.execute("select mobile from customer_mobiles")
                a3=cursor.fetchall()
                print('*'*20,"CUSTOMERS DETAILS",'*'*20)
                for a,b,c in zip(a1,a2,a3):
                    print(f"{'Name':<15} {'Address':<10} {'Mobile':<10}")
                    print(*a,' '*2,*b,' '*2,*c,' '*3)
                    print('-'*17)
                print('*'*50)
            #PROFIT GRAPH
            elif option==3:
                query='select *from profit'
                cursor.execute(query)
                records=cursor.fetchall()
                dates = [row[0].strftime("%d-%m-%Y") for row in records]
                profits=[row[1] for row in records]
                plt.figure(figsize=(10,5))
                plt.plot(dates, profits, marker='o')
                plt.title("Daily Profit Analysis")
                plt.xlabel("Date")
                plt.ylabel("Profit")
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            elif option==4:
                break
            else:
               print('please,select valid option')
    else:
         print("invalid credintial")
else:
    print('pleases choose correction option')

    
conn.commit()
conn.close()
