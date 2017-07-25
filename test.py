def open_files(p):
    pressure = p

    if float(pressure) <= 1:
        table_z0 = open('Z0_1.csv')
    else:
        table_z0 = open('Z0_2.csv')

    if float(pressure) >= 1:
        table_z1 = open('Z1_2.csv')
    else:
        table_z1 = open('Z1_1.csv')

    table_z0_lines = table_z0.readlines()
    table_z1_lines = table_z1.readlines()
    num1_lines = len(table_z0_lines)
    num2_lines = len(table_z1_lines)

    return table_z0_lines, table_z1_lines


def sort(z0_lines, z1_lines):
    tr_values = []
    values_z0 = []

    #tr_values_z1 = []
    values_z1 = []

    pr_values = z0_lines[3].split(',')
    pr_values = [float(i) for i in pr_values]

    for i in range(4, len(z0_lines)):
        line = z0_lines[i].split(',')
        line = [float(i) for i in line]

        #first_value = line[0]
        #tr_values_z0.append(first_value)
        line.remove(line[0])

        values_z0.append(line)

    #tr_values_z0 = [float(i) for i in tr_values_z0]

    #pr_values_z1 = z1_lines[3].split(',')
    #pr_values_z1 = [float(i) for i in pr_values_z1]

    for i in range(4, len(z1_lines)):
        line = z1_lines[i].split(',')
        line = [float(i) for i in line]

        first_value = line[0]
        tr_values.append(first_value)
        line.remove(first_value)

        values_z1.append(line)

    tr_values = [float(i) for i in tr_values]

    return (pr_values, tr_values, values_z0, values_z1)


