# import xml.etree.ElementTree as ET
# from datetime import datetime

# xml_file ="consolidated_report.xml"
# tree = ET.parse(xml_file)
# root = tree.getroot()
# data={}

# def formated_text(text,condition):
#     return f"[{text}]" if condition else str(text)

# for suite in root.findall('.//suite/suite'):
#     status_element = suite.find('./status')
#     status = status_element.get('status') if status_element is not None else 'N/A'
#     end_time=status_element.get('endtime')
#     specified_date = datetime.strptime(end_time, "%Y%m%d %H:%M:%S.%f")
#     current_time = datetime.now()
#     time_difference = current_time - specified_date
#     hours_difference = int(time_difference.total_seconds() // 3600)
#     if hours_difference>8:
#         hours='*('+str(hours_difference)+ ' hours ago)'
#     else:
#         hours=None
#     all_test_element=suite.findall('./test')
#     status_critical='none'
#     for test in all_test_element:
#         status_element = test.find('./status')
#         status_test=status_element.get('status')
#         if status_test=='FAIL':
#             tag_elements = test.findall('tag')
#             tags=set(map(lambda tag_element: tag_element.text, tag_elements))
#             if 'non-critical'  in tags:
#                 status_critical='non-critical'
#             else:
#                 status_critical='critical'
#     tag_elements=suite.findall('.//tag')
#     tag_texts = set(map(lambda tag_element: tag_element.text, tag_elements))
#     condition = lambda x: x in tags
#     formated_string = ', '.join(formated_text(item, condition(item)) for item in tag_texts) if tag_texts else suite.get('name')
#     if status_critical!='none':
#         status+='('+status_critical+')'
#     data[formated_string]=status+hours
# with open('Status_suites.txt','w') as file:
#     for key, value in data.items():
#         file.write(f'{key: <60} {value}\n')



import xml.etree.ElementTree as ET
from datetime import datetime

xml_file ="consolidated_report.xml"
tree = ET.parse(xml_file)
root = tree.getroot()
data={}

def formated_text(text,condition):
    return f"[{text}]" if condition else str(text)

for tests in root.findall('.//test'):
    test_id=tests.get('id')
    status_element = tests.find('./status')
    status = status_element.get('status') if status_element is not None else 'N/A'
    end_time=status_element.get('endtime')
    if end_time!='N/A':
        specified_date = datetime.strptime(end_time, "%Y%m%d %H:%M:%S.%f")
        current_time = datetime.now()
        time_difference = current_time - specified_date
        hours_difference = int(time_difference.total_seconds() // 3600)
        if hours_difference>8:
            hours='*('+str(hours_difference)+ ' hours ago)'
        else:
            hours=''
    tags=tests.findall('./tag')
    status_critical='none'
    tag_texts = set(map(lambda tag_element: tag_element.text, tags))
    if 'non-critical' in tag_texts:
        status_critical='non-critical'
    else:
        status_critical='critical'

    status+='('+status_critical+')'+hours
    tags_status={}
    for tag in tag_texts:
        tags_status[test_id]=status
        if tag in data:
            data[tag].update(tags_status)
        else:
            data[tag]=tags_status
with open('Status_suites.txt','w') as file:
    for key, val in data.items():
        if len(val)==1:
            final_status=list(val.values())[0]
        else:
            final_status=val
        file.write(f'{key: <60} {final_status}\n')

