import asyncio
import unittest
import os
import pyrevolt

class HTTPTests(unittest.IsolatedAsyncioTestCase):
    async def asyncTearDown(self) -> None:
        await asyncio.sleep(0)
        return await super().asyncTearDown()

    async def test_request(self) -> None:
        client: pyrevolt.HTTPClient = pyrevolt.HTTPClient()
        request: pyrevolt.Request = pyrevolt.Request(pyrevolt.Method.GET, "/")
        
        result: dict = await client.Request(request)
        self.assertEqual(result["ws"], "wss://ws.revolt.chat")
        await client.Close()

    async def test_fetch_user(self) -> None:
        client: pyrevolt.HTTPClient = pyrevolt.HTTPClient()
        user: str = "01FYEQ9FTJ62N39TGZ9P7BMCZD"
        request: pyrevolt.Request = pyrevolt.Request(pyrevolt.Method.GET, "/users/" + user)
        request.AddAuthentication(os.getenv("token"))
        
        result: dict = await client.Request(request)
        self.assertEqual(result["username"], "Fabio")
        await client.Close()

class GatewayTests(unittest.IsolatedAsyncioTestCase):
    async def test_gateway_url(self) -> None:
        gateway: pyrevolt.Gateway = pyrevolt.Gateway()
        result: dict = await gateway.GetWebsocketURL()
        self.assertEqual(result, "wss://ws.revolt.chat")
        await gateway.Close()

    async def test_gateway_connect(self) -> None:
        self.gateway: pyrevolt.Gateway = pyrevolt.Gateway()
        await self.gateway.Connect()
        await self.gateway.Send({
            "type": pyrevolt.GatewayEvent.Ping.value,
            "data": 0
        })
        self.assertEqual({
            "type": pyrevolt.GatewayEvent.Pong.value,
            "data": 0
        }, await self.gateway.Receive())
        await self.gateway.Close()

if __name__ == "__main__":
    unittest.main(verbosity=2)