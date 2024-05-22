import streamlit as st

# Set page layout to wide
# st.set_page_config(layout="wide")

def determine_grade(ratings):
    # Level 1 determination logic
    if all(rating in ['低关注度', '数据缺失（DG）'] for category in ratings for rating in ratings[category].values()):
        return '1级'
    else:
        # Level 4 determination logic
        if any(rating == '高关注度' for rating in ratings['健康危害I组危害终点'].values()):
            return '4级'
        else:
            if any(rating == '极高关注度' for category in ['健康危害II组危害终点', '生态毒性危害终点'] for rating in ratings[category].values()):
                if any(rating == '极高关注度' for rating in ratings['环境归趋危害终点'].values()):
                    return '4级'
                else:
                    if ratings['环境归趋危害终点'].get('持久性', '低关注度') == '高关注度':
                        if (ratings['环境归趋危害终点'].get('生物蓄积性', '低关注度') == '高关注度' or
                                ratings['环境归趋危害终点'].get('迁移性', '低关注度') == '高关注度'):
                            return '4级'
                        else:
                            return '3级'
                    else:
                        return '3级'
            else:
                if ratings['环境归趋危害终点'].get('持久性', '低关注度') == '极高关注度':
                    if (ratings['环境归趋危害终点'].get('生物蓄积性', '低关注度') == '极高关注度' or
                            ratings['环境归趋危害终点'].get('迁移性', '低关注度') == '极高关注度'):
                        return '4级'
                    else:
                        # Level 3 determination logic
                        if (any(rating == '中关注度' for rating in ratings['健康危害I组危害终点'].values()) or
                            any(rating == '高关注度' for rating in ratings['环境影响危害终点'].values())):
                            return '3级'
                        else:
                            if (any(rating == '高关注度' or rating == '中关注度' for category in ['健康危害II组危害终点', '生态毒性危害终点'] for rating in ratings[category].values())):
                                return '3级'
                            else:
                                if (ratings['环境归趋危害终点'].get('生物蓄积性', '低关注度') == '高关注度' or
                                        ratings['环境归趋危害终点'].get('迁移性', '低关注度') == '高关注度'):
                                    return '3级'
                                else:
                                    return '2级'
                else:
                    if (any(rating == '中关注度' for rating in ratings['健康危害I组危害终点'].values()) or
                        any(rating == '高关注度' for rating in ratings['环境影响危害终点'].values())):
                        return '3级'
                    else:
                        if (any(rating == '高关注度' or rating == '中关注度' for category in ['健康危害II组危害终点', '生态毒性危害终点'] for rating in ratings[category].values())):
                            if any(rating == '高关注度' for rating in ratings['环境归趋危害终点'].values()):
                                return '3级'
                            else:
                                if (ratings['环境归趋危害终点'].get('生物蓄积性', '低关注度') == '极高关注度' or
                                        ratings['环境归趋危害终点'].get('迁移性', '低关注度') == '极高关注度' or
                                        ratings['环境归趋危害终点'].get('生物蓄积性', '低关注度') == '高关注度' or
                                        ratings['环境归趋危害终点'].get('迁移性', '低关注度') == '高关注度'):
                                    return '3级'
                                else:
                                    return '2级'
                        else:
                            if (ratings['环境归趋危害终点'].get('生物蓄积性', '低关注度') == '极高关注度' or
                                    ratings['环境归趋危害终点'].get('迁移性', '低关注度') == '极高关注度' or
                                    ratings['环境归趋危害终点'].get('生物蓄积性', '低关注度') == '高关注度' or
                                    ratings['环境归趋危害终点'].get('迁移性', '低关注度') == '高关注度'):
                                if (any(rating == '高关注度' or rating == '中关注度' for category in ['健康危害II组危害终点', '生态毒性危害终点'] for rating in ratings[category].values())):
                                    return '3级'
                                else:
                                    return '2级'
                            else:
                                return '2级'


