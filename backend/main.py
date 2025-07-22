from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 允许前端访问（重要！）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储交易数据的内存列表
trades_storage = []

# 交易数据格式
class Trade(BaseModel):
    commodity: str   # 商品名称
    type: str        # 类型：Buy/Sell
    quantity: float  # 数量
    price: float     # 价格

# 添加新交易
@app.post("/trades")
async def create_trade(trade: Trade):
    print(f"接收到交易数据：{trade.dict()}")  # 新增日志
    trades_storage.append(trade.dict())
    return trade

# 获取所有交易（含名义价值计算）
@app.get("/trades")
async def get_trades():
    trades_with_value = []
    for trade in trades_storage:
        # 计算名义价值 = 数量 × 价格
        trade_copy = trade.copy()
        trade_copy['notional_value'] = trade['quantity'] * trade['price']
        trades_with_value.append(trade_copy)
    return trades_with_value

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)