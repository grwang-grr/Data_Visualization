import pandas as pd


def load_and_clean_data():
    # 读取csv，路径和main.py同级data文件夹
    df = pd.read_csv("./data/twitchdata-update.csv")
    # 过滤直播时长为0的脏数据
    df = df[df["Stream time(minutes)"] > 0]
    # 计算观看效率
    df["watch_efficiency"] = df["Watch time(Minutes)"] / df["Stream time(minutes)"]
    return df

# 获取观看时长前20主播
def get_top20_streamers():
    df = load_and_clean_data()
    top20 = df.sort_values("Watch time(Minutes)", ascending=False).head(20)[["Channel", "Watch time(Minutes)"]]
    return top20.to_dict("records")

# 各语言主播数量统计（饼图）
def get_language_count():
    df = load_and_clean_data()
    lang_cnt = df["Language"].value_counts().reset_index()
    lang_cnt.columns = ["name", "value"]
    return lang_cnt.to_dict("records")

# 直播时长vs平均观众 散点图数据（区分签约）
def get_scatter_data():
    df = load_and_clean_data()
    data_list = []
    for _, row in df.iterrows():
        data_list.append({
            "stream_time": row["Stream time(minutes)"],
            "avg_viewers": row["Average viewers"],
            "partnered": row["Partnered"],
            "channel": row["Channel"]
        })
    return data_list

# 各语言平均在线观众（条形图）
def get_lang_avg_viewer():
    df = load_and_clean_data()
    lang_group = df.groupby("Language")["Average viewers"].mean().reset_index()
    lang_group = lang_group.sort_values("Average viewers", ascending=False)
    return lang_group.to_dict("records")

# 相关性矩阵
def get_corr_data():
    df = load_and_clean_data()
    cols = ["Watch time(Minutes)", "Stream time(minutes)", "Peak viewers", "Average viewers", "Followers gained"]
    corr = df[cols].corr()
    data = []
    for i, col1 in enumerate(corr.index):
        for j, col2 in enumerate(corr.columns):
            data.append([i, j, round(corr.loc[col1, col2], 2)])
    return {"matrix": data, "labels": cols}
# 全局统计数据
def get_global_stats():
    df = load_and_clean_data()
    # 总主播数量：转int
    total = int(len(df))
    # 总直播时长：求和结果是numpy.int64，转int
    total_stream_time = int(df["Stream time(minutes)"].sum())
    # 总观看时长
    total_watch_time = int(df["Watch time(Minutes)"].sum())
    # 全平台平均在线观众：numpy.float64转float
    avg_viewers = float(round(df["Average viewers"].mean(), 2))
    # 签约主播占比
    partnered_num = int(df[df["Partnered"] == True].shape[0])
    partnered_pct = float(round((partnered_num / total) * 100, 2))
    return {
        "total": total,
        "totalStreamTime": total_stream_time,
        "totalWatchTime": total_watch_time,
        "avgViewers": avg_viewers,
        "partneredPct": partnered_pct
    }