def adjust_grade_for_dg(grade, ratings):
    # Adjust grade based on DG logic
    if grade == '1级':
        if any(rating == '数据缺失（DG）' for category in ratings for rating in ratings[category].values()):
            grade = '2级DG'
    elif grade == '2级':
        if any(ratings[category].get(endpoint, '低关注度') == '数据缺失（DG）' for category in ratings for endpoint in [
            '致癌性', '致突变性', '生殖毒性', '发育毒性', '急性水生生物毒性',
            '慢性水生生物毒性', '持久性', '生物蓄积性', '迁移性', '消耗臭氧层效应',
            '温室效应'
        ]):
            grade = '3级DG'
        elif (ratings['健康危害II组危害终点'].get('呼吸道致敏性', '低关注度') == '数据缺失（DG）' and
              ratings['健康危害II组危害终点'].get('皮肤致敏性', '低关注度') == '数据缺失（DG）'):
            grade = '3级DG'
        elif sum(1 for endpoint in [
            '急性毒性', '器官毒性', '神经毒性', '皮肤刺激性', '严重眼损伤、眼部刺激性'
        ] if ratings['健康危害II组危害终点'].get(endpoint, '低关注度') == '数据缺失（DG）') > 1:
            grade = '3级DG'
    elif grade == '3级':
        if any(ratings[category].get(endpoint, '低关注度') == '数据缺失（DG）' for category in ratings for endpoint in [
            '致癌性', '致突变性', '持久性', '消耗臭氧层效应', '温室效应'
        ]):
            grade = '4级DG'
        elif any(all(ratings[category].get(endpoint, '低关注度') == '数据缺失（DG）' for category in ratings  for endpoint in pair) for pair in [
            ('生殖毒性', '发育毒性'), ('呼吸道致敏性', '皮肤致敏性'),
            ('皮肤刺激性', '严重眼损伤、眼部刺激性'),
            ('急性水生生物毒性', '慢性水生生物毒性'),
            ('生物蓄积性', '迁移性')
        ]):
            grade = '4级DG'
        elif sum(1 for endpoint in [
            '急性毒性', '器官毒性', '神经毒性'
        ] if ratings['健康危害II组危害终点'].get(endpoint, '低关注度') == '数据缺失（DG）') > 1:
            grade = '4级DG'
    return grade


# Generate the image path based on the endpoint name
def get_image_path(endpoint_name):
    return f"pic/{endpoint_name}.png"


def get_color(grade):
    if '1级' in grade:
        return "green"
    elif '3级' in grade or '4级' in grade:
        return "red"
    else:
        return "orange"

# Page title
st.title('化学物质绿色分级评估系统')
st.caption('（Green Classification Assessment System for Chemicals, GCAS）')
# Hazard endpoints list
endpoints = {
    '健康危害I组危害终点': ['致癌性', '致突变性', '生殖毒性', '发育毒性', '内分泌干扰活性'],
    '健康危害II组危害终点': ['急性毒性', '器官毒性', '神经毒性', '呼吸道致敏性', '皮肤致敏性', '皮肤刺激性', '严重眼损伤、眼部刺激性'],
    '生态毒性危害终点': ['急性水生生物毒性', '慢性水生生物毒性'],
    '环境归趋危害终点':['持久性', '生物蓄积性', '迁移性'],
    '环境影响危害终点': ['消耗臭氧层效应', '温室效应', '生产过程碳排放量']
}

# Rating options
rating_options_full = ['低关注度', '中关注度', '高关注度', '极高关注度','数据缺失（DG）']
rating_options_reduced = ['低关注度', '中关注度', '高关注度','数据缺失（DG）']

# Store user ratings in a dictionary
ratings = {}

# Create rating interface for each hazard endpoint
for category, endpoints_list in endpoints.items():
    # cols = st.columns([1, 1, 1])
    # with cols[1]:
    #     st.subheader(category)
    for endpoint in endpoints_list:
        # Use columns to center the options
        label_html = f""" <div style="font-size:20px; margin-bottom:0px;"> {endpoint} </div> """
        st.markdown(label_html, unsafe_allow_html=True)

        if endpoint in ['致癌性', '致突变性', '生殖毒性', '发育毒性', '内分泌干扰活性', '皮肤刺激性', '严重眼损伤、眼部刺激性', '消耗臭氧层效应', '温室效应', '生产过程碳排放量']:
            cols = st.columns([1, 5, 1])
            with cols[1]:
                selected_rating = st.radio("", rating_options_reduced, horizontal=True, key=f'{category}_{endpoint}')
        else:
            cols = st.columns([1, 15, 1])
            with cols[1]:
                selected_rating = st.radio("", rating_options_full, horizontal=True, key=f'{category}_{endpoint}')
        # Update dictionary to store ratings
        if category not in ratings:
            ratings[category] = {}
        ratings[category][endpoint] = selected_rating
        image_path = get_image_path(endpoint)
        if image_path:
            st.image(image_path, use_column_width=True)
        st.divider()
# Submit button
# Submit button
if st.button('提交评级'):
    chemical_grade = determine_grade(ratings)
    adjust_chemical_grade = adjust_grade_for_dg(chemical_grade,ratings)
    color = get_color(adjust_chemical_grade)
    cols = st.columns([1, 3, 1])
    with cols[1]:
        st.markdown(f'<h3 style="color: {color};">该化学物质的原绿色分级为: {chemical_grade}</h3>', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: {color};">该化学物质的修正后绿色分级为: {adjust_chemical_grade}</h3>', unsafe_allow_html=True)


