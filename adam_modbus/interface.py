import asyncio
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Literal


class AdamConnectionError(RuntimeError):
    pass


DEFAULT_ADAM_PORT = 1025
ADAM_CONNECTION_TIMEOUT = 0.1


@dataclass
class AdamConnection:
    socket: socket.socket
    ip: str
    port: int
    timeout: float = ADAM_CONNECTION_TIMEOUT
    model: str | None = None

    async def _send_and_receive(self, message: str) -> str:
        loop = asyncio.get_running_loop()

        try:
            await asyncio.wait_for(
                loop.sock_sendall(self.socket, message.encode("ascii")),
                self.timeout,
            )
            adam_out = await asyncio.wait_for(
                loop.sock_recv(self.socket, 100), self.timeout
            )
        except asyncio.TimeoutError:
            raise AdamConnectionError("ADAM connection timed out")

        response = adam_out.decode().strip()
        return response

    async def set_digital_out(
        self,
        pin: int,
        value: bool,
        model: None | Literal["6052"] | Literal["6317"] = None,
    ) -> None:
        if model is not None:
            self.model = model

        assert self.model is not None, "Model must be set before setting digital out"

        if self.model == "6052":
            command = f"#011{pin:x}0{int(value)}\r"
        elif self.model == "6317":
            command = f"#01D0{pin:x}{int(value)}\r"
        else:
            raise NotImplementedError(
                f"Digital out not implemented for Adam-{self.model}"
            )

        response = await self._send_and_receive(command)
        assert response[:3] == ">01", response[:3]

    async def get_adam_digital_inputs(self) -> list[bool]:
        response = await self._send_and_receive("$016\r")
        assert response[:3] == "!01", f"Unexpected response: {response}"

        binary_string = "".join(f"{int(char, 16):0>4b}" for char in response[3:])
        return [char == "1" for char in binary_string][::-1]

    async def get_adam_analog_inputs(self) -> list[float]:
        response = await self._send_and_receive("#01\r")

        assert response[:3] == ">01", response
        response_data = response[3:]

        # 7 characters per channel: +00.011
        assert len(response_data) % 7 == 0, response_data

        return [
            float(response_data[i * 7 : i * 7 + 7])
            for i in range(len(response_data) // 7)
        ]

    async def get_adam_model(self) -> str:
        response = await self._send_and_receive("$01M\r")

        assert response[:3] == "!01", f"Unexpected response: {response}"

        self.model = response[3:]

        return self.model

    async def enable_high_speed_analog_integration(self) -> None:
        response = await self._send_and_receive("%0100000020\r")
        assert response[:3] == "!01", f"Unexpected response: {response}"


@asynccontextmanager
async def adam_connection_context(
    ip: str,
    port: int = DEFAULT_ADAM_PORT,
    timeout: float = ADAM_CONNECTION_TIMEOUT,
) -> AsyncIterator[AdamConnection]:
    adam_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    loop = asyncio.get_running_loop()

    # according to chatgpt, asyncio does not support timeouts on UDP sockets
    # so we manually do this with asyncio.wait_for, otherwise it will hang forever
    adam_sock.setblocking(False)

    try:
        await loop.sock_connect(adam_sock, (ip, port))
        yield AdamConnection(
            adam_sock,
            ip,
            port,
            timeout,
        )

    except OSError:
        raise AdamConnectionError(f"Could not connect to ADAM at {ip}")

    finally:
        adam_sock.close()
