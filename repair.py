import random
from read_data import t_arrive, travel_time, wait_time
def calcule_time_pathe(path,depot):
    for element in path:
        element.arrival_time = 0
        element.departure_time = 0
    current_time = 0
    for i, loc in enumerate(path):
        arrival_time = t_arrive(path, i)
        wait = wait_time(arrival_time, loc.O)
        loc.arrival_time = arrival_time
        loc.departure_time = arrival_time + wait + loc.d
        current_time = loc.departure_time
    return round(current_time)

def calculate_profit(path):
    total_profit = sum(loc.S for loc in path)
    return total_profit
def is_valid_path(path, depot, Tmax):
    # print("tmax",Tmax)
    current_time = 0
    for i, loc in enumerate(path):
 
        arrival_time = t_arrive(path, i)
        if arrival_time > loc.C:
            return False  # Arrival time is after the closing time
        wait = wait_time(arrival_time, loc.O)
        loc.arrival_time = arrival_time
        loc.departure_time = arrival_time + wait + loc.d
        current_time = loc.departure_time

    for element in path:
        element.arrival_time = 0
        element.departure_time = 0
    # Check if we can return to the depot on time
    if current_time + travel_time(path[-1], depot) > Tmax:
        print("tmax the path",current_time + travel_time(path[-1], depot))
        return False
    else:
        udate = [loc.i for loc in path] 
        print("path", udate)
        print("full path time", current_time + travel_time(path[-1], depot))
    return True

def repaire_greedy(paths,liste_non_visited, depot, Tmax ):
    print ("la methode repaire_greedy")
    for path in paths:
        if not path:
            path.extend([depot, depot])
        else:
            if path[0].i != depot.i:
                path.insert(0, depot)
            if path[-1].i != depot.i:
                path.append(depot)
            for h in liste_non_visited:
                if h.i==depot.i:
                   liste_non_visited.remove(h)
            # if depot in liste_non_visited:
            #             print ("yesss")
            #             liste_non_visited.remove(depot)
            # else :
            #             print("nooooo")  
    # print("uuuuuuuuuuuuuuuuuuuuuuuuuuuu",liste_non_visited)
    
    points_sorted = sorted(liste_non_visited, key=lambda loc: loc.S, reverse=True)
    points_sortede = [loc.i for loc in points_sorted]
    # print("points_sorted_no insert",points_sortede)
    uninserted_points = []
    
    for point_loc in points_sorted:
        for path in paths:
            best_profit = -float('inf')
            best_position = None
            for i in range(1, len(path)):
                path.insert(i, point_loc)
                # if point_loc.i==1:

                #print("ramdan",is_valid_path(path, depot, Tmax))
                if is_valid_path(path, depot, Tmax):
                    # print("time path is ",calcule_time_pathe(path,depot))

                    profit = calculate_profit(path)
                    udate = [loc.i for loc in liste_non_visited] 
                    # print("la liste_non_visited_  avent remove point_loc est   ",udate)
                    # print("la point_loc est ",point_loc.i )
                    
                    for element in liste_non_visited:
                            if element.i ==point_loc.i:
                                liste_non_visited.remove(element)
                                break
                    # print ("yesss")
                    udadte = [loc.i for loc in liste_non_visited] 
                    # print("la liste_non_visited_  appré remove point_loc est   ",udadte)
                    # print(point_loc.i)
                        # liste_non_visited.remove(point_loc)
                    if profit > best_profit:
                        best_profit = profit
                        best_position = i

                path.pop(i)
                # print("eeeeeee",point_loc.i)
            if best_position is not None:
                path.insert(best_position, point_loc)
                #inserted = True
                break

    # udadte = [loc.i for loc in liste_non_visited] 
    # print("oute of function   ",udadte)
    return paths, liste_non_visited #, total_profit





# def repaire_temp(pathe,point):
#     for i in pathe:
#         if i.i==point:
#            tmax=t_arrive(pathe,i)+travel_time()
        
#     return tmax  