def find_value(pr, tr, pr_val, tr_val, val_z0, val_z1):
    press = float(pr)
    temp = float(tr)

    if temp > 1.1 and press < 1:
        return float('NaN'), float('NaN')
    elif temp > 1.5 and press > 1:
        return float('NaN'), float('NaN')
    else:
        try:
            pr_index = pr_val.index(press)
        except ValueError, e:
            try:
                tr_index = tr_val.index(temp)
                # Tr value is in table, Pr is not
                print "tr in table, pr not in table"
                for i in range (0, len(pr_val) - 1):
                    if pr_val[i] <= press:
                        if pr_val[i + 1] < press and i == len(pr_val) - 2:
                            return float('NaN'), float('NaN')
                        elif pr_val[i + 1] < press:
                            continue
                        else:
                            x0_pr = pr_val[i]
                            x1_pr = pr_val[i + 1]

                            y0_z0_pr1, y0_z1_pr1 = find_value(x0_pr, temp,
                                                              pr_val, tr_val,
                                                              val_z0, val_z1)
                            y1_z0_pr1, y1_z1_pr1 = find_value(x1_pr, temp,
                                                              pr_val, tr_val,
                                                              val_z0, val_z1)
                            break
                    else:
                        return float('NaN'), float('NaN')

                z0 = ((y1_z0_pr1 - y0_z0_pr1) * (press - x0_pr) / (x1_pr - x0_pr)
                       + y0_z0_pr1)
                z1 = ((y1_z1_pr1 - y0_z1_pr1) * (press - x0_pr) / (x1_pr - x0_pr)
                       + y0_z1_pr1)

                return z0, z1
            except ValueError, e:
                # Pr and Tr are not in table
                print "pr and tr not in table"
                for i in range (0, len(tr_val) - 1):
                    if tr_val[i] <= temp:
                        if tr_val[i + 1] < temp and i == len(tr_val) - 2:
                            return float('NaN'), float('NaN')
                        elif tr_val[i + 1] < temp:
                            continue
                        else:
                            x0_tr = tr_val[i]
                            x1_tr = tr_val[i + 1]
                            break
                    else:
                        return float('NaN'), float('NaN')
                for i in range (0, len(pr_val) - 1):
                    if pr_val[i] <= press:
                        if pr_val[i + 1] < press and i == len(pr_val) - 2:
                            return float('NaN'), float('NaN')
                        elif pr_val[i + 1] < press:
                            continue
                        else:
                            x0_pr = pr_val[i]
                            x1_pr = pr_val[i + 1]

                            y0_z0_pr1, y0_z1_pr1 = find_value(x0_pr, x0_tr,
                                                              pr_val, tr_val,
                                                              val_z0, val_z1)
                            y1_z0_pr1, y1_z1_pr1 = find_value(x1_pr, x0_tr,
                                                              pr_val, tr_val,
                                                              val_z0, val_z1)
                            y0_z0_pr2, y0_z1_pr2 = find_value(x0_pr, x1_tr,
                                                              pr_val, tr_val,
                                                              val_z0, val_z1)
                            y1_z0_pr2, y1_z1_pr2 = find_value(x1_pr, x1_tr,
                                                              pr_val, tr_val,
                                                              val_z0, val_z1)
                            break
                    else:
                        return float('NaN'), float('NaN')

                z0_1 = ((y1_z0_pr1 - y0_z0_pr1) * (press - x0_pr) / (x1_pr - x0_pr)
                         + y0_z0_pr1)
                z1_1 = ((y1_z1_pr1 - y0_z1_pr1) * (press - x0_pr) / (x1_pr - x0_pr)
                         + y0_z1_pr1)

                z0_2 = ((y1_z0_pr2 - y0_z0_pr2) * (press - x0_pr) / (x1_pr - x0_pr)
                         + y0_z0_pr2)
                z1_2 = ((y1_z1_pr2 - y0_z1_pr2) * (press - x0_pr) / (x1_pr - x0_pr)
                         + y0_z1_pr2)

                z0_3 = (z0_2 - z0_1) * (temp - x0_tr) / (x1_tr - x0_tr) + z0_1
                z1_3 = (z1_2 - z1_1) * (temp - x0_tr) / (x1_tr - x0_tr) + z1_1

                return float(z0_3), float(z1_3)
        try:
            tr_index = tr_val.index(temp)
        except ValueError, e:
            # Pr value in table, Tr is not
            print "pr in table, tr not in table"
            for i in range (0, len(tr_val) - 1):
                if tr_val[i] <= temp:
                    if tr_val[i + 1] < temp and i == len(tr_val) - 2:
                        return float('NaN'), float('NaN')
                    elif tr_val[i + 1] < temp:
                        continue
                    else:
                        x0_tr = tr_val[i]
                        x1_tr = tr_val[i + 1]

                        y0_z0_tr1, y0_z1_tr1 = find_value(press, x0_tr,
                                                          pr_val, tr_val,
                                                          val_z0, val_z1)
                        y1_z0_tr1, y1_z1_tr1 = find_value(press, x1_tr,
                                                          pr_val, tr_val,
                                                          val_z0, val_z1)
                        break
                else:
                    return float('NaN'), float('NaN')

            z0 = ((y1_z0_tr1 - y0_z0_tr1) * (temp - x0_tr) / (x1_tr - x0_tr)
                   + y0_z0_tr1)
            z1 = ((y1_z1_tr1 - y0_z1_tr1) * (temp - x0_tr) / (x1_tr - x0_tr)
                   + y0_z1_tr1)

            return z0, z1

        # Pr and Tr values are in table
        print "pr and tr are in table ", tr_index, pr_index
        return (val_z0[tr_index][pr_index], val_z1[tr_index][pr_index])
        #return (val_z0[tr_z0_index][pr_z0_index],
                #val_z1[tr_z1_index][pr_z1_index])


