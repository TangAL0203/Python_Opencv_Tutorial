#-*-coding:utf-8-*-
import matplotlib.pyplot as plt  

overall_top3_recall = {'part_details_of_clothes': 0.44520560358107253, 'fitness_of_clothes': 0.7388310082994879, 'graphic_elements_texture': 0.48681268087345436, 'style_of_clothes': 0.5004896560166483, 'type_of_collars': 0.9098014466721686, 'fabric_of_clothes': 0.6668895507871861, 'type_of_dresses': 0.4852532427424336, 'type_of_sleeves': 0.917098097223156, 'length_of_trousers': 0.8732394366197183, 'design_of_dresses': 0.5742441637964026, 'type_of_trousers': 0.8888888888888888, 'thickness_of_clothes': 0.9991319444444444, 'type_of_waistlines': 0.8452077048038988, 'length_of_dresses': 0.8435674500747181, 'length_of_sleeves': 0.8601542641774038, 'type_of_clothes_buttons': 0.7750806314717366, 'length_of_upper_body_clothes': 0.9302811021430559}
overall_top5_recall = {'part_details_of_clothes': 0.523025063882999, 'fitness_of_clothes': 1.0, 'graphic_elements_texture': 0.6291107603262299, 'style_of_clothes': 0.6766740115069164, 'type_of_collars': 0.9688819845623574, 'fabric_of_clothes': 0.7874901221810224, 'type_of_dresses': 0.6792773316862261, 'type_of_sleeves': 0.9552208700329456, 'length_of_trousers': 1.0, 'design_of_dresses': 0.8378300803673938, 'type_of_trousers': 0.9466666666666667, 'thickness_of_clothes': 1.0, 'type_of_waistlines': 0.9675098630772802, 'length_of_dresses': 1.0, 'length_of_sleeves': 0.953457796476466, 'type_of_clothes_buttons': 0.9679171617721949, 'length_of_upper_body_clothes': 1.0}
  
top3_name_list = [name for name in overall_top3_recall.keys()]
top5_name_list = [name or name in overall_top5_recall.keys()]

top3_num_list = [overall_top3_recall[name] for name in overall_top3_recall.keys()]
top5_num_list = [overall_top5_recall[name] for name in overall_top5_recall.keys()]


# plt.bar(range(len(top3_num_list)), top3_num_list,color='rgb',tick_label=top3_name_list)
# plt.xticks(rotation=-45)
# plt.show()

plt.bar(range(len(top5_num_list)), top5_num_list,color='rgb',tick_label=top5_name_list)
plt.xticks(rotation=65)
plt.show()
