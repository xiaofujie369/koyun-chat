from collections import defaultdict
from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.visitor_connections: dict[tuple[str, str], set[WebSocket]] = defaultdict(set)
        self.dashboard_connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect_visitor(self, site_key: str, visitor_uid: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.visitor_connections[(site_key, visitor_uid)].add(websocket)

    def disconnect_visitor(self, site_key: str, visitor_uid: str, websocket: WebSocket) -> None:
        connections = self.visitor_connections.get((site_key, visitor_uid))
        if not connections:
            return
        connections.discard(websocket)
        if not connections:
            self.visitor_connections.pop((site_key, visitor_uid), None)

    async def connect_dashboard(self, site_id: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.dashboard_connections[str(site_id)].add(websocket)

    def disconnect_dashboard(self, site_id: UUID, websocket: WebSocket) -> None:
        connections = self.dashboard_connections.get(str(site_id))
        if not connections:
            return
        connections.discard(websocket)
        if not connections:
            self.dashboard_connections.pop(str(site_id), None)

    async def send_to_visitor(self, site_key: str, visitor_uid: str, payload: dict) -> None:
        stale: list[WebSocket] = []
        for websocket in self.visitor_connections.get((site_key, visitor_uid), set()):
            try:
                await websocket.send_json(payload)
            except RuntimeError:
                stale.append(websocket)
        for websocket in stale:
            self.disconnect_visitor(site_key, visitor_uid, websocket)

    async def broadcast_dashboard(self, site_id: UUID, payload: dict) -> None:
        stale: list[WebSocket] = []
        for websocket in self.dashboard_connections.get(str(site_id), set()):
            try:
                await websocket.send_json(payload)
            except RuntimeError:
                stale.append(websocket)
        for websocket in stale:
            self.disconnect_dashboard(site_id, websocket)


manager = ConnectionManager()
