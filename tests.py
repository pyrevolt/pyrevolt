import asyncio
import unittest
import os
import pyvolt

class HTTPTests(unittest.IsolatedAsyncioTestCase):
    async def asyncTearDown(self) -> None:
        await asyncio.sleep(0)
        return await super().asyncTearDown()

    async def test_request(self) -> None:
        client: pyvolt.HTTPClient = pyvolt.HTTPClient()
        request: pyvolt.Request = pyvolt.Request(pyvolt.Method.GET, "/")
        
        result: dict = await client.Request(request)
        self.assertEqual(result["ws"], "wss://ws.revolt.chat")
        await client.Close()

    async def test_fetch_user(self) -> None:
        client: pyvolt.HTTPClient = pyvolt.HTTPClient()
        user: str = "01FYEQ9FTJ62N39TGZ9P7BMCZD"
        request: pyvolt.Request = pyvolt.Request(pyvolt.Method.GET, "/users/" + user)
        request.AddAuthentication(os.getenv("token"))
        
        result: dict = await client.Request(request)
        self.assertEqual(result["username"], "Fabio")
        await client.Close()

class GatewayTests(unittest.IsolatedAsyncioTestCase):
    async def test_gateway_url(self) -> None:
        gateway: pyvolt.Gateway = pyvolt.Gateway()
        result: dict = await gateway.GetWebsocketURL()
        self.assertEqual(result, "wss://ws.revolt.chat")
        await gateway.Close()

    async def test_gateway_connect(self) -> None:
        self.gateway: pyvolt.Gateway = pyvolt.Gateway()
        await self.gateway.Connect()
        await self.gateway.Send({
            "type": pyvolt.GatewayEvent.Ping.value,
            "data": 0
        })
        self.assertEqual({
            "type": pyvolt.GatewayEvent.Pong.value,
            "data": 0
        }, await self.gateway.Receive())
        await self.gateway.Close()

    async def test_gateway_keep_alive(self) -> None:
        self.gateway: pyvolt.Gateway = pyvolt.Gateway()
        expectedPongResult: dict = {
            "type": pyvolt.GatewayEvent.Pong.value,
            "data": 0
        }
        await self.gateway.Connect()
        await self.gateway.Send({
            "type": pyvolt.GatewayEvent.Ping.value,
            "data": 0
        })
        self.assertEqual(expectedPongResult, await self.gateway.Receive())
        result: dict = await asyncio.wait_for(self.gateway.Receive(), timeout=30)
        self.assertEqual(expectedPongResult, result)

    async def test_gateway_identify(self) -> None:
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)