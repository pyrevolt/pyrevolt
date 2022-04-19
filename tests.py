import asyncio
import unittest
import os
import pyvolt

class HTTPTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client: pyvolt.HTTPClient = pyvolt.HTTPClient()
        return await super().asyncSetUp()

    async def asyncTearDown(self) -> None:
        await self.client.Close()
        return await super().asyncTearDown()

    async def test_request(self) -> None:
        request: pyvolt.Request = pyvolt.Request(pyvolt.Method.GET, "/")
        
        result: dict = await self.client.Request(request)
        self.assertEqual(result["ws"], "wss://ws.revolt.chat")
        await self.client.Close()

    async def test_fetch_user(self) -> None:
        user: str = "01FYEQ9FTJ62N39TGZ9P7BMCZD"
        request: pyvolt.Request = pyvolt.Request(pyvolt.Method.GET, "/users/" + user)
        request.AddAuthentication(os.getenv("token"))
        
        result: dict = await self.client.Request(request)
        self.assertEqual(result["username"], "Fabio")

class GatewayTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.gateway: pyvolt.Gateway = pyvolt.Gateway()
        return await super().asyncSetUp()

    async def asyncTearDown(self) -> None:
        await self.gateway.Close()
        return await super().asyncTearDown()

    async def test_get_gateway_url(self) -> None:
        result: dict = await self.gateway.GetWebsocketURL()
        self.assertEqual(result, "wss://ws.revolt.chat")

    async def test_gateway_connect(self) -> None:
        await self.gateway.Connect()
        await self.gateway.Send({
            "type": pyvolt.GatewayEvent.Ping.value.VALUE,
            "data": 0
        })
        self.assertEqual({
            "type": pyvolt.GatewayEvent.Pong.value.VALUE,
            "data": 0
        }, await self.gateway.Receive())

    async def test_gateway_keep_alive(self) -> None:
        expectedPongResult: dict = {
            "type": pyvolt.GatewayEvent.Pong.value.VALUE,
            "data": 0
        }
        await self.gateway.Connect()
        await self.gateway.Send({
            "type": pyvolt.GatewayEvent.Ping.value.VALUE,
            "data": 0
        })
        self.assertEqual(expectedPongResult, await self.gateway.Receive())
        result: dict = await asyncio.wait_for(self.gateway.Receive(), timeout=30)
        self.assertEqual(expectedPongResult, result)

    async def test_gateway_identify(self) -> None:
        expectedAuthenticatedResult: dict = {
            "type": pyvolt.GatewayEvent.Authenticated.value.VALUE
        }
        await self.gateway.Connect()
        await self.gateway.Authenticate(os.getenv("token"))
        self.assertEqual(expectedAuthenticatedResult, await self.gateway.Receive())

class SessionTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session: pyvolt.Session = pyvolt.Session()
        await self.session.Start(os.getenv("token"))
        return await super().asyncSetUp()

    async def asyncTearDown(self) -> None:
        await self.session.Close()
        return await super().asyncTearDown()

    async def test_session(self) -> None:
        await self.session.GatewayReceive()
        result: dict = await self.session.GatewayReceive()
        self.assertEqual(result["type"], pyvolt.GatewayEvent.Ready.value)
        for user in result["users"]:
            self.assertIsInstance(user, pyvolt.User)
        for channel in result["channels"]:
            self.assertIsInstance(channel, pyvolt.Channel)
        for server in result["servers"]:
            self.assertIsInstance(server, pyvolt.Server)

if __name__ == "__main__":
    unittest.main(verbosity=2)