def find_value_pressinter(pr, tr, pr_val, tr_val, val_z0, val_z1):
    press = float(pr)
    temp = float(tr)

    if temp > 1.1 and press < 1:
        return float('NaN'), float('NaN')
    elif temp > 1.5 and press > 1:
        return float('NaN'), float('NaN')
    else:
        try:
            pr_index = pr_val.index(press)
        except ValueError, e:
            try:
                tr_index = tr_val.index(temp)

                # Tr value is in table, Pr is not
                for i in range (0, len(pr_val) - 1):
                    if pr_val[i] <= press:
                        if pr_val[i + 1] < press and i == len(pr_val) - 2:
                            return float('NaN'), float('NaN')
                        elif pr_val[i + 1] < press:
                            continue
                        else:
                            x0_pr = pr_val[i]
                            x1_pr = pr_val[i + 1]

                            y0_z0_pr1, y0_z1_pr1 = find_value_pressinter(x0_pr,
                                                       temp, pr_val, tr_val,
                                                       val_z0, val_z1)
                            y1_z0_pr1, y1_z1_pr1 = find_value_pressinter(x1_pr,
                                                       temp, pr_val, tr_val,
                                                       val_z0, val_z1)
                            break
                    else:
                        return float('NaN'), float('NaN')
                z0 = ((y1_z0_pr1 - y0_z0_pr1) * (press - x0_pr) / (x1_pr - x0_pr)
                       + y0_z0_pr1)
                z1 = ((y1_z1_pr1 - y0_z1_pr1) * (press - x0_pr) / (x1_pr - x0_pr)
                       + y0_z1_pr1)

                return z0, z1
            except ValueError, e:
                # Pr and Tr are not in table
                for i in range (0, len(tr_val) - 1):
                    if tr_val[i] <= temp:
                        if tr_val[i + 1] < temp and i == len(tr_val) - 2:
                            return float('NaN'), float('NaN')
                        elif tr_val[i + 1] < temp:
                            continue
                        else:
                            x0_tr = tr_val[i]
                            x1_tr = tr_val[i + 1]
                            break
                    else:
                        return float('NaN'), float('NaN')
                for i in range (0, len(pr_val) - 1):
                    if pr_val[i] <= press:
                        if pr_val[i + 1] < press and i == len(pr_val) - 2:
                            return float('NaN'), float('NaN')
                        elif pr_val[i + 1] < press:
                            continue
                        else:
                            x0_pr = pr_val[i]
                            x1_pr = pr_val[i + 1]

                            y0_z0_pr1, y0_z1_pr1 = find_value_pressinter(x0_pr,
                                                      x0_tr, pr_val, tr_val,
                                                      val_z0, val_z1)
                            y1_z0_pr1, y1_z1_pr1 = find_value_pressinter(x1_pr,
                                                      x0_tr, pr_val, tr_val,
                                                      val_z0, val_z1)
                            y0_z0_pr2, y0_z1_pr2 = find_value_pressinter(x0_pr,
                                                      x1_tr, pr_val, tr_val,
                                                      val_z0, val_z1)
                            y1_z0_pr2, y1_z1_pr2 = find_value_pressinter(x1_pr,
                                                      x1_tr, pr_val, tr_val,
                                                      val_z0, val_z1)
                            break
                    else:
                        return float('NaN'), float('NaN')

                z0_1 = ((y1_z0_pr1 - y0_z0_pr1) * (press - x0_pr) /
                        (x1_pr - x0_pr) + y0_z0_pr1)
                z1_1 = ((y1_z1_pr1 - y0_z1_pr1) * (press - x0_pr) /
                        (x1_pr - x0_pr) + y0_z1_pr1)

                z0_2 = ((y1_z0_pr2 - y0_z0_pr2) * (press - x0_pr) /
                        (x1_pr - x0_pr) + y0_z0_pr2)
                z1_2 = ((y1_z1_pr2 - y0_z1_pr2) * (press - x0_pr) /
                        (x1_pr - x0_pr) + y0_z1_pr2)

                z0_3 = ((z0_2 - z0_1) * (temp - x0_tr) /
                        (x1_tr - x0_tr) + z0_1)
                z1_3 = ((z1_2 - z1_1) * (temp - x0_tr) /
                        (x1_tr - x0_tr) + z1_1)

                return float(z0_3), float(z1_3)
        try:
            tr_index = tr_val.index(temp)
        except ValueError, e:
            # Pr value in table, Tr is not
            for i in range (0, len(tr_val) - 1):
                if tr_val[i] <= temp:
                    if tr_val[i + 1] < temp and i == len(tr_val) - 2:
                        return float('NaN'), float('NaN')
                    elif tr_val[i + 1] < temp:
                        continue
                    else:
                        x0_tr = tr_val[i]
                        x1_tr = tr_val[i + 1]

                        y0_z0_tr1, y0_z1_tr1 = find_value_pressinter(press,
                                                      x0_tr, pr_val, tr_val,
                                                      val_z0, val_z1)
                        y1_z0_tr1, y1_z1_tr1 = find_value_pressinter(press,
                                                      x1_tr, pr_val, tr_val,
                                                      val_z0, val_z1)

                        break
                else:
                    return float('NaN'), float('NaN')
            z0 = ((y1_z0_tr1 - y0_z0_tr1) * (temp - x0_tr) / (x1_tr - x0_tr)
                   + y0_z0_tr1)
            z1 = ((y1_z1_tr1 - y0_z1_tr1) * (temp - x0_tr) / (x1_tr - x0_tr)
                   + y0_z1_tr1)

            return z0, z1
        # Pr and Tr values are in table
        return (val_z0[tr_index][pr_index], val_z1[tr_index][pr_index])


