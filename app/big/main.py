from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import data_process as dp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Twitch可视化后端")
# 解决跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 静态文件挂载
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/api/stats")
async def api_stats():
    return dp.get_global_stats()
@app.get("/api/scatter")
async def api_scatter(lang: str = "all", channel: str = ""):
    df = dp.load_and_clean_data()
    # 语言过滤逻辑
    if lang != "all":
        df = df[df["Language"] == lang]

    # 主播名称过滤（柱状图点击联动）
    if channel:
        df = df[df["Channel"] == channel]

    # 组装返回数据
    data_list = []
    for _, row in df.iterrows():
        data_list.append({
            "stream_time": int(row["Stream time(minutes)"]),
            "avg_viewers": int(row["Average viewers"]),
            "partnered": bool(row["Partnered"]),
            "channel": row["Channel"]
        })
    return {"data": data_list}
# 基础图表接口
@app.get("/api/top20")
async def api_top20():
    return {"data": dp.get_top20_streamers()}

@app.get("/api/lang_count")
async def api_lang_count():
    return {"data": dp.get_language_count()}



@app.get("/api/lang_avg_view")
async def api_lang_avg_view():
    return {"data": dp.get_lang_avg_viewer()}

# 高阶附加接口
@app.get("/api/correlation")
async def api_corr():
    return dp.get_corr_data()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)