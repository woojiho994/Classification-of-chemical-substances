import streamlit as st
def determine_grade(ratings):
    # 1级判断逻辑
    if all(rating == '低关注度' for category in ratings for rating in ratings[category].values()):
        return '1级'
    else:
        # 进入4级判断逻辑
        if any(rating == '高关注度' for endpoint in ratings['健康危害I组危害终点'] for rating in [ratings['健康危害I组危害终点'][endpoint]]):
            return '4级'
        else:
            # 检查II组健康危害、生态毒性和环境归趋的极高关注度
            if (any(rating == '极高关注度' for category in ['健康危害II组危害终点', '生态毒性危害终点'] for rating in ratings[category].values()) or
                any(rating == '极高关注度' for endpoint in ratings['环境影响危害终点'] for rating in [ratings['环境影响危害终点'][endpoint]])):
                return '4级'
            else:
                # 进入3级判断逻辑
                # 检查持久性、生物蓄积性和迁移性的关注度
                persistence = ratings['生态毒性危害终点'].get('持久性', '低关注度')
                bioaccumulation = ratings['生态毒性危害终点'].get('生物蓄积性', '低关注度')
                mobility = ratings['生态毒性危害终点'].get('迁移性', '低关注度')
                # 3级判断逻辑
                if (any(rating == '中关注度' for endpoint in ratings['健康危害I组危害终点'] for rating in [ratings['健康危害I组危害终点'][endpoint]]) or
                    any(rating == '高关注度' for endpoint in ratings['环境影响危害终点'] for rating in [ratings['环境影响危害终点'][endpoint]]) or
                    any(rating == '极高关注度' for category in ['健康危害II组危害终点', '生态毒性危害终点'] for rating in ratings[category].values())):
                    return '3级'
                else:
                    if ((persistence == '高关注度' and (bioaccumulation == '高关注度' or mobility == '高关注度')) or
                        (persistence == '极高关注度' and (bioaccumulation == '极高关注度' or mobility == '极高关注度'))):
                        return '3级'
                    else:
                        return '2级'
def get_color(grade):
    if grade == '1级':
        return "green"
    elif grade in ['3级', '4级']:
        return "red"
    else:
        return "orange"
# 假设ratings是从用户界面收集的评级数据
# 例如：
# ratings = {
#     '健康危害I组危害终点': {'致癌性': '低关注度'},
#     '健康危害II组危害终点': {'急性毒性': '中关注度'},
#     ...
# }

# 化学物质评级

# 页面标题
st.title('化学物质危害评级系统')

# 存储用户评级的字典
ratings = {}

# 危害终点列表
endpoints = {
    '健康危害I组危害终点': ['致癌性', '致突变性', '生殖毒性', '发育毒性', '内分泌干扰活性'],
    '健康危害II组危害终点': ['急性毒性', '器官毒性',  '神经毒性', '呼吸道致敏性', '皮肤致敏性','皮肤刺激性', '严重眼损伤/眼部刺激性'],
    '生态毒性危害终点': ['急性水生生物毒性', '慢性水生生物毒性', '持久性', '生物蓄积性', '迁移性'],
    '环境影响危害终点': ['消耗臭氧层效应', '温室效应', '生产过程碳排放量']
}

# 评级选项
rating_options = ['低关注度', '中关注度', '高关注度', '极高关注度']

# 为每个危害终点创建评级界面
for category, endpoints_list in endpoints.items():
    st.header(category)
    for endpoint in endpoints_list:
        # st.write(f'{endpoint}的评级:')
        # 使用horizontal=True将选项放在一行中
        selected_rating = st.radio(endpoint, rating_options, horizontal=True)
        # 更新字典以存储评级
        if category not in ratings:
            ratings[category] = {}
        ratings[category][endpoint] = selected_rating

# 提交按钮
# submit_button = st.button('提交评级')

# 提交后显示用户选择的评级
# if submit_button:
#     st.header('提交的评级')
#     for category, category_ratings in ratings.items():
#         st.subheader(category)
#         for endpoint, rating in category_ratings.items():
#             st.write(f'{endpoint}: {rating}')

# # 重置按钮
# reset_button = st.button('重置选项')

# # 重置用户选择的评级
# if reset_button:
#     st.experimental_reset()
    
    
chemical_grade = determine_grade(ratings)
st.warning(f'该化学物质的绿色分级为: {chemical_grade}')