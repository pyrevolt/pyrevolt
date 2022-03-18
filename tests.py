import unittest
import os
import pyrevolt

class HTTPTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        return super().setUp()

    async def test_request(self) -> None:
        client = pyrevolt.HTTPClient()
        request = pyrevolt.Request(pyrevolt.Method.GET, "/")
        
        result = await client.request(request)
        self.assertEqual(result["ws"], "wss://ws.revolt.chat")
        await client.close()

    async def test_fetch_user(self) -> None:
        client = pyrevolt.HTTPClient()
        user = "01FYEQ9FTJ62N39TGZ9P7BMCZD"
        request = pyrevolt.Request(pyrevolt.Method.GET, "/users/" + user)
        request.AddAuthentication(os.getenv("token"))
        
        result = await client.request(request)
        self.assertEqual(result["username"], "Fabio")
        await client.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)