def main_add_controller_for_text_flow_features(event_key=None):
    if (event_key!=None) and (SW_global.current_axes!=None):
        kw=[]
        if (SW_global.current_axes==guideline_axes[l]):
            if((SW_global.kern_list[0]>SW_global.max_limit) and((SW_global.current_pos==None) or(SW_global.current_pos>=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))):
                if event_key==" ":
                    kw.clear()
                    kw.append(event_key)
                    if(len(SW_global.axes_data)>0):
                        text_flow_main1(list1=kw,zero_axes=SW_global.axes_data[str(0)]["axis_data"],current_axes=SW_global.current_axes)
                        


    return 


def text_flow_main1(list1=None,current_axes=None,zero_axes=None):
    print("I am in text flow main1")
    print("This is list1",list1)
    print("This is current_axes",current_axes)
    print("This is zero_axes",zero_axes)
    if((list1!=None) and(current_axes!=None) and(zero_axes!=None)):
        next_axes,key=find_next_axes1(zero_axes=zero_axes)
        if(current_axes==guideline_axes[l]):
            print("check pint 234")
            print()
            check_axes=None
            if(len(SW_global.axes_data)>0):
                #check_axes=SW_global.axes_data[0]
                if(len(next_axes)>0):
                    print("check point 2")
                    change_controller(key=None,axesdata=next_axes[0])
                    print("check point 3")
                    check_axes=next_axes[0]
                    print("This is list1",list1)
                    print("Next_axes1",next_axes)
                    letter_manupulation_after_apply_text_flow(need_array=list1,next_axes1=next_axes,key_for_axes_no=key,axesdata=check_axes)
                    print("check point 4")

                else:
                    print("check point 5")
                    save_data_to_axes_dict(kern_value1=kern_value_array.copy(),delete_list1=delete_list.copy(),recent_input_list1=SW_global.recent_input_list,cursor_pos1=SW_global.cursor_pos.copy(),cursor_data1=SW_global.cursor_data.copy(),kern_list1=SW_global.kern_list,axes_key_index=None,letters_already_written1=SW_global.letters_already_written,lines1=guideline_axes[l].lines,axesdata=guideline_axes[l])
                    newCreateGuideLine(1,None,None,None,None)#createNewGuideLine(1,None,None,None,None)
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=list1.copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    kern_value_array.extend(temp_kern_value1.copy())
                    SW_global.kern_list.clear()
                    SW_global.kern_list.extend(temp_kern_list1)
                    delete_list.clear()
                    delete_list.extend(temp_delete1.copy())
                    SW_global.cursor_data.clear()
                    SW_global.cursor_data.extend(temp_cursor_data1.copy())
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.extend(temp_cursor_pos1.copy())
                    SW_global.letters_already_written.clear()
                    ### need to remove after complete
                    ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                    for k22 in range(len(letters_already_written3)):
                        letters_already_written3[k22]=letters_already_written3[k22]+3

                    SW_global.letters_already_written.extend(letters_already_written3.copy())
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    guideline_axes[l].lines.extend(temp_guideline_axes11.copy())
        #letter_manupulation_after_apply_text_flow(need_array=None,next_axes1=None,key_for_axes_no=None,axesdata=None)

            else:
                print("check point 6")
                #check_axes=next_axes[0]
                if(len(next_axes)>0):
                    check_axes=next_axes[0]
                    change_controller(key=None,axesdata=check_axes)

                    print("check axes",check_axes)
                    next_axes1,key1=find_next_axes1(zero_axes=zero_axes)
                    if(len(SW_global.axes_data)>0):
                        check_axes=SW_global.axes_data[str(0)]["axis_data"]
                    else:
                        check_axes=guideline_axes[l]
                    if(key1==None):
                        key1=0
                    print("This is check point 6 list1,next_axes1,key1_for_next_axes_no",list1,next_axes1,key1)


                    letter_manupulation_after_apply_text_flow(need_array=list1,next_axes1=next_axes1,key_for_axes_no=0,axesdata=check_axes)
                else:
                    newCreateGuideLine(1,None,None,None,None)
                    temp_kern_value11,temp_kern_list11,temp_delete11,temp_recent11,temp_cursor_data11,temp_cursor_pos11,letters_already_written31,temp_guideline_axes11=add_digit_in_axes(list_of_digit=list1.copy(),spec_axes=guideline_axes[l],baselines_objects_array=None)
                    kern_value_array.clear()
                    kern_value_array.extend(temp_kern_value11.copy())
                    delete_list.clear()
                    delete_list.extend(temp_delete11.copy())
                    SW_global.kern_list.clear()
                    SW_global.kern_list.extend(temp_kern_list11.copy())
                    SW_global.recent_input_list.clear()
                    SW_global.recent_input_list.extend(temp_recent11.copy())
                    SW_global.cursor_pos.clear()
                    SW_global.cursor_pos.extend(temp_cursor_pos11.copy())
                    SW_global.cursor_data.clear()
                    SW_global.cursor_data.extend(temp_cursor_data11.copy())
                    SW_global.letters_already_written.clear()
                    ### need to remove after complete
                    ##3 here we can use SW_globa.letter_already_written.extend(list(map(letter_already_written3,lamda X: X+4)))
                    for k22 in range(len(letters_already_written31)):
                        letters_already_written31[k22]=letters_already_written31[k22]+3

                    SW_global.letters_already_written.extend(letters_already_written31.copy())
                    while(len(guideline_axes[l].lines)>4):
                        del guideline_axes[l].lines[len(guideline_axes[l].lines)-1]
                    guideline_axes[l].lines.extend(temp_guideline_axes11.copy())


        else:
            print("I am in else part ")
            check_flag=None
            key_axes=None
            print()
            for j in range(len(SW_global.axes_data)):
                if(SW_global.axes_data[str(j)]["axis_data"]==current_axes):
                    key_axes=j
                    break
            print("This is list1",list1)
            print("This is need axes",next_axes)

            #next_axes1,key1=find_next_axes1(zero_axes=zero_axes)
            letter_manupulation_after_apply_text_flow(need_array=list1,next_axes1=next_axes,key_for_axes_no=key,axesdata=SW_global.axes_data[str(key_axes)]["axis_data"])


    return