def temp_inter():
    pr_index = None

    try:
        pr_index = pr_val.index(press)
    except ValueError, e:
        for i in range (0, len(pr_val) - 1):
            if pr_val[i] < press:
                if pr_val[i + 1] < press:
                    if i == len(pr_val) - 2:
                        return float('NaN')
                    else:
                        continue
                else:
                    break
            else:
                return float('NaN')

    answer = []
    z_list = []

    if pr_index != None:
        print len(val_z1), val_z1
        for i in range(0, len(val_z1)):
            z_list.append(val_z0[i][pr_index] + acentric *
                          val_z1[i][pr_index])
            smallest_diff = nsmallest(2, z_list, key = lambda x:
                                      abs(x - float(z)))
            #print tr_z0[i], (val_z0[i][pr_z0_index] + acentric *
                          #val_z1[i][pr_z1_index])
            #print z_list
            #print smallest_diff
            #print pr_z0_index
            #print i, val_z0[i][pr_z0_index] + acentric * val_z1[i][pr_z1_index]
            if abs(val_z0[i][pr_index] + acentric * val_z1[i][pr_index] -
                   float(z)) < 0.0001:
                answer.append(tr_val[i])
                continue
            else:
                if len(smallest_diff) == 2:
                    x0 = tr_val[z_list.index(smallest_diff[0])]
                    x1 = tr_val[z_list.index(smallest_diff[1])]
                    y0 = smallest_diff[0]
                    y1 = smallest_diff[1]

                    if y0 == y1:
                        continue
                    else:
                        x = (x1 - x0) * (float(z) - y0) / (y1 - y0) + x0

                        calc_z0, calc_z1, calc_z = calculate_z(cr_temp, cr_pressure,
                                                              acentric, x, pressure)
                        if x < 0.3 or x > 1.5:
                            continue
                        elif abs(float(z) - calc_z) > 0.00001:
                            continue
                        else:
                            add_answer = True
                            # print answer
                            for i in range (0, len(answer)):
                                if abs(answer[i] - x) < 0.001:
                                    add_answer = False
                                    # print answer[i], x
                                    break
                                else:
                                    continue
                            if add_answer:
                                answer.append(x)
                                z_list[z_list.index(smallest_diff[0])] = float('NaN')
                                z_list[z_list.index(smallest_diff[1])] = float('NaN')
                            else:
                                continue

                else:
                    continue
    else:
        for i in range(0, len(val_z1)):
            #print "Length", i, len(z_list), len(tr_z0)
            z0, z1 = find_value(press, tr_val[i], pr_val, tr_val, val_z0, val_z1)

            z_list.append(z0 + acentric * z1)
            #print tr_z0[i], z_list[len(z_list) - 1]
            smallest_diff = nsmallest(2, z_list, key = lambda x: abs(x - float(z)))
            #print float(z0) + acentric * float(z1), z
            #print "\t", float(z0) + acentric * float(z1) - z
            if abs(float(z0) + acentric * float(z1) - float(z)) < 0.0001:
                answer.append(tr_val[i])
                continue
            else:
                if len(smallest_diff) == 2:
                    x0 = tr_val[z_list.index(min(smallest_diff))]
                    #print "*", smallest_diff
                    x1 = tr_val[z_list.index(max(smallest_diff))]
                    y0 = min(smallest_diff)
                    y1 = max(smallest_diff)

                    if y0 == y1:
                        continue

                    x = (x1 - x0) * (float(z) - y0) / (y1 - y0) + x0
                    #print "x: ", x
                    calc_z0, calc_z1, calc_z = calculate_z(cr_temp, cr_pressure,
                                                           acentric, x, pressure)
                    #print z, calc_z, abs(float(z) - calc_z)
                    if x < 0.3 or x > 1.5:
                        # print x
                        #return float('NaN')
                        continue
                    elif abs(float(z) - calc_z) > 0.00001:
                        continue
                    else:
                        add_answer = True
                        for i in range (0, len(answer)):
                            if abs(answer[i] - x) < 0.001:
                                add_answer = False
                                break
                            else:
                                continue
                        if add_answer:
                            answer.append(x)
                            z_list[z_list.index(smallest_diff[0])] = float('NaN')
                            z_list[z_list.index(smallest_diff[1])] = float('NaN')
                        else:
                            continue
    return format_answer(answer)