def repaire_fin(liste_non_visited, depot, Tmax, path):
    tested_points = set()
    print ("la methode repaire_fin")
    
    if not path or path[0].i != depot.i:
        path.insert(0, depot)
        if depot in liste_non_visited:
            liste_non_visited.remove(depot)
    no_insert = [loc.i for loc in liste_non_visited]        
    # print('iiiiiiiii',no_insert)        
    # if liste_non_visited:
    #     print ("ttttttttttt",liste_non_visited[0].i)
    #     liste_non_visited.remove(liste_non_visited[0])
    while liste_non_visited:
        point = random.choice(liste_non_visited)
        
        path.append(point)
        if point.i == depot.i:
            path.pop()
        else:
           if is_valid_path(path, depot, Tmax):
                    # print("time path is ",calcule_time_pathe(path,depot))
                    for i in liste_non_visited:
                        if i.i == point.i:
                            
                            # print("eeeeeeeeee")
                            # no_insert = [loc.i for loc in liste_non_visited]    
                            # print (no_insert) 
                            # print(i.i)
                            liste_non_visited.remove(i) # إزالة العنصر باستخدام pop
                            # print("kkkkk")
                            # no_insert = [loc.i for loc in liste_non_visited]    
                            # print (no_insert) 
                            tested_points.clear()
           else:
                path.pop()
                tested_points.add(point)
                
                if len(tested_points) == len(liste_non_visited):
                    break
    
    if path[-1].i != depot.i:
        path.append(depot)
    
    #profit = calculate_profit(path)
    
    return path, liste_non_visited #,#profit
def shortest_path_insertion(paths, liste_non_visited, depot, Tmax):
    # تأكد من أن كل مسار يبدأ وينتهي بالـ depot
    print ("la methode shortest_path_insertion")

    for path in paths:
        if not path:
            path.extend([depot, depot])
        else:
            if path[0].i != depot.i:
                path.insert(0, depot)
            if path[-1].i != depot.i:
                path.append(depot)
    
    # إزالة الـ depot من liste_non_visited
    liste_non_visited = [h for h in liste_non_visited if h.i != depot.i]

    # نستخدم نسخة من liste_non_visited حتى نستطيع التعديل عليها أثناء التكرار
    for city in liste_non_visited[:]:
        best_insertion_index = None  # أفضل موقع للإدخال
        best_increase = float('inf')  # أقل زيادة في وقت السفر
        
        # نبحث عن أفضل مكان لإدخال المدينة الجديدة
        for path in paths:
            for i in range(1, len(path)):
                prev_city = path[i - 1]  # المدينة السابقة
                next_city = path[i] if i < len(path) else None  # المدينة التالية

                if next_city is None:
                    increase = travel_time(prev_city, city)  # زيادة وقت السفر إذا كانت المدينة هي الأخيرة
                else:
                    # حساب زيادة وقت السفر عند إدخال المدينة بين المدينة السابقة والتالية
                    increase = travel_time(prev_city, city) + travel_time(city, next_city) - travel_time(prev_city, next_city)
                
                if increase < best_increase:
                    path.insert(i, city)  # إدخال المدينة بشكل مؤقت للتحقق من صلاحية المسار
                    if is_valid_path(path, depot, Tmax):
                        best_increase = increase  # تحديث أقل زيادة في وقت السفر
                        best_insertion_index = i  # تحديث أفضل موقع للإدخال
                    path.pop(i)  # إزالة الإدخال المؤقت إذا لم يكن المسار صالحاً
            
            # إذا وجدنا موقعاً جيداً للإدخال
            if best_insertion_index is not None:
                path.insert(best_insertion_index, city)  # إدخال المدينة بشكل دائم
                liste_non_visited.remove(city)  # إزالة المدينة من القائمة الغير زائرة
                break  # الخروج من الحلقة بعد إدخال المدينة

    # تأكد من أن كل مسار ينتهي بالـ depot
    for path in paths:
        if path[-1].i != depot.i:
            path.append(depot)

    return paths, liste_non_visited  # إعادة المسارات والقائمة المحدثة للمدن الغير زائرة