def main_add_controller_for_text_flow_features3(event_key=None):
    global delete_list,guideline_axes
    if(SW_global.current_axes==guideline_axes[l]):
        if((SW_global.kern_list[0]>=SW_global.max_limit) and((SW_global.current_pos==None) or(SW_global.current_pos>=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))):
            ### Take all the data of current line to the dictinary and create new line and reset data
            if(event_key==" "):
                print("Normal add function need to used ")
                ### here need to add the function for change #####
                kw.clear()
                
                kw.append(event_key)
                if(len(SW_global.axes_data)>0):
                    print("check point x")

                    #### need to add new version of text flow features

                    ###text_flow_main1(list1=kw,zero_axes=SW_global.axes_data[str(0)]["axis_data"],current_axes=SW_global.current_axes)
                else:
                    print("check point y")
                    ##### need to add new version of text flow features
                    ###text_flow_main1(list1=kw,zero_axes=guideline_axes[l],current_axes=SW_global.current_axes)
                #add_any_letter_with_space_from_rear_side(event_key=event_key)
            else:
                print("Need to use speacial operation for data handaling ")
                print("delete_list :",delete_list)
                if(" " in delete_list):
                    key_from_last_word_detection=last_word_detection(axesdata=guideline_axes[l])
                    SW_global.delete_list_divide.clear()
                    temp_delete_list1=[]
                    for k5 in range(0,key_from_last_word_detection+1):
                        temp_delete_list1.append(delete_list[k5])
                    k12=temp_delete_list1.copy()
                    SW_global.delete_list_divide.append(k12)
                    temp_delete_list1.clear()
                    for j in range(key_from_last_word_detection+1,len(delete_list)):
                        temp_delete_list1.append(delete_list[j])
                    temp_delete_list1.append(event_key)
                    k13=temp_delete_list1.copy()
                    SW_global.delete_list_divide.append(k13)
                    temp_axes_list=[]
                    temp_axes_list.append(guideline_axes[l])
                    clear_digit_from_axes(axesdata=temp_axes_list[0])
                    base_array=[]
                    for j in range(4):
                        base_array.append(guideline_axes[l].lines[j])
                    # clear_digit_from_axes(axesdata=temp_axes_list[1])
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=SW_global.delete_list_divide[0],spec_axes=temp_axes_list[0],baselines_objects_array=base_array)
                    kern_value_array.clear()
                    delete_list.clear()
                    SW_global.kern_list=temp_kern_list1.copy()
                    print("temp_delete1",temp_delete1)
                    print("temp_kern_value1",temp_kern_value1)
                    reset_guide_line_delete_kern_value(temp_delete1,temp_kern_value1)
                    set_guideLine_variables(kern_value_array1=temp_kern_value1,delete_list1=temp_delete1,kern_list1=temp_kern_list1,recent1=temp_recent1,lines1=temp_guideline_axes1,cursor_pos1=temp_cursor_pos1,
                    cursor_data1=temp_cursor_data1,letters_already_written=letters_already_written3)
                    features_checking_function()
                    if(len(SW_global.axes_data)>0):
                        print("ok1")
                        ### need to add upgrade text flow main #####
                        #text_flow_main1(list1=SW_global.delete_list_divide[1],zero_axes=SW_global.axes_data[str(0)]["axis_data"],current_axes=SW_global.current_axes)
                    else:
                        print("ok2")
                        ##### need to add upgrade text flow main #####
                        #text_flow_main1(list1=SW_global.delete_list_divide[1],zero_axes=guideline_axes[l],current_axes=SW_global.current_axes)
                    #features_checking_function()
                    ###kern_value_array2,kern_list2,delete_list2,recent_input_list2,cursor_data2,cursor_pos2,letters_already_written2
                else:
                    print("Don't need to check just use normal operation ")
                    SW_global.embed_array.append(event_key)
        elif((SW_global.kern_list[0]<SW_global.max_limit) and (((SW_global.current_pos!=None) and(len(SW_global.cursor_pos)>0)) and(SW_global.current_pos<SW_global.cursor_pos[-1]))):
            print()
            SW_global.current_pos_in_number=None
            current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
            for j in range(len(delete_list)):
                if j==SW_global.current_pos_in_number:
                    delete_list.append(event_key)
            k=divide_delete_list_with_the_base_of_max_limit3(need_array=delete_list,limit1=SW_global.max_limit)
            base_array=[]
            for k1 in range(4):
                base_array.append(guideline_axes[l].lines[k1])
            temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=k[0],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
            set_guideLine_variables(kern_value_array1=temp_kern_value1,delete_list1=temp_delete1,kern_list1=temp_kern_list1,recent1=temp_recent1,lines1=temp_guideline_axes1,cursor_pos1=temp_cursor_pos1,
                    cursor_data1=temp_cursor_data1,letters_already_written=letters_already_written3)
            # if SW_global.current_pos_in_number!=None:
        else:
            if (SW_global.kern_list[0]<SW_global.max_limit)  and (((SW_global.current_pos!=None)and (len(SW_global.cursor_pos)>0)) and (SW_global.current_pos>=SW_global.cursor_pos[-1])):
                print()
                add_any_letter_with_space_from_rear_side(event_key=event_key)
    else:
        print("Here for any where on axes")
        temp_del=[]
        do_flag=0
        if SW_global.current_axes!=None:
            for j in range(len(SW_global.axes_data)):
                if SW_global.axes_data[str(j)]["axes_data"]==SW_global.current_axes:
                    do_flag=1
                    SW_global.current_pos_in_number=None
                    current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.current_axes)
                else:
                    temp_del.extend(SW_global.axes_data[str(j)]["delete_list"])    
            temp_del.extend(delete_list)
            k5=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_del,limit1=SW_global.max_limit)
            k_next=[]
            id=None
            if len(k5)>len(SW_global.axes_data)+1:
                if " " in k5[len(k5)-2]:
                    for k22 in range(k5[len(k5)-2]):
                        if " "==k5[len(k5)-2][k22]:
                            id=k22
                    k_t=k5[len(k5)-2][id:]
                    k_next.extend(k_t)
                    k_next.extend(k5[len(k5)-1])
                    k4=k5[:len(k5)-3]
                    k41=k5[len(k5)-2][:id]
                    k4.append(k41)
                    for k6 in range(len(k4)-1):
                        base_array=[(SW_global.axes_data[str(k6)]["lines"])[k7] for k7 in range(4)]
                        temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,\
                        temp_guideline_axes1=add_digit_in_axes(list_of_digit=k4[k6],spec_axes=SW_global.axes_data[str(k6)]["axis_data"],baselines_objects_array=base_array)
                        save_data_to_axes_dict(kern_value1=temp_kern_value1,delete_list1=temp_delete1,recent_input_list1=temp_recent1,cursor_pos1=temp_cursor_pos1,cursor_data1=temp_cursor_data1,axes_key_index=k6,
                        letters_already_written1=letters_already_written3,axesdata=SW_global.axes_data[str(k6)]["axis_data"],lines1=temp_guideline_axes1)
                    base_array=[guideline_axes[l].lines[k22] for k22 in range(4)]
                    temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,\
                    temp_guideline_axes1=add_digit_in_axes(list_of_digit=k4[-1],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
                    #### need to add text_flow_main with argument list as k_next

                    



                    





    return