def pressure_inter():
    tr_index = None

    try:
        tr_index = tr_val.index(temp)
    except ValueError, e:
        for i in range (0, len(tr_val) - 1):
            if tr_val[i] < temp:
                if  tr_val[i + 1] < temp:
                    if i == len(tr_val) - 2:
                        return float('NaN')
                    else:
                        continue
                else:
                    break
            else:
                return float('NaN')

    answer = []
    z_list = []

    if tr_index != None:
        if  tr_index > 22:
            start = 7
        else:
            start = 0

        #print len(val_z1[0]), val_z1[0]
        for i in range(start, len(val_z1[0])):
            z_list.append(val_z0[tr_index][i] + acentric *
                          val_z1[tr_index][i])
            smallest_diff = nsmallest(2, z_list, key = lambda x:
                                      abs(x - float(z)))

            #print z_list
            #print smallest_diff

            if abs(val_z0[tr_index][i] + acentric * val_z1[tr_index][i] -
                   float(z)) < 0.0001:
                add_answer = True

                for j in range (0, len(answer)):
                    if abs(answer[j] - x) < 0.1:
                        add_answer = False
                        break
                    else:
                        continue

                if add_answer:
                    answer.append(pr_val[i])
                else:
                    continue
            else:
                if len(smallest_diff) == 2:
                    for x in range(0, len(z_list)):
                        if abs(z_list.index(smallest_diff[0]) -
                           z_list.index(smallest_diff[1])) != 1:
                            index1 = z_list.index(smallest_diff[0])
                            index2 = z_list.index(smallest_diff[1])
                            z_list[min(index1, index2)] = 0 #float('NaN')
                            smallest_diff = nsmallest(2, z_list, key = lambda x:
                                                      abs(x - float(z)))

                    if tr_index > 22:
                        x0 = pr_val[z_list.index(smallest_diff[0]) + 7]
                        x1 = pr_val[z_list.index(smallest_diff[1]) + 7]
                    else:
                        x0 = pr_val[z_list.index(smallest_diff[0])]
                        x1 = pr_val[z_list.index(smallest_diff[1])]

                    y0 = smallest_diff[0]
                    y1 = smallest_diff[1]

                    if y0 == y1:
                        continue
                    else:
                        x = (x1 - x0) * (float(z) - y0) / (y1 - y0) + x0

                        calc_z0, calc_z1, calc_z = calculate_z(cr_temp, cr_pressure,
                                                              acentric, temp, x)
                        #print "x: ", x, "z: ", z, abs(float(z) - calc_z)
                        if x < 0.01 or x > 10 or x == float('NaN'):
                            continue
                        elif abs(float(z) - calc_z) > 0.0001:
                            continue
                        else:
                            add_answer = True
                            if tr_index > 22 and x < 1:
                                add_answer = False
                            for j in range (0, len(answer)):
                                if abs(answer[j] - x) < 0.1:
                                    add_answer = False
                                    # print answer[i], x
                                    break
                                else:
                                    continue
                            if add_answer:
                                answer.append(x)
                                #print "answer added", x
                                z_list[z_list.index(smallest_diff[0])] = 0
                                z_list[z_list.index(smallest_diff[1])] = 0
                            else:
                                continue

                else:
                    continue
    else:
        for i in range(0, len(val_z1[0])):
            # print "Length", i, len(z_list), len(tr_z0)
            z0, z1 = find_value(pr_val[i], temp, pr_val, tr_val,
                                val_z0, val_z1)

            # print temp, pr_val[i], z0, z1

            z_list.append(z0 + acentric * z1)
            # print pr_val[i], z_list[len(z_list) - 1]
            smallest_diff = nsmallest(2, z_list, key = lambda x:
                                      abs(x - float(z)))
            #print z_list
            #print smallest_diff
            #print float(z0) + acentric * float(z1), z
            #print float(z0) + acentric * float(z1) - z
            if abs(float(z0) + acentric * float(z1) - float(z)) < 0.0001:
                add_answer = True
                for j in range (0, len(answer)):
                    if abs(answer[j] - x) < 0.1:
                        add_answer = False
                        break
                    else:
                        continue

                if add_answer:
                    answer.append(pr_val[i])
                else:
                    continue
            else:
                if len(smallest_diff) == 2:
                    if abs(z_list.index(smallest_diff[0]) -
                           z_list.index(smallest_diff[1])) != 1:
                        index1 = z_list.index(smallest_diff[0])
                        index2 = z_list.index(smallest_diff[1])
                        z_list[min(index1, index2)] = 0 #float('NaN')
                        #z_list[z_list.index(smallest_diff[1])] = float('NaN')
                        smallest_diff = nsmallest(2, z_list, key = lambda x:
                                                  abs(x - float(z)))
                    x0 = pr_val[z_list.index(min(smallest_diff))]
                    #print "*", smallest_diff
                    x1 = pr_val[z_list.index(max(smallest_diff))]
                    y0 = min(smallest_diff)
                    y1 = max(smallest_diff)

                    if y0 == y1:
                        continue

                    x = (x1 - x0) * (float(z) - y0) / (y1 - y0) + x0
                    #print "x: ", x
                    calc_z0, calc_z1, calc_z = calculate_z(cr_temp, cr_pressure,
                                                           acentric, temp, x)
                    # z_list[z_list.index(smallest_diff[1])] = float('NaN')
                    #print "**", z, x, calc_z, abs(float(z) - calc_z)
                    if x < 0.01 or x > 10:
                        # print x
                        # return float('NaN')
                        continue
                    elif abs(float(z) - calc_z) > 0.006:
                        continue
                    else:
                        add_answer = True

                        if temp > 1.1 and x < 1:
                            add_answer = False

                        for i in range (0, len(answer)):
                            if abs(answer[i] - x) < 0.1:
                                add_answer = False
                                break
                            else:
                                continue
                        if add_answer:
                            answer.append(x)

                            z_list[z_list.index(smallest_diff[0])] = 0
                            z_list[z_list.index(smallest_diff[1])] = 0
                        else:
                            continue
    return format_answer(answer)
