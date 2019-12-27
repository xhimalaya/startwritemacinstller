def main_back_space_controller():
	if(SW_global.current_axes!=None):
		if(SW_global.current_axes==guideline_axes[l]):
			if((len(SW_global.cursor_data)==0) and (len(SW_global.axes_data)>0)):
				guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
				kern_value_array.clear()
				kern_value_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"])
				SW_global.kern_list.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"])
				delete_list.clear()
				delete_list.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"])
				SW_global.letters_already_written.clear()
				SW_global.letters_already_written.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
				guideline_axes[l].lines.clear()
				guideline_axes[l].lines.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"])
				SW_global.cursor_pos.clear()
				SW_global.cursor_pos.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"])
				SW_global.cursor_data.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"])
				compositedot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["compositedot_already_applied_array"])
				startdot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_already_applied_array"])
				decisiondot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decisiondot_already_applied_array"])
				connectdot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connectdot_already_applied_array"])
				stoke_arrow_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["stoke_arrow_flag_pos"]
				decision_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decision_dot_flag_pos"]
				connect_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connect_dot_flag_pos"]
				startdot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_flag_pos"]
				SW_global.current_axes=guideline_axes[l]
				SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
				del SW_global.axes_data[str(len(SW_global.axes_data)-1)]
			elif((SW_global.current_pos==None) or((len(SW_global.cursor_pos)>0) and (SW_global.current_pos==SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))):
				delete_letter_from_end()
			else:
				current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=guideline_axes[l])
				temp=[]
				for j in range(len(delete_list)):
					if(SW_global.current_pos_in_number!=None and j!=SW_global.current_pos_in_number):
						temp.append(j)
				clear_digit_from_axes(axesdata=guideline_axes[l])
				base_line_array=[]
				for j in range(4):
					base_line_array.append(guideline_axes[l].lines[j])
				temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp,spec_axes=guideline_axes[l],baselines_objects_array=base_line_array)
				kern_value_array.clear()
				kern_value_array.extends(temp_kern_value1.copy())
				SW_global.kern_list.clear()
				SW_global.kern_list.extends(temp_kern_list1.copy())
				delete_list.clear()
				delete_list.extends(temp_delete1.copy())
				SW_global.recent_input_list.clear()
				SW_global.recent_input_list.extends(temp_recent1.copy())
				SW_global.cursor_data.clear()
				SW_global.cursor_data.extends(temp_cursor_data1)
				SW_global.cursor_pos.clear()
				SW_global.cursor_pos.extends(temp_cursor_pos1)
				SW_global.letters_already_written.clear()
				SW_global.letters_already_written.extends(letters_already_written3)
				guideline_axes[l].lines.clear()
				guideline_axes[l].lines.extends(temp_guideline_axes1.copy())
				if(SW_global.current_pos_in_number>0):
					SW_global.current_pos_in_number=SW_global.current_pos_in_number-1
					SW_global.current_pos=SW_global.cursor_pos[SW_global.current_pos_in_number]
					SW_global.current_axes=guideline_axes[l]
					### need to add cursor data #####
		else:
			temp_delete_list0=[]

			if(len(SW_global.axes_data)>0):
				key_for_axes=None
				for j in range(len(SW_global.axes_data)):
					if(SW_global.axes_data[str(j)]["axis_data"]==SW_global.current_axes):
						key_for_axes=j
						break

				if(key_for_axes!=None):
					for j in range(key_for_axes,len(SW_global.axes_data)):
						if(j==key_for_axes):
							current_pos_in_number_find(current_pos1=SW_global.current_pos,current_axes1=SW_global.axes_data[str(j)]["axis_data"])
							for i in range(len(SW_global.axes_data[str(j)]["delete_list"])):
								if(SW_global.current_pos_in_number!=i):
									temp_delete_list0.append(SW_global.axes_data[str(j)]["delete_list"][i])
						else:
							temp_delete_list0.extends(SW_global.axes_data[str(j)]["delete_list"])
				temp_delete_list0.extends(delete_list.copy())
				temp_delete_list1=divide_delete_list_with_the_base_of_max_limit3(need_array=temp_delete_list0,limit1=SW_global.max_limit)
				count1=key_for_axes
				for j in range(len(temp_delete_list1)):
					clear_digit_from_axes(axesdata=SW_global.axes_data[str(count1)]["axis_data"])
					base_array=[]
					if(count1<=len(SW_global.axes_data)-1):
						for k1 in range(4):
							base_array.append(SW_global.axes_data[str(count1)]["lines"][k1])
						temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp_delete_list1[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
						save_data_to_axes_dict(kern_value1=temp_kern_value1,delete_list1=temp_delete1,recent_input_list1=temp_recent1,cursor_pos1=temp_cursor_pos1,cursor_data1=temp_cursor_data1,axes_key_index=count1,
							letters_already_written1=letters_already_written3,axesdata=SW_global.axes_data[str(count1)]["axis_data"],lines1=temp_guideline_axes1)
						count1=count1+1
					elif(count1==len(SW_global.axes_data)):
						clear_digit_from_axes(axesdata=guideline_axes[l])
						base_array=[]
						for k1 in range(4):
							base_array.append(guideline_axes[l].lines[k1])
						temp_kern_value1,temp_kern_list1,temp_delete1,temp_recent1,temp_cursor_data1,temp_cursor_pos1,letters_already_written3,temp_guideline_axes1=add_digit_in_axes(list_of_digit=temp_delete_list1[j],spec_axes=guideline_axes[l],baselines_objects_array=base_array)
						kern_value_array.clear()
						kern_value_array.extends(temp_kern_value1.copy())
						SW_global.kern_list.clear()
						SW_global.kern_list.extends(temp_kern_list1.copy())
						delete_list.clear()
						delete_list.extends(temp_delete1.copy())
						SW_global.recent_input_list.clear()
						SW_global.recent_input_list.extends(temp_recent1.copy())
						SW_global.cursor_data.clear()
						SW_global.cursor_data.extends(temp_cursor_data1)
						SW_global.cursor_pos.clear()
						SW_global.cursor_pos.extends(temp_cursor_pos1)
						SW_global.letters_already_written.clear()
						SW_global.letters_already_written.extends(letters_already_written3)
						guideline_axes[l].lines.clear()
						guideline_axes[l].lines.extends(temp_guideline_axes1.copy())
						count1=count1+1
				if(count1<len(SW_global.axes_data)):
					guideline_axes[l].set_visible(False)
					guideline_axes[l]=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["axis_data"]
					kern_value_array.clear()
					kern_value_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_value_array"])
					SW_global.kern_list.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["kern_list"])
					delete_list.clear()
					delete_list.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["delete_list"])
					SW_global.letters_already_written.clear()
					SW_global.letters_already_written.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["letters_already_written"])
					guideline_axes[l].lines.clear()
					guideline_axes[l].lines.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["lines"])
					SW_global.cursor_pos.clear()
					SW_global.cursor_pos.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_pos"])
					SW_global.cursor_data.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["cursor_data"])
					compositedot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["compositedot_already_applied_array"])
					startdot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_already_applied_array"])
					decisiondot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decisiondot_already_applied_array"])
					connectdot_already_applied_array.extends(SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connectdot_already_applied_array"])
					stoke_arrow_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["stoke_arrow_flag_pos"]
					decision_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["decision_dot_flag_pos"]
					connect_dot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["connect_dot_flag_pos"]
					startdot_flag_pos=SW_global.axes_data[str(len(SW_global.axes_data)-1)]["startdot_flag_pos"]
					SW_global.current_axes=guideline_axes[l]
					SW_global.current_pos=SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
					del SW_global.axes_data[str(len(SW_global.axes_data)-1)]





	return




	def delete_letter_from_end():
		try:
			if(SW_global.single_click_data!=None):
				SW_global.single_click_data.set_visible(False)
			len1 = len(SW_global.letters_already_written)
			len2 = len1 - 1
			srt_loop = SW_global.letters_already_written[len2 - 1]
			end_loop = SW_global.letters_already_written[len2]
			for de1 in SW_global.cursor_data:
				de1.set_visible(False)
			for i in range(srt_loop, end_loop):
				guideline_axes[l].lines[i].set_visible(False)
			del SW_global.letters_already_written[len1-1]
			del SW_global.letters_already_written[len1-2]
			last_input_len = len(delete_list)
			last_glyph = delete_list[last_input_len - 1]
			del delete_list[last_input_len - 1]
			l12 = len(kern_value_array)
			del kern_value_array[l12 - 1]
			kern_x = SW_global.kern_list[0] - 300 - manuscript.x_max[last_glyph]
			SW_global.kern_list.insert(0, kern_x)
			if SW_global.connectdot_on_off == 1:
				len11 = len(connectdot_already_applied_array)
				last_value1 = connectdot_already_applied_array[len11 - 1]
				starting_value1 = connectdot_already_applied_array[len11 - 2]
				del connectdot_already_applied_array[len11 - 1]
				del connectdot_already_applied_array[len11 - 2]
				for i in range(starting_value1, last_value1):
					guideline_axes[l].lines[i].set_visible(False)
				connect_dot_flag_pos = connect_dot_flag_pos - 1
			if SW_global.decisiondot_on_off == 1:
				len11 = len(decisiondot_already_applied_array)
				last_value1 = decisiondot_already_applied_array[len11 - 1]
				starting_value1 = decisiondot_already_applied_array[len11 - 2]
				del decisiondot_already_applied_array[len11 - 1]
				del decisiondot_already_applied_array[len11 - 2]
				for i in range(starting_value1, last_value1):
					guideline_axes[l].lines[i].set_visible(False)
				decision_dot_flag_pos = decision_dot_flag_pos - 1
			if SW_global.stokearrow_on_off == 1:
				len11 = len(compositedot_already_applied_array)
				last_value1 = compositedot_already_applied_array[len11 - 1]
				starting_value1 = compositedot_already_applied_array[len11 - 2]
				del compositedot_already_applied_array[len11 - 1]
				del compositedot_already_applied_array[len11 - 2]
				for i in range(starting_value1, last_value1):
					guideline_axes[l].lines[i].set_visible(False)
				stoke_arrow_flag_pos = stoke_arrow_flag_pos - 1
			if SW_global.startdot_on_off == 1:
				len11 = len(startdot_already_applied_array)
				last_value1 = startdot_already_applied_array[len11 - 1]
				starting_value1 = startdot_already_applied_array[len11 - 2]
				del startdot_already_applied_array[len11 - 1]
				del startdot_already_applied_array[len11 - 2]
				for i in range(starting_value1, last_value1):
					guideline_axes[l].lines[i].set_visible(False)
				startdot_flag_pos = startdot_flag_pos - 1
			del SW_global.cursor_data[len(SW_global.cursor_data)-1]
			del SW_global.cursor_pos[len(SW_global.cursor_pos)-1]
			try:
				visible_item=SW_global.cursor_data[len(SW_global.cursor_data)-1]
			except Exception as e:
				print(e)
				pass
            if(len(SW_global.cursor_pos)>1):
                cursor_x1=list(np.full((500),SW_global.cursor_pos[len(SW_global.cursor_pos)-1]))#-manuscript.x_max[delete_list[len(delete_list)-1]]))
                cursor_y=list(np.linspace(-900,1500,500))
                plot_data=plt.plot(cursor_x1, cursor_y, color='black', linewidth=0.6, dashes=(3, 4))
                SW_global.single_click_data=plot_data[0]
                ###### Add current_curosr current_axes ##########
                SW_global.current_axes=guideline_axes[l]
                SW_global.current_pos=SW_global.cursor_pos[-1]
                print("It is changed from point 1")
                SW_global.current_pos_in_number=len(SW_global.cursor_pos)-1
            fig.canvas.draw()
		except Exception as e:
			print("Exception occur",e)
			pass
		return