"""齿轮系转速求解台 —— FastAPI 入口。

API 路由优先于静态文件挂载：
  POST /api/solve               提交轴/传动关系/已知转速，返回精确求解结果
  POST /api/gear-options        目标转速配齿：枚举一个齿数字段 1~500，逐一精确求解
  POST /api/torque-balance      理想传动转矩平衡：已知外加转矩 + 待求轴，精确求解
  POST /api/transmission-paths  传动链路追踪：最短链路总数、字典序最小链路与必经关系
  POST /api/mesh-harmonics      啮合谐波重合诊断：各关系基频 1~12 次谐波的跨关系重合
  POST /api/brake-plans         最少制动轴方案：枚举可制动轴子集，求制动轴数最少的有效方案
  POST /api/sensor-plans        测速点布设：枚举可增设测速点的轴的子集，求测点数最少的有效方案
  POST /api/safe-speed-range    输入轴安全调速区间：已知转速改可调输入，求满足各轴限速的最大安全闭区间
  其余路径                      提供前端静态页面
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .solver import (
    BrakePlansRequest,
    GearOptionsRequest,
    SafeSpeedRangeRequest,
    SensorPlansRequest,
    SolveRequest,
    TorqueBalanceRequest,
    TransmissionPathsRequest,
    brake_plans,
    gear_options,
    mesh_harmonics,
    safe_speed_range,
    sensor_plans,
    solve,
    torque_balance,
    transmission_paths,
)

app = FastAPI(title="齿轮系转速求解台", version="1.7.0")

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@app.post("/api/solve")
def api_solve(req: SolveRequest) -> dict:
    return solve(req)


@app.post("/api/gear-options")
def api_gear_options(req: GearOptionsRequest) -> dict:
    return gear_options(req)


@app.post("/api/torque-balance")
def api_torque_balance(req: TorqueBalanceRequest) -> dict:
    return torque_balance(req)


@app.post("/api/transmission-paths")
def api_transmission_paths(req: TransmissionPathsRequest) -> dict:
    return transmission_paths(req)


@app.post("/api/mesh-harmonics")
def api_mesh_harmonics(req: SolveRequest) -> dict:
    return mesh_harmonics(req)


@app.post("/api/brake-plans")
def api_brake_plans(req: BrakePlansRequest) -> dict:
    return brake_plans(req)


@app.post("/api/sensor-plans")
def api_sensor_plans(req: SensorPlansRequest) -> dict:
    return sensor_plans(req)


@app.post("/api/safe-speed-range")
def api_safe_speed_range(req: SafeSpeedRangeRequest) -> dict:
    return safe_speed_range(req